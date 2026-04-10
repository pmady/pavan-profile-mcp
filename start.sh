#!/bin/bash
# Production startup script for Render deployment
# This ensures uvicorn is configured correctly for reverse proxy

set -e

echo "Starting Pavan Profile MCP Server..."
echo "PORT: ${PORT:-10000}"
echo "Environment: Production (Render)"

# Run FastMCP with HTTP transport
# Uvicorn will use the environment variables for proxy configuration
exec uv run fastmcp run server.py \
  --transport http \
  --host 0.0.0.0 \
  --port "${PORT:-10000}" \
  --no-banner
