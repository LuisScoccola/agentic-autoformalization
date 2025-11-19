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


# Install Claude Code and Python packages system wide
RUN npm install -g @anthropic-ai/claude-code

RUN pip3 install --break-system-packages aristotlelib python-dotenv

# Install elan in /opt (accessible to all users)
RUN curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain leanprover/lean4:stable --no-modify-path
RUN mv /root/.elan /opt/elan && chmod -R 755 /opt/elan

# Set up environment for elan
ENV ELAN_HOME="/opt/elan"
ENV PATH="/opt/elan/bin:${PATH}"

# Verify Lean installation
RUN lean --version && lake --version

# Add elan to claude user's PATH in .bashrc
RUN echo 'export ELAN_HOME="/opt/elan"' >> /home/claude/.bashrc && \
    echo 'export PATH="/opt/elan/bin:$PATH"' >> /home/claude/.bashrc

USER claude


# Set working directory
WORKDIR /workspace

CMD ["/bin/bash"]
