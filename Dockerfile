# syntax=docker/dockerfile:1
#
# Devcontainer image which includes basic linux tools and configuration from this dotfiles repo.
#
# Build args injected by build-and-push.sh:
#   USERNAME   – username for the image and default user
#   REPO_URL   – https:// URL of the origin remote
#   GIT_SHA    – full commit SHA baked into the image
#   BUILD_DATE – YYYYMMDD-hhmm for the image tag


# ── builder ───────────────────────────────────────────────────────────────────
# Shallow-clone the repo so the final image carries a small .git directory
# (enough for `git fetch` / `git merge`) rather than the full object history.
# Also remove the fonts/ directory to save space, since it isn't useful inside a container.
FROM ubuntu:24.04 AS builder

ARG REPO_URL=""
ARG GIT_SHA="unknown"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git git-lfs \
        ca-certificates \
    && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY . .

RUN git clone --local --no-hardlinks --depth=1 /src /dotfiles \
    && git -C /dotfiles remote remove origin \
    && if [ -n "${REPO_URL}" ]; then \
           git -C /dotfiles remote add origin "${REPO_URL}"; \
       fi \
    && git -C /dotfiles config --file /dotfiles/.gitmodules --get-regexp '^submodule\..+\.path$' \
       | while IFS=' ' read key path; do \
             name="${key#submodule.}"; name="${name%.path}"; \
             # Point each submodule at its already-present copy in /src rather than
             # fetching from the configured URL (which may be relative or require
             # network access). The -c flag overrides the URL transiently without
             # modifying .gitmodules or .git/config. \
             git -C /dotfiles -c protocol.file.allow=always -c "submodule.${name}.url=/src/${path}" \
                 submodule update --init --depth=1 -- "${path}"; \
         done \
    && rm -rf /dotfiles/fonts \
    && rm -rf /dotfiles/.git/lfs \
    && echo "${GIT_SHA}" > /dotfiles/.git-sha


# ── final ─────────────────────────────────────────────────────────────────────
FROM ubuntu:24.04

ARG USERNAME=devuser
ARG USER_UID=1111
ARG USER_GID=$USER_UID

ARG REPO_URL=""
ARG GIT_SHA="unknown"
ARG BUILD_DATE="unknown"

# Labels follow OCI image-spec conventions
LABEL org.opencontainers.image.revision="${GIT_SHA}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.source="${REPO_URL}"

# ── system deps ───────────────────────────────────────────────────────────────
RUN apt-get update && \
        apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        file \
        git git-lfs \
        procps \
        python3 \
        sudo \
    && rm -rf /var/lib/apt/lists/*

# ── user ───────────────────────────────────────────────────────────────────────
# Create the user, and give it sudo permission. All in one step to avoid cluttering layers
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Allow sudo for the user
RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set bash as the default shell (updated to brew bash after sync-brew)
RUN chsh -s /usr/bin/bash ${USERNAME}
ENV SHELL=/usr/bin/bash
ENV BREW_BASH=/home/linuxbrew/.linuxbrew/bin/bash

# Set the default user for the image, also used in the rest of steps.
USER $USERNAME

# ── copy repo ─────────────────────────────────────────────────────────────────
# The builder stage produced a shallow clone; .git is small but fetch/merge work.
WORKDIR /dotfiles
COPY --from=builder --chown=${USERNAME}:${USERNAME} /dotfiles .
RUN echo "${BUILD_DATE}" > /dotfiles/.build-date

# ── homebrew ──────────────────────────────────────────────────────────────────
RUN NONINTERACTIVE=1 /bin/bash -c \
    "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
ENV PATH="/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:${PATH}"

# ── install dotfiles ──────────────────────────────────────────────────────────
RUN python3 /dotfiles/scripts/deploy-dotfiles /dotfiles --apply

# ── sync brew packages ────────────────────────────────────────────────────────
RUN /dotfiles/scripts/sync-brew \
    && brew cleanup --prune=all \
    && rm -rf "$(brew --cache)"

# ── install neovim plugins ────────────────────────────────────────────────────
# First pass: install lazy.nvim plugins; strip .git dirs to save space
RUN nvim --headless "+Lazy! install" +qa \
    && find ~/.local/share/nvim/lazy -mindepth 1 -maxdepth 1 -type d \
       -exec rm -rf {}/.git \;
# Second pass: compile treesitter parsers (synchronous, waits for completion)
RUN nvim --headless -c "lua require('nvim-treesitter.install').update({ with_sync = true })()" -c "qa" \
    && find ~/.local/share/nvim/lazy/nvim-treesitter -name '*.c' -delete \
    && find ~/.local/share/nvim/lazy/nvim-treesitter -name '*.cc' -delete
# Third pass: let mason finish installing tools (shfmt, stylua, etc.)
RUN nvim --headless -c "lua vim.defer_fn(function() vim.cmd('qa!') end, 60000)" +qa \
    && rm -rf ~/.local/share/nvim/mason/packages/*/node_modules \
    && rm -rf ~/.local/share/nvim/mason/staging

# ── switch default shell to brew bash ─────────────────────────────────────────
RUN echo "${BREW_BASH}" | sudo tee -a /etc/shells \
    && sudo chsh -s "${BREW_BASH}" ${USERNAME}
ENV SHELL=${BREW_BASH}

WORKDIR /home/${USERNAME}

CMD ["sleep", "infinity"]
