# Dot Files

Repository of personal dot/setting files and environment setup

## Manual Setup

### General setting files
```
Setup soft links -

# Bash setting
settings/_dot_bashrc                    -> ~/.bashrc

# Vim and NeoVim settings
settings/_dot_config/nvim/init.vim      -> ~/.config/nvim/init.vim
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

### Fonts
Install any font in `fonts/`
