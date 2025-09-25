# Dockerfile
FROM docker.n8n.io/n8nio/n8n:latest

USER root

# 1) Install Python + pip (and certs)
RUN apk add --no-cache python3 py3-pip ca-certificates tzdata curl

# 2) Virtualenv for MCP servers
RUN python3 -m venv /opt/mcp-venv

# 3) Preinstall packages with wheels-only so no runtime compiles/downloads
#    - pydantic-core + pydantic explicitly (wheels pulled now)
#    - mcp-server-time (depends on pydantic)
RUN /opt/mcp-venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/mcp-venv/bin/pip install --no-cache-dir --only-binary=:all: \
    "pydantic-core" "pydantic" "mcp-server-time"

# 4) Smoke-check imports so build fails early if a wheel is missing
RUN /opt/mcp-venv/bin/python - <<'PY'
import pydantic_core, pydantic, mcp_server_time
print("OK: pydantic_core=", pydantic_core.__version__)
print("OK: pydantic=", pydantic.__version__)
PY

# 5) Wrapper on PATH so n8n can run `mcp-server-time`
RUN printf '#!/bin/sh\nexec /opt/mcp-venv/bin/mcp-server-time "$@"\n' \
    > /usr/local/bin/mcp-server-time \
    && chmod +x /usr/local/bin/mcp-server-time

# Install uv globally; no flags needed, just set UV_INSTALL_DIR
ENV UV_INSTALL_DIR=/usr/local/bin
ENV TZ=Asia/Taipei

RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && uv --version \
    && which uvx

USER node
