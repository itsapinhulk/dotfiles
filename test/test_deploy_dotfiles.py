"""
test_deploy_dotfiles.py — unittest test suite for deploy-dotfiles.

Run with:
    python test/test_deploy_dotfiles.py

Cross-platform notes
--------------------
* Symlink tests are skipped on Windows unless the process has the required
  privilege (Developer Mode or admin).
* Path comparisons always use ``.resolve()`` to avoid drive-letter casing
  differences on Windows.
* No test hard-codes Unix paths such as ``/tmp``.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import io
import platform
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

# ---------------------------------------------------------------------------
# Load deploy-dotfiles (hyphenated name, no .py extension)
# ---------------------------------------------------------------------------

_SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "deploy-dotfiles"
_loader = importlib.machinery.SourceFileLoader("deploy_dotfiles", str(_SCRIPT_PATH))
_spec = importlib.util.spec_from_loader("deploy_dotfiles", _loader)
_module = importlib.util.module_from_spec(_spec)
sys.modules["deploy_dotfiles"] = _module
_spec.loader.exec_module(_module)

from deploy_dotfiles import (
    DeployContext,
    HandlerResult,
    SpecialHandler,
    SPECIAL_HANDLERS,
    SYMLINK_WHOLE_DIRS,
    deploy_repos_with_priority,
    deploy_repos_with_priority,
    make_backup,
    repo_name_to_target_name,
    resolve_target_path,
    settings_root,
    subpath_to_target,
    main,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _can_symlink() -> bool:
    """Return True if the current process can create symlinks."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        probe = tmp_path / "_probe"
        target = tmp_path / "_target"
        target.write_text("x")
        try:
            probe.symlink_to(target)
            probe.unlink()
            return True
        except (OSError, NotImplementedError):
            return False


def _make_ctx(target_root: Path, backup_root: Path | None = None,
              dry_run: bool = False) -> DeployContext:
    return DeployContext(
        target_root=target_root,
        backup_root=backup_root,
        dry_run=dry_run,
        verbose=False,
    )


def make_test_repo(base: Path, name: str, files: dict[str, str]) -> Path:
    """Create a test repo with files under its settings/ directory."""
    repo = base / name
    (repo / "settings").mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        p = repo / "settings" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    return repo


# ---------------------------------------------------------------------------
# Tests for resolve_target_path
# ---------------------------------------------------------------------------

