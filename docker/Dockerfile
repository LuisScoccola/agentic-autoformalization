FROM ubuntu:24.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    nodejs \
    npm \
    wget \
    ripgrep \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -s /bin/bash claude && \
    echo "claude ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install Claude Code and Python packages system wide
RUN npm install -g @anthropic-ai/claude-code

RUN pip3 install --break-system-packages aristotlelib python-dotenv leanclient

## Install elan in /opt (accessible to all users)
RUN curl https://elan.lean-lang.org/elan-init.sh -sSf | sh -s -- -y --default-toolchain leanprover/lean4:stable --no-modify-path
RUN mv /root/.elan /opt/elan
RUN sudo chown -R claude /opt/elan
RUN chmod -R 755 /opt/elan

# Set up environment for elan
ENV ELAN_HOME="/opt/elan"
ENV PATH="/opt/elan/bin:${PATH}"

RUN elan toolchain install leanprover/lean4:v4.26.0-rc1

RUN curl -LsSf https://astral.sh/uv/install.sh | UV_INSTALL_DIR=/usr/local/bin sh

USER claude

# Set working directory
WORKDIR /workspace

CMD ["/bin/bash"]
