brew update --quiet &&
brew install --quiet \
  bash \
  bash-completion@2 \
  cmake \
  curl \
  fd \
  fzf \
  git \
  git-lfs \
  ipython \
  jj \
  jupyterlab \
  lua \
  luarocks \
  neovim \
  ninja  \
  nvm \
  ripgrep \
  the_silver_searcher \
  tmux \
  tmuxp \
  tpm \
  wget \
  zip \
  &&
brew upgrade &&
brew autoremove
