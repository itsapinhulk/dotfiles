# Dot Files

Repository of personal dot/setting files and Nix based environment setup


## Manual Setup

### Bash, NeoVim
```
Setup soft links -
settings/_dot_config/nvim       -> ~/.config/nvim
settings/_dot_bashrc            -> ~/.bashrc
```

### Git
```
Add to ~/.gitconfig -
[include]
    path = /path/to/dotfiles/settings/gitconfig
```

### Fonts
```
mkir -p ~/.fonts
cp -r ext/source-code-pro/OTF/*.otf ~/.fonts
fc-cache -f -v
```

## To Do
* [ ] Add Nix based environment setup
* [ ] Automated setup script, including backups
* [ ] Check if all settings can be moved to nix expressions
