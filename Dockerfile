# Reference Dockerfile for the ORANO MCP server.
#
# Glama.ai's automated check requires every MCP server to ship with a
# Dockerfile that the Glama runner can build and introspect. This file
# implements the production ORANO MCP server: an HTTP server on port 8000
# mounted at /mcp that authenticates clients with a bearer personal API key
# (scope `orano:read`) and exposes the six read-only tools.
#
# This Dockerfile is the reference implementation; the actual production
# server runs as part of the ORANO FastAPI backend at
# https://api.oranoai.com/mcp/ and uses the same tool surface.

FROM python:3.12-slim

WORKDIR /app

# Install the MCP SDK and a minimal ASGI stack
RUN pip install --no-cache-dir \
    mcp[server]>=1.0.0 \
    starlette>=0.36.0 \
    uvicorn>=0.27.0 \
    pydantic>=2.0.0

# Copy the reference server implementation
COPY reference_server.py /app/reference_server.py

# Expose the MCP server port
EXPOSE 8000

# Health check — Glama's runner uses this to verify the container started
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz', timeout=2).read()" || exit 1

# Start the MCP server
CMD ["python", "reference_server.py"]
