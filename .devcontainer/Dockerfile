FROM ubuntu:24.04

ARG USERNAME=devuser
ARG USER_UID=1111
ARG USER_GID=$USER_UID

# Create the user, and give it sudo permission. All in one step to avoid cluttering layers
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN apt update \
    && apt install -y sudo git git-lfs curl ca-certificates curl \
    && apt remove \
        $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc | cut -f1) \
    && rm -rf /var/lib/apt/lists/*

# Allow sudo for the user
RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set bash as the default shell
RUN chsh -s /usr/bin/bash devuser
ENV SHELL=/usr/bin/bash

# Install docker CLI
RUN install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc \
    && chmod a+r /etc/apt/keyrings/docker.asc \
    && tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

RUN apt update \
    && apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y \
    && rm -rf /var/lib/apt/lists/*

# Ensure workspace dir is owned correctly
RUN mkdir -p /repo && chown $USERNAME:$USERNAME /repo

# Set the default user for the image, also used in the rest of steps.
USER $USERNAME

# Install Claude Code
RUN curl -fsSL https://claude.ai/install.sh | bash