class TestResolveTargetPath(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_ordinary_file(self):
        """Non-mapped subpath resolves to root / translated name."""
        root = self.tmp / "home"
        result = resolve_target_path(root, Path("_dot_bashrc"))
        self.assertEqual(result, root / ".bashrc")

    def test_nested_path(self):
        """Nested subpath is fully translated under root."""
        root = self.tmp / "home"
        result = resolve_target_path(root, Path("_dot_local") / "bin")
        self.assertEqual(result, root / ".local" / "bin")

    def test_returns_path_object(self):
        """resolve_target_path returns a Path instance."""
        root = self.tmp / "home"
        result = resolve_target_path(root, Path("_dot_bashrc"))
        self.assertIsInstance(result, Path)

    def test_unmapped_subpath_under_root(self):
        """A path not in OS_PATH_MAP is placed directly under root."""
        root = self.tmp / "home"
        result = resolve_target_path(root, Path("_dot_bashrc"))
        self.assertTrue(str(result).startswith(str(root)))


# ---------------------------------------------------------------------------
# Tests for repo_name_to_target_name
# ---------------------------------------------------------------------------

class TestRepoNameToTargetName(unittest.TestCase):

    def test_dot_prefix_converted(self):
        """_dot_ prefix becomes a leading dot."""
        self.assertEqual(repo_name_to_target_name("_dot_bashrc"), ".bashrc")
        self.assertEqual(repo_name_to_target_name("_dot_emacs"), ".emacs")

    def test_non_dot_name_unchanged(self):
        """Names without the _dot_ prefix are returned as-is."""
        self.assertEqual(repo_name_to_target_name("vimrc"), "vimrc")
        self.assertEqual(repo_name_to_target_name("README.md"), "README.md")


# ---------------------------------------------------------------------------
# Tests for subpath_to_target
# ---------------------------------------------------------------------------

class TestSubpathToTarget(unittest.TestCase):

    def test_single_component(self):
        """Single _dot_-prefixed component is translated."""
        result = subpath_to_target(Path("_dot_vimrc"))
        self.assertEqual(result, Path(".vimrc"))

    def test_nested_components(self):
        """Each component is translated independently."""
        result = subpath_to_target(Path("_dot_config") / "app")
        self.assertEqual(result, Path(".config") / "app")


# ---------------------------------------------------------------------------
# Tests for settings_root
# ---------------------------------------------------------------------------

class TestSettingsRoot(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_settings_subdir_preferred(self):
        """settings/ subdirectory is used when present."""
        repo = self.tmp / "repo"
        (repo / "settings").mkdir(parents=True)
        self.assertEqual(settings_root(repo), repo / "settings")

    def test_repo_root_fallback(self):
        """Repo root is used when no settings/ subdirectory exists."""
        repo = self.tmp / "repo"
        repo.mkdir()
        self.assertEqual(settings_root(repo), repo)


# ---------------------------------------------------------------------------
# Tests for make_backup
# ---------------------------------------------------------------------------

class TestMakeBackup(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.dest = self.tmp / "backup"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_backup_file(self):
        """A file is copied to dest."""
        src = self.tmp / "file.txt"
        src.write_text("content")
        dest = self.dest / "file.txt"
        make_backup(src, dest, dry_run=False)
        if platform.system() == "Windows":
            # Windows writes a pointer .txt file instead of copying
            pointer = (self.dest / "file.txt.txt").read_text()
            self.assertEqual(Path(pointer).resolve(), src.resolve())
        else:
            self.assertEqual(dest.read_text(), "content")
        self.assertTrue(src.exists())  # original untouched

    def test_backup_directory(self):
        """A directory is copied to dest."""
        src = self.tmp / "mydir"
        src.mkdir()
        (src / "file.txt").write_text("content")
        dest = self.dest / "mydir"
        make_backup(src, dest, dry_run=False)
        if platform.system() == "Windows":
            # Windows writes a pointer .txt file instead of copying
            pointer = (self.dest / "mydir.txt").read_text()
            self.assertEqual(Path(pointer).resolve(), src.resolve())
        else:
            self.assertTrue(dest.is_dir())
            self.assertEqual((dest / "file.txt").read_text(), "content")

    def test_backup_nonexistent_is_noop(self):
        """Backing up a nonexistent path does nothing (no error)."""
        make_backup(self.tmp / "nonexistent", self.dest / "nonexistent", dry_run=False)
        self.assertFalse(self.dest.exists())

    def test_backup_dry_run_creates_nothing(self):
        """dry_run=True does not write any files."""
        src = self.tmp / "file.txt"
        src.write_text("content")
        make_backup(src, self.dest / "file.txt", dry_run=True)
        self.assertFalse(self.dest.exists())


# ---------------------------------------------------------------------------
# Tests for special handlers
# ---------------------------------------------------------------------------

class TestSpecialHandlers(unittest.TestCase):

    def test_special_handlers_dict(self):
        """SPECIAL_HANDLERS maps strings to SpecialHandler instances."""
        self.assertIsInstance(SPECIAL_HANDLERS, dict)
        for name, handler in SPECIAL_HANDLERS.items():
            self.assertIsInstance(name, str)
            self.assertIsInstance(handler, SpecialHandler)

    def test_symlink_whole_dirs_is_set(self):
        """SYMLINK_WHOLE_DIRS is a set."""
        self.assertIsInstance(SYMLINK_WHOLE_DIRS, set)


# ---------------------------------------------------------------------------
# Tests for DeployContext
# ---------------------------------------------------------------------------

class TestDeployContext(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_deploy_context_init(self):
        """DeployContext stores its constructor arguments."""
        home = self.tmp / "home"
        backup = self.tmp / "backup"
        ctx = DeployContext(
            target_root=home,
            backup_root=backup,
            dry_run=True,
            verbose=False,
        )
        self.assertEqual(ctx.target_root, home)
        self.assertEqual(ctx.backup_root, backup)
        self.assertTrue(ctx.dry_run)

    def test_run_backup_dir_under_backup_root(self):
        """run_backup_dir is a subdirectory of backup_root when provided."""
        home = self.tmp / "home"
        backup = self.tmp / "backup"
        ctx = DeployContext(
            target_root=home,
            backup_root=backup,
            dry_run=False,
            verbose=False,
        )
        self.assertIsNotNone(ctx.run_backup_dir)
        self.assertEqual(ctx.run_backup_dir.parent, backup)

    def test_backup_path_outside_target_root(self):
        """ctx.backup falls back to path.name when path is outside target_root.

        On Windows, OS_PATH_MAP redirects some paths (e.g. .config/nvim) to
        AppData locations that are outside a test's temp target_root.  This
        exercises the ValueError fallback in ctx.backup.
        """
        home = self.tmp / "home"
        home.mkdir()
        outside = self.tmp / "other_dir"
        outside.mkdir()
        target_file = outside / ".nvimrc"
        target_file.write_text("colorscheme dark")
        backup_root = self.tmp / "backup"
        ctx = _make_ctx(home, backup_root=backup_root)
        # path is outside target_root → relative_to raises ValueError
        ctx.backup(target_file)
        if platform.system() == "Windows":
            pointer = (ctx.run_backup_dir / "_dot_nvimrc.txt").read_text()
            self.assertEqual(Path(pointer).resolve(), target_file.resolve())
        else:
            expected = ctx.run_backup_dir / "_dot_nvimrc"
            self.assertTrue(expected.exists())
            self.assertEqual(expected.read_text(), "colorscheme dark")

    def test_backup_translates_dot_components(self):
        """ctx.backup translates all dotted path components under target_root."""
        home = self.tmp / "home"
        home.mkdir()
        # Create .config/vim/init.vim under home
        nested = home / ".config" / "vim"
        nested.mkdir(parents=True)
        target_file = nested / "init.vim"
        target_file.write_text("set number")
        backup_root = self.tmp / "backup"
        ctx = _make_ctx(home, backup_root=backup_root)
        ctx.backup(target_file)
        if platform.system() == "Windows":
            pointer = (ctx.run_backup_dir / "_dot_config" / "vim" / "init.vim.txt").read_text()
            self.assertEqual(Path(pointer).resolve(), target_file.resolve())
        else:
            expected = ctx.run_backup_dir / "_dot_config" / "vim" / "init.vim"
            self.assertTrue(expected.exists())
            self.assertEqual(expected.read_text(), "set number")


# ---------------------------------------------------------------------------
# Tests for HandlerResult
# ---------------------------------------------------------------------------

class TestHandlerResult(unittest.TestCase):

    def test_no_change(self):
        """changed=False means the target is already correct."""
        result = HandlerResult(changed=False, description="Already correct")
        self.assertFalse(result.changed)
        self.assertEqual(result.description, "Already correct")

    def test_change_needed(self):
        """changed=True means the target needs updating."""
        result = HandlerResult(changed=True, description="Needs update")
        self.assertTrue(result.changed)
        self.assertEqual(result.description, "Needs update")


# ---------------------------------------------------------------------------
# Tests for deploy_repo
# ---------------------------------------------------------------------------

class TestDeployRepo(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.home = self.tmp / "home"
        self.home.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_deploy_repo_simple_symlink(self):
        """deploy_repo symlinks a top-level settings file into the target dir."""
        if not _can_symlink():
            self.skipTest("Symlinks not available on this platform")
        repo = make_test_repo(self.tmp, "repo", {"_dot_vimrc": "set number"})
        deploy_repos_with_priority(_make_ctx(self.home), [repo])
        vimrc = self.home / ".vimrc"
        self.assertTrue(vimrc.is_symlink())
        self.assertEqual(vimrc.read_text(), "set number")

    def test_deploy_repo_with_nested_files(self):
        """deploy_repo recurses into subdirectories and symlinks files."""
        if not _can_symlink():
            self.skipTest("Symlinks not available on this platform")
        repo = make_test_repo(self.tmp, "repo", {"_dot_config/vim/init.vim": "set number"})
        deploy_repos_with_priority(_make_ctx(self.home), [repo])
        init_vim = self.home / ".config" / "vim" / "init.vim"
        self.assertTrue(init_vim.is_symlink())
        self.assertEqual(init_vim.read_text(), "set number")


# ---------------------------------------------------------------------------
# Tests for deploy_repos_with_priority
# ---------------------------------------------------------------------------

class TestDeployReposWithPriority(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.home = self.tmp / "home"
        self.home.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_deploy_repos_with_priority_ordering(self):
        """First repo wins when multiple repos provide the same path."""
        if not _can_symlink():
            self.skipTest("Symlinks not available on this platform")
        repo1 = make_test_repo(self.tmp, "base",     {"_dot_bashrc": "base"})
        repo2 = make_test_repo(self.tmp, "personal", {"_dot_bashrc": "personal"})
        repo3 = make_test_repo(self.tmp, "work",     {"_dot_bashrc": "work"})
        deploy_repos_with_priority(_make_ctx(self.home), [repo1, repo2, repo3])
        self.assertEqual((self.home / ".bashrc").read_text(), "base")


# ---------------------------------------------------------------------------
# Tests for main
# ---------------------------------------------------------------------------

class TestMain(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_main_help(self):
        """--help prints usage and exits 0."""
        buf = io.StringIO()
        with redirect_stdout(buf):
            with self.assertRaises(SystemExit) as cm:
                main(["--help"])
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("usage", buf.getvalue().lower())

    def test_main_invalid_args(self):
        """Unrecognised argument exits non-zero."""
        with self.assertRaises(SystemExit) as cm:
            main(["--invalid-arg"])
        self.assertNotEqual(cm.exception.code, 0)

    def test_main_dry_run(self):
        """Default (no --apply) is a dry-run: no files are created."""
        repo = make_test_repo(self.tmp, "repo", {"_dot_bashrc": "content"})
        home = self.tmp / "home"
        home.mkdir()
        buf = io.StringIO()
        with redirect_stdout(buf):
            result = main([str(repo), "--target", str(home)])
        self.assertEqual(result, 0)
        self.assertFalse((home / ".bashrc").exists())


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.home = self.tmp / "home"
        self.home.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_full_deployment_workflow(self):
        """End-to-end: files and nested dirs are symlinked into the target home."""
        if not _can_symlink():
            self.skipTest("Symlinks not available on this platform")
        repo = make_test_repo(self.tmp, "repo", {
            "_dot_vimrc": "set number",
            "_dot_vim/init.vim": "set number",
        })
        deploy_repos_with_priority(_make_ctx(self.home), [repo])
        self.assertTrue((self.home / ".vimrc").is_symlink())
        self.assertEqual((self.home / ".vimrc").read_text(), "set number")
        self.assertTrue((self.home / ".vim" / "init.vim").is_symlink())
        self.assertEqual((self.home / ".vim" / "init.vim").read_text(), "set number")

    def test_deployment_with_backups(self):
        """Existing files are backed up before being replaced by symlinks."""
        if not _can_symlink():
            self.skipTest("Symlinks not available on this platform")
        (self.home / ".bashrc").write_text("old config")
        backup_root = self.tmp / "backup"
        repo = make_test_repo(self.tmp, "repo", {"_dot_bashrc": "new config"})
        ctx = _make_ctx(self.home, backup_root=backup_root)
        deploy_repos_with_priority(ctx, [repo])
        self.assertTrue((self.home / ".bashrc").is_symlink())
        self.assertEqual((self.home / ".bashrc").read_text(), "new config")
        self.assertEqual(ctx.run_backup_dir.parent, backup_root)
        if platform.system() == "Windows":
            pointer = (ctx.run_backup_dir / "_dot_bashrc.txt").read_text()
            self.assertEqual(Path(pointer).resolve(), (self.home / ".bashrc").resolve())
        else:
            self.assertEqual((ctx.run_backup_dir / "_dot_bashrc").read_text(), "old config")


# ---------------------------------------------------------------------------
# Tests for .gitconfig special handler
# ---------------------------------------------------------------------------

class TestGitconfigHandler(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.home = self.tmp / "home"
        self.home.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_gitconfig_gets_include_not_symlink(self):
        """_dot_gitconfig is deployed via [include], not a plain symlink."""
        repo = make_test_repo(self.tmp, "repo", {"_dot_gitconfig": "[user]\n\tname = Test\n"})
        deploy_repos_with_priority(_make_ctx(self.home), [repo])
        gitconfig = self.home / ".gitconfig"
        self.assertFalse(gitconfig.is_symlink())
        self.assertIn("[include]", gitconfig.read_text())

    def test_gitconfig_include_points_to_repo_file(self):
        """The [include] path points to the repo's _dot_gitconfig."""
        repo = make_test_repo(self.tmp, "repo", {"_dot_gitconfig": "[user]\n\tname = Test\n"})
        src = repo / "settings" / "_dot_gitconfig"
        deploy_repos_with_priority(_make_ctx(self.home), [repo])
        self.assertIn(str(src), (self.home / ".gitconfig").read_text())

    def test_gitconfig_idempotent(self):
        """Deploying twice does not duplicate the [include] block."""
        repo = make_test_repo(self.tmp, "repo", {"_dot_gitconfig": "[user]\n\tname = Test\n"})
        ctx = _make_ctx(self.home)
        deploy_repos_with_priority(ctx, [repo])
        content_after_first = (self.home / ".gitconfig").read_text()
        deploy_repos_with_priority(ctx, [repo])
        self.assertEqual((self.home / ".gitconfig").read_text(), content_after_first)

    def test_gitconfig_uses_two_space_indent(self):
        """Generated [include] block uses 2-space indentation, not tabs."""
        repo = make_test_repo(self.tmp, "repo", {"_dot_gitconfig": "[user]\n  name = Test\n"})
        deploy_repos_with_priority(_make_ctx(self.home), [repo])
        text = (self.home / ".gitconfig").read_text()
        self.assertIn("  path = ", text)
        self.assertNotIn("\tpath = ", text)

    def test_gitconfig_idempotent_with_spaces(self):
        """Idempotency check works when existing file uses spaces instead of tabs."""
        repo = make_test_repo(self.tmp, "repo", {"_dot_gitconfig": "[user]\n  name = Test\n"})
        src = repo / "settings" / "_dot_gitconfig"
        # Pre-create .gitconfig with a space-indented include (as generated by this tool)
        gitconfig = self.home / ".gitconfig"
        gitconfig.write_text(f"[include]\n  path = {src}\n")
        ctx = _make_ctx(self.home)
        deploy_repos_with_priority(ctx, [repo])
        # Should not add a second [include] block
        self.assertEqual((self.home / ".gitconfig").read_text().count("[include]"), 1)

    def test_gitconfig_no_leading_blank_line(self):
        """Inserting into a file with no leading comments produces no blank line at top."""
        repo = make_test_repo(self.tmp, "repo", {"_dot_gitconfig": "[user]\n  name = Test\n"})
        # Pre-create .gitconfig with content but no leading comments
        (self.home / ".gitconfig").write_text("[user]\n  email = test@example.com\n")
        deploy_repos_with_priority(_make_ctx(self.home), [repo])
        text = (self.home / ".gitconfig").read_text()
        self.assertFalse(text.startswith("\n"), f"file starts with blank line: {text!r}")


# ---------------------------------------------------------------------------
# Tests for .config/conda/condarc special handler
# ---------------------------------------------------------------------------

class TestBashrcHandler(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.home = self.tmp / "home"
        self.home.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_bashrc_file_symlinked(self):
        """_dot_bashrc is symlinked into ~/.bashrc."""
        if not _can_symlink():
            self.skipTest("Symlinks not available on this platform")
        repo = make_test_repo(self.tmp, "repo", {"_dot_bashrc": "export PATH=~/bin:$PATH\n"})
        deploy_repos_with_priority(_make_ctx(self.home), [repo])
        self.assertTrue((self.home / ".bashrc").is_symlink())

    def test_bash_profile_alias_created(self):
        """~/.bash_profile is created as a symlink to ~/.bashrc."""
        if not _can_symlink():
            self.skipTest("Symlinks not available on this platform")
        repo = make_test_repo(self.tmp, "repo", {"_dot_bashrc": "export PATH=~/bin:$PATH\n"})
        deploy_repos_with_priority(_make_ctx(self.home), [repo])
        alias = self.home / ".bash_profile"
        self.assertTrue(alias.is_symlink())
        self.assertEqual(alias.resolve(), (self.home / ".bashrc").resolve())


class TestCondaHandler(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.home = self.tmp / "home"
        self.home.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_condarc_file_symlinked(self):
        """condarc is symlinked into .config/conda/condarc."""
        if not _can_symlink():
            self.skipTest("Symlinks not available on this platform")
        repo = make_test_repo(self.tmp, "repo", {"_dot_config/conda/condarc": "channels:\n  - defaults\n"})
        deploy_repos_with_priority(_make_ctx(self.home), [repo])
        self.assertTrue((self.home / ".config" / "conda" / "condarc").is_symlink())

    def test_condarc_alias_created(self):
        """~/.condarc is created as a symlink to ~/.config/conda/condarc."""
        if not _can_symlink():
            self.skipTest("Symlinks not available on this platform")
        repo = make_test_repo(self.tmp, "repo", {"_dot_config/conda/condarc": "channels:\n  - defaults\n"})
        deploy_repos_with_priority(_make_ctx(self.home), [repo])
        alias = self.home / ".condarc"
        self.assertTrue(alias.is_symlink())
        self.assertEqual(alias.resolve(), (self.home / ".config" / "conda" / "condarc").resolve())


# ---------------------------------------------------------------------------
# Tests for SYMLINK_WHOLE_DIRS
# ---------------------------------------------------------------------------

class TestSymlinkWholeDirs(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.home = self.tmp / "home"
        self.home.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_whole_dir_symlinked_not_recursed(self):
        """A path in SYMLINK_WHOLE_DIRS is symlinked as a unit, not recursed."""
        if not _can_symlink():
            self.skipTest("Symlinks not available on this platform")
        # .config/nvim/lua is in SYMLINK_WHOLE_DIRS
        repo = make_test_repo(self.tmp, "repo", {
            "_dot_config/nvim/lua/init.lua": "-- init",
            "_dot_config/nvim/lua/plugin.lua": "-- plugin",
        })
        deploy_repos_with_priority(_make_ctx(self.home), [repo])
        lua_dir = self.home / ".config" / "nvim" / "lua"
        # The directory itself should be a symlink, not its contents individually
        self.assertTrue(lua_dir.is_symlink())
        self.assertFalse((lua_dir / "init.lua").is_symlink())  # files inside are not symlinks


# ---------------------------------------------------------------------------
# Tests for skip_paths
# ---------------------------------------------------------------------------

class TestSkipPaths(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.home = self.tmp / "home"
        self.home.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_skipped_path_not_deployed(self):
        """A path in skip_paths is not deployed."""
        if not _can_symlink():
            self.skipTest("Symlinks not available on this platform")
        repo = make_test_repo(self.tmp, "repo", {
            "_dot_bashrc": "bash",
            "_dot_vimrc": "vim",
        })
        ctx = DeployContext(
            target_root=self.home,
            backup_root=None,
            dry_run=False,
            verbose=False,
            skip_paths=frozenset({".bashrc"}),
        )
        deploy_repos_with_priority(ctx, [repo])
        self.assertFalse((self.home / ".bashrc").exists())
        self.assertTrue((self.home / ".vimrc").is_symlink())

    def test_main_skip_flag(self):
        """--skip prevents a path from being deployed."""
        if not _can_symlink():
            self.skipTest("Symlinks not available on this platform")
        repo = make_test_repo(self.tmp, "repo", {
            "_dot_bashrc": "bash",
            "_dot_vimrc": "vim",
        })
        buf = io.StringIO()
        with redirect_stdout(buf):
            result = main([str(repo), "--target", str(self.home),
                           "--apply", "--skip", ".bashrc"])
        self.assertEqual(result, 0)
        self.assertFalse((self.home / ".bashrc").exists())
        self.assertTrue((self.home / ".vimrc").is_symlink())


# ---------------------------------------------------------------------------
# Tests for --apply
# ---------------------------------------------------------------------------

class TestApply(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.home = self.tmp / "home"
        self.home.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_apply_creates_symlinks(self):
        """--apply actually creates symlinks (dry-run does not)."""
        if not _can_symlink():
            self.skipTest("Symlinks not available on this platform")
        repo = make_test_repo(self.tmp, "repo", {"_dot_bashrc": "content"})
        buf = io.StringIO()
        with redirect_stdout(buf):
            result = main([str(repo), "--target", str(self.home), "--apply"])
        self.assertEqual(result, 0)
        self.assertTrue((self.home / ".bashrc").is_symlink())

    def test_missing_repo_exits_nonzero(self):
        """A non-existent repo path causes main to return non-zero."""
        result = main([str(self.tmp / "nonexistent"), "--target", str(self.home)])
        self.assertNotEqual(result, 0)


# ---------------------------------------------------------------------------
# Tests for multi-repo priority: second repo fills in uncovered entries
# ---------------------------------------------------------------------------

class TestMultiRepoPriority(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.home = self.tmp / "home"
        self.home.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_second_repo_fills_in_missing_entries(self):
        """Entries not in the first repo are deployed from subsequent repos."""
        if not _can_symlink():
            self.skipTest("Symlinks not available on this platform")
        repo1 = make_test_repo(self.tmp, "base",     {"_dot_bashrc": "base"})
        repo2 = make_test_repo(self.tmp, "personal", {"_dot_vimrc": "vim"})
        deploy_repos_with_priority(_make_ctx(self.home), [repo1, repo2])
        self.assertEqual((self.home / ".bashrc").read_text(), "base")
        self.assertEqual((self.home / ".vimrc").read_text(), "vim")

    def test_first_repo_wins_for_overlapping_entries(self):
        """The first repo's version of a file takes priority over later repos."""
        if not _can_symlink():
            self.skipTest("Symlinks not available on this platform")
        repo1 = make_test_repo(self.tmp, "base",     {"_dot_bashrc": "base"})
        repo2 = make_test_repo(self.tmp, "personal", {"_dot_bashrc": "personal"})
        deploy_repos_with_priority(_make_ctx(self.home), [repo1, repo2])
        self.assertEqual((self.home / ".bashrc").read_text(), "base")


if __name__ == "__main__":
    unittest.main()
