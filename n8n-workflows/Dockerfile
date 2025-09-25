# Dockerfile
FROM docker.n8n.io/n8nio/n8n:latest

USER root

# 1) Install Python + pip (and certs)
RUN apk add --no-cache python3 py3-pip ca-certificates tzdata curl

# 2) Create a virtualenv and install the time server into it
RUN python3 -m venv /opt/mcp-venv \
    && /opt/mcp-venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/mcp-venv/bin/pip install --no-cache-dir mcp-server-time

# 3) Expose a wrapper on PATH so n8n can run `mcp-server-time`
RUN printf '#!/bin/sh\nexec /opt/mcp-venv/bin/mcp-server-time "$@"\n' > /usr/local/bin/mcp-server-time \
    && chmod +x /usr/local/bin/mcp-server-time

# (optional) keep tzdata only if you need timezone DB at runtime
# RUN apk del tzdata

# Install uv globally; no flags needed, just set UV_INSTALL_DIR
ENV UV_INSTALL_DIR=/usr/local/bin
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && uv --version \
    && which uvx

USER node
