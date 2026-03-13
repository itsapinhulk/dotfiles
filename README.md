# Dot Files

Repository of personal dot/setting files and environment setup

## Automated Setup
The repo comes with a script to deploy all the settings and keep any further changes in sync. It will
preview the changes without `--apply`, and supports `--verbose` to print out every file it processes.

Either `deploy-dotfiles <repo> [--skip path] [--apply]`

Or, if you are maintaining your own dotfiles and this one is a submodule, you can either call

`deploy-dotfiles <main-repo> <fallback-repo> ... [--apply]`

The .bashrc has a helper function `sync-dotfiles` which calls the above, which can be further customized by 
setting `DOTFILES_SYNC_REPOS` and `DOTFILES_SYNC_SKIP`.

## Manual Setup
### NeoVim

1. Install `ripgrep`, `fzf`, `fd`, `cmake`, `lua(5.1)` and `luarocks(3+)`

2. Either copy the contents of (for further customization) or link to `init.lua` (deploy script can handle this)

    ```
    settings/_dot_config/nvim/init.lua      -> ~/.config/nvim/init.lua
    ```

3. Create a soft link for the default set of configs (deploy script can handle this).

    ```
    settings/_dot_config/nvim/lua                   -> ~/.config/nvim/lua
    settings/_dot_config/nvim/_dot_neoconf.json     -> ~/.config/nvim/.neoconf.json
    ```

    or

    ```
    settings/_dot_config/nvim/lua/config      -> ~/.config/nvim/lua/config
    settings/_dot_config/nvim/lua/plugins     -> ~/.config/nvim/lua/plugins
    ```

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
