ln -s ~/workspace/github/dotfiles/terminator ~/.config/

ln -s ~/workspace/github/dotfiles/bashrc ~/.bashrc

ln -s ~/workspace/github/dotfiles/vimrc ~/.vimrc

ln -s ~/workspace/github/dotfiles/dir_colors ~/.dir_colors

mkdir -p ~/.vim

ln -s ~/workspace/github/dotfiles/vim/autoload ~/.vim/
ln -s ~/workspace/github/dotfiles/vim/bundle ~/.vim/

mkdir -p ~/.fonts
ln -s ~/workspace/github/dotfiles/fonts/PowerlineSymbols.otf ~/.fonts/
sudo fc-cache -vf ~/.fonts
mkdir -p ~/.config/fontconfig/conf.d
ln -s ~/workspace/github/dotfiles/fonts/10-powerline-symbols.conf ~/.config/fontconfig/conf.d/

#something about git config

ln -s ~/workspace/github/dotfiles/git_settings/git-completion.bash ~/.git-completion.bash
ln -s ~/workspace/github/dotfiles/git_settings/git-prompt.sh ~/.git-prompt.sh


