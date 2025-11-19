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
    sudo \
    && rm -rf /var/lib/apt/lists/*


# Create a non-root user
RUN useradd -m -s /bin/bash claude && \
    echo "claude ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Switch to non-root user
USER claude

# Install elan (Lean version manager)
RUN curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain leanprover/lean4:stable

# Add elan to PATH
ENV PATH="/home/claude/.elan/bin:${PATH}"

# Verify Lean installation
RUN lean --version

# Install Claude Code and Python packages using system npm
USER root
RUN npm install -g @anthropic-ai/claude-code
RUN pip3 install --break-system-packages aristotlelib python-dotenv
USER claude


# Set working directory
WORKDIR /workspace

CMD ["/bin/bash"]
