FROM ubuntu:24.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    sudo \
    ca-certificates \
    gnupg \
    lsb-release \
    git \
    python3 \
    python3-pip \
    wget \
    ripgrep \
    tmux \
    && rm -rf /var/lib/apt/lists/*

# Add NodeSource Node 20 repository
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*


# Create a non-root user
RUN useradd -m -s /bin/bash agent && \
    echo "agent ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install claude code, gemini-cli, and Python packages system wide
RUN npm install -g @anthropic-ai/claude-code

RUN npm install -g @google/gemini-cli

RUN pip3 install --break-system-packages --upgrade aristotlelib python-dotenv leanclient

## Install elan in /opt (accessible to all users)
RUN curl https://elan.lean-lang.org/elan-init.sh -sSf | sh -s -- -y --default-toolchain leanprover/lean4:stable --no-modify-path
RUN mv /root/.elan /opt/elan
RUN sudo chown -R agent /opt/elan
RUN chmod -R 755 /opt/elan

# Set up environment for elan
ENV ELAN_HOME="/opt/elan"
ENV PATH="/opt/elan/bin:${PATH}"

RUN elan toolchain install leanprover/lean4:v4.26.0-rc1

RUN curl -LsSf https://astral.sh/uv/install.sh | UV_INSTALL_DIR=/usr/local/bin sh

USER agent 

# Set working directory
WORKDIR /workspace

CMD ["/bin/bash"]
