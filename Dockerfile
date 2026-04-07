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

# Railway/Render set PORT automatically; default to 8000
ENV PORT=8000

EXPOSE 8000

# Use FastMCP CLI to run with HTTP transport
# --forwarded-allow-ips='*' trusts Railway's proxy headers
CMD ["sh", "-c", "uv run fastmcp run server.py --transport http --host 0.0.0.0 --port ${PORT} --forwarded-allow-ips '*'"]
