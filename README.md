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

### NeoVim

1. Install `ripgrep`, `fd`, `node`, `cmake`, `lua` and `luarocks`

2. Either copy the contents of (for further customization) or link to `init.lua`

    ```
    settings/_dot_config/nvim/init.lua      -> ~/.config/nvim/init.lua
    ```

3. Create a soft link for the default set of configs

    ```
    settings/_dot_config/nvim/lua      -> ~/.config/nvim/lua
    ```
    or

    ```
    settings/_dot_config/nvim/lua/config      -> ~/.config/nvim/lua/config
    settings/_dot_config/nvim/lua/plugins     -> ~/.config/nvim/lua/plugins
    ```

### Fonts
Install any font in `fonts/` (using `./scripts/install_fonts.sh` on Linux)

