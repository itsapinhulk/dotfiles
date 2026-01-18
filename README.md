# Dot Files

Repository of personal dot/setting files and environment setup

## Manual Setup

### General setting files
```
Setup soft links -

# Bash setting
settings/_dot_bashrc                    -> ~/.bashrc

# Ideamvim settings
settings/_dot_ideavimrc                 -> ~/.ideavimrc

# Tmux config
ext/tmux-conf/.tmux.conf                -> ~/.tmux.conf
settings/_dot_tmux.conf.local           -> ~/.tmux.conf.local

# Set up both since conda writes changes to the second file
settings/_dot_config/conda/condarc      -> ~/.config/conda/condarc
settings/_dot_config/conda/condarc      -> ~/.condarc

# Set configs for jujutsu (jj)
settings/_dot_config/jj/config.toml      -> ~/.config/jj/config.toml
# Note you'll also need to set up ~/.jjconfig.toml for personal settings

```

### Git
```
Setup soft link -
settings/_dot_gitignore_global  -> ~/.gitignore_global

Add to ~/.gitconfig -
[include]
    path = /path/to/dotfiles/settings/_dot_gitconfig
```

```
On Windows, enable long paths -
git config --global core.longpaths true
```

### NeoVim

1. Install `ripgrep`, `fzf`, `fd`, `cmake`, `lua(5.1)` and `luarocks(3+)`

2. Either copy the contents of (for further customization) or link to `init.lua`

    ```
    settings/_dot_config/nvim/init.lua      -> ~/.config/nvim/init.lua
    ```

3. Create a soft link for the default set of configs

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
Install any font in `fonts/` (using `./scripts/install_fonts.sh` on Linux)

### Homebrew

1. Install homebrew for your platform
2. Run `scripts/sync_homebrew.sh` to install and update

### ipython and Jupyter(lab)

1. For ipython, run `ipython profile create`
2. Replace `~/.ipython/profile_default/ipython_config.py` with link to `settings/_dot_ipython/profile_default/ipython_config.py`

3. For Jupyter, run `jupyter lab --generate-config`
4. Replace `~/.jupyter/jupyter_lab_config.py` with link to `settings/_dot_jupyter/jupyter_lab_config.py`

### Default login shell

To ensure the latest bash installed by `brew`, or any other non-standard installation
outside `/bin` is used, change the default login shell -

`sudo sh -c 'echo /path/to/new/bin/bash >> /etc/shells'`
`chsh -s /path/to/new/bin/bash`
