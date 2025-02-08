# Dot Files

Repository of personal dot/setting files and environment setup

## Manual Setup

### Bash, NeoVim, Tmux, Conda
```
Setup soft links -

settings/_dot_config/nvim/init.vim      -> ~/.config/nvim/init.vim
settings/_dot_ideavimrc                 -> ~/.ideavimrc

settings/_dot_bashrc                    -> ~/.bashrc

ext/tmux-conf/.tmux.conf                -> ~/.tmux.conf
settings/_dot_tmux.conf.local           -> ~/.tmux.conf.local

# Set up both since conda writes changes to the second file
settings/_dot_config/conda/condarc      -> ~/.config/conda/condarc
settings/_dot_config/conda/condarc      -> ~/.condarc
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
```
mkdir -p ~/.fonts
cp -r ext/source-code-pro/OTF/*.otf ~/.fonts
fc-cache -f -v
```
