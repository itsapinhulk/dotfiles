brew update &&
brew install \
  bash \
  bash-completion@2 \
  fd \
  fzf \
  git \
  git-lfs \
  jj \
  lua \
  luarocks \
  neovim \
  nvm \
  ripgrep \
  the_silver_searcher \
  tmux \
  tmuxp \
  tpm \
  &&
brew upgrade &&
brew autoremove
