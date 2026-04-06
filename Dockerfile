FROM python:3.11-slim

WORKDIR /app

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml .
COPY server.py .
COPY data/ data/

# Install dependencies
RUN uv pip install --system -e .

# Railway/Render set PORT automatically; default to 8000
ENV MCP_TRANSPORT=sse
ENV PORT=8000

EXPOSE 8000

CMD ["python", "server.py"]
