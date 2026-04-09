FROM python:3.11-slim

WORKDIR /app

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml .
COPY README.md .
COPY server.py .
COPY data/ data/

# Install dependencies
RUN uv pip install --system -e .

# Render sets PORT automatically; default to 10000
ENV PORT=10000

# Configure uvicorn to trust proxy headers (Render's load balancer)
ENV UVICORN_PROXY_HEADERS=1
ENV UVICORN_FORWARDED_ALLOW_IPS=*

EXPOSE 10000

# Use FastMCP CLI with HTTP transport
# The environment variables above configure uvicorn to trust Render's proxy
CMD ["sh", "-c", "uv run fastmcp run server.py --transport http --host 0.0.0.0 --port ${PORT}"]
