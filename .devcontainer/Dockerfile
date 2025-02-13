FROM inkywhat-dsp/core

RUN --mount=type=cache,target=/var/cache/apt \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    vim \
    htop \
    zsh \
    sudo \
    openssh-client \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/tmp/* /var/lib/apt/lists/*

WORKDIR /tmp

COPY .devcontainer/requirements.txt .
RUN --mount=type=cache,target=/root/.cache \
    uv pip install -r requirements.txt --system

RUN rm -rf /tmp/*

ENV SHELL=/usr/bin/zsh
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
