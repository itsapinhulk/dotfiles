# syntax=docker/dockerfile:1
#
# Devcontainer image which includes basic linux configuration and this dotfiles repo.
#
# Build args injected by build-and-push.sh:
#   USERNAME   – username for the image and default user
#   REPO_URL   – https:// URL of the origin remote
#   GIT_SHA    – full commit SHA baked into the image
#   BUILD_DATE – YYYYMMDD-hhmm for the image tag


# ── base ──────────────────────────────────────────────────────────────────────
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
        git git-lfs sudo \
        ca-certificates \
        python3 \
    && rm -rf /var/lib/apt/lists/*

# ── user ───────────────────────────────────────────────────────────────────────
# Create the user, and give it sudo permission. All in one step to avoid cluttering layers
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Allow sudo for the user
RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set bash as the default shell
RUN chsh -s /usr/bin/bash ${USERNAME}

# Set the default user for the image, also used in the rest of steps.
USER $USERNAME

# ── copy repo ─────────────────────────────────────────────────────────────────
# The build context is the repository root.
# .dockerignore should exclude build artefacts, secrets, etc.
WORKDIR /dotfiles
COPY . .
RUN sudo chown -R ${USERNAME}:${USERNAME} /dotfiles \
    && git config core.autocrlf input \
    && git rm --cached -r . \
    && git reset --hard

# Rewrite the origin remote to the canonical https:// URL so that
# `git pull` / `git fetch` works from inside a running container.
# Stamp the exact commit so the image is self-describing at runtime.
# Only performed when REPO_URL is provided; skipped for local/manual builds.
RUN if [ -n "${REPO_URL}" ]; then git remote set-url origin "${REPO_URL}"; fi \
    && echo "${GIT_SHA}" > /dotfiles/.git-sha \
    && echo "${BUILD_DATE}" > /dotfiles/.build-date

# ── install dotfiles ──────────────────────────────────────────────────────────
RUN python3 /dotfiles/scripts/deploy-dotfiles /dotfiles --apply

CMD ["sleep", "infinity"]
