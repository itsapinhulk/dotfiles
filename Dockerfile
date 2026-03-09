# Devcontainer image which includes basic linux configuration and this dotfiles repo.
FROM ubuntu:24.04

# syntax=docker/dockerfile:1
#
# Build args injected by build-and-push.sh:
#   REPO_URL   – https:// URL of the origin remote
#   GIT_SHA    – full commit SHA baked into the image
#   BUILD_DATE – YYYYMMDD-hhmm for the image tag

ARG REPO_URL=""
ARG GIT_SHA="unknown"
ARG BUILD_DATE="unknown"

# ── base ──────────────────────────────────────────────────────────────────────
FROM ubuntu:24.04

ARG REPO_URL
ARG GIT_SHA
ARG BUILD_DATE

# Labels follow OCI image-spec conventions
LABEL org.opencontainers.image.revision="${GIT_SHA}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.source="${REPO_URL}"

# ── system deps ───────────────────────────────────────────────────────────────
RUN apt-get update && \
        apt-get install -y --no-install-recommends \
        git \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ── copy repo ─────────────────────────────────────────────────────────────────
# The build context is the repository root.
# .dockerignore should exclude build artefacts, secrets, etc.
WORKDIR /dotfiles
COPY . .

# Rewrite the origin remote to the canonical https:// URL so that
# `git pull` / `git fetch` works from inside a running container.
# Stamp the exact commit so the image is self-describing at runtime.
# Only performed when REPO_URL is provided; skipped for local/manual builds.
RUN if [ -n "${REPO_URL}" ]; then git remote set-url origin "${REPO_URL}"; fi \
    && echo "${GIT_SHA}" > /app/.git-sha \
    && echo "${BUILD_DATE}" > /app/.build-date

# ── default command ───────────────────────────────────────────────────────────
# Override in `docker run` or a child image.
CMD ["bash"]
