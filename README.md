# Dot Files

Repository of personal dot/setting files and Nix based environment setup

## Manual Setup

### Bash, NeoVim, Tmux
```
Setup soft links -

settings/_dot_config/nvim       -> ~/.config/nvim

settings/_dot_bashrc            -> ~/.bashrc

ext/tmux-conf/.tmux.conf        -> ~/.tmux.conf
settings/_dot_tmux.conf.local   -> ~/.tmux.conf.local
```

### Git
```
Setup soft link -
settings/_dot_gitignore_global  -> ~/.gitignore_global

Add to ~/.gitconfig -
[include]
    path = /path/to/dotfiles/settings/gitconfig
```

### Fonts
```
mkdir -p ~/.fonts
cp -r ext/source-code-pro/OTF/*.otf ~/.fonts
fc-cache -f -v
```

## To Do
* [ ] Add Nix based environment setup
* [ ] Automated setup script, including backups
* [ ] Check if all settings can be moved to nix expressions
