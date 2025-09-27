brew update --quiet &&
brew install --quiet \
  bash \
  bash-completion@2 \
  cmake \
  curl \
  direnv \
  fd \
  fswatch \
  fzf \
  git \
  git-lfs \
  ipython \
  jj \
  jq \
  jupyterlab \
  libxml2 \
  lua \
  luarocks \
  neovim \
  ninja  \
  nvm \
  ripgrep \
  rsync \
  the_silver_searcher \
  tmux \
  tmuxp \
  tpm \
  wget \
  zip \
  &&
brew upgrade &&
brew autoremove
