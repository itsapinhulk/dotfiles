# Dot Files

Repository of personal dot/setting files and environment setup.
There is also a Dockerfile which includes basic linux tools and configuration from this repo.
The built images are available on Docker Hub (https://hub.docker.com/r/itsapinhulk/devcontainer) and
GitHub Packages (https://ghcr.io/itsapinhulk/devcontainer).

## Automated Setup
The repo comes with a script to deploy all the settings and keep any further changes in sync. It will
preview the changes without `--apply`, and supports `--verbose` to print out every file it processes.

Either `deploy-dotfiles <repo> [--skip path] [--apply]`

Or, if you are maintaining your own dotfiles and this one is a submodule, you can call

`deploy-dotfiles <main-repo> <fallback-repo> ... [--apply]`

or, the repo also includes a `sync-dotfiles` script which calls the above, and can be further customized by
setting `DOTFILES_SYNC_REPOS` and `DOTFILES_SYNC_SKIP`.

If you are going to be a passive consumer of this repo, it is recommended that you include it as a submodule in your own personal dotfiles.
If you are going to be an active user of this repo, contributing changes, you should clone it in a directory alongside your personal dotfiles.

## Manual Setup

### Fonts
Install any font in `fonts/` (using `./scripts/install-dotfiles-font` on Linux)

### Homebrew

1. Install homebrew for your platform
2. Run `scripts/sync-brew` to install and update the set of brew packages
3. You customize the Brewfile used by the above script by setting `DOTFILES_BREWFILE`
4. To include this repo's Brewfile in your own, use the following snippet -

  `instance_eval(File.read("/path/to/itsapinhulk/dotfiles/scripts/Brewfile"))`

### ipython and Jupyter(lab)

1. For ipython, run `ipython profile create`
2. Run the script to replace `~/.ipython/profile_default/ipython_config.py` with link to `settings/_dot_ipython/profile_default/ipython_config.py`

3. For Jupyter, run `jupyter lab --generate-config`
4. Run the script to replace `~/.jupyter/jupyter_lab_config.py` with link to `settings/_dot_jupyter/jupyter_lab_config.py`

### Default login shell

To ensure the latest bash installed by `brew`, or any other non-standard installation
outside `/bin` is used, change the default login shell -

`sudo sh -c 'echo /path/to/new/bin/bash >> /etc/shells'`
`chsh -s /path/to/new/bin/bash`
