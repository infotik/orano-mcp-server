"""Reference implementation of the ORANO MCP server.

This is a minimal but functional MCP server that exposes the six ORANO
read-only tools to any compatible AI agent. The production server runs
at https://api.oranoai.com/mcp/ as part of the ORANO FastAPI backend;
this reference exists so the Glama.ai runner (and any other Docker-based
MCP playground) can spin up a working server for testing/listing.

Tools exposed:
  - list_projects(status)
  - get_project(project_id, fields)
  - get_project_context(project_id, fields, format)
  - search_library(query, limit)
  - read_memory_facts(kind)
  - get_pending_handoffs(limit)
"""

import os
import json
from datetime import datetime, UTC
from typing import Any

from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount
import uvicorn

# Server identity (matches official MCP registry server.json)
SERVER_NAME = "orano"
SERVER_VERSION = "0.1.0"
REQUIRED_SCOPE = "orano:read"

mcp = FastMCP(name=SERVER_NAME, version=SERVER_VERSION)


# --- Reference data (in production: read from Postgres + pgvector) ---
_PROJECTS = [
    {
        "id": "demo-1",
        "title": "Reel: How to use Notion for PKM",
        "summary": "Walkthrough of Notion as a personal knowledge management tool.",
        "key_points": ["Databases as tables", "Linked databases", "Templates for notes"],
        "status": "active",
        "created_at": "2026-08-15T10:00:00Z",
    },
    {
        "id": "demo-2",
        "title": "TikTok: 3-minute cold brew recipe",
        "summary": "Step-by-step cold brew with kitchen staples.",
        "key_points": ["Coarse grind", "12-hour steep", "Filter through paper"],
        "status": "completed",
        "created_at": "2026-08-20T14:30:00Z",
    },
]

_MEMORY_FACTS = [
    {"kind": "preference", "subject": "favorite-coffee", "value": "cold-brew", "confidence": 0.9},
    {"kind": "goal", "subject": "ship-orano-mcp", "value": "v1.0", "confidence": 0.7},
]


def _check_auth(headers: dict[str, str] | None) -> None:
    """Validate the bearer API key. In production this calls the ORANO
    auth service. The reference raises on missing/invalid key."""
    if not headers:
        return  # FastMCP wraps this transparently in HTTP transport
    auth = headers.get("authorization", "")
    if not auth.startswith("Bearer "):
        raise PermissionError("Missing bearer token")
    # Real implementation: verify against the ORANO API key service.
    # The reference accepts any non-empty key for local testing.


@mcp.tool()
def list_projects(status: str | None = None) -> list[dict[str, Any]]:
    """List the user's ORANO projects with optional status filter."""
    items = _PROJECTS
    if status:
        items = [p for p in items if p["status"] == status]
    return items


@mcp.tool()
def get_project(project_id: str) -> dict[str, Any]:
    """Return a single project's full structured understanding."""
    for p in _PROJECTS:
        if p["id"] == project_id:
            return p
    return {"error": "not_found", "project_id": project_id}


@mcp.tool()
def get_project_context(project_id: str, fields: list[str] | None = None) -> dict[str, Any]:
    """Return only the requested context fields for a project."""
    project = get_project(project_id)
    if "error" in project:
        return project
    if not fields:
        return project
    return {k: v for k, v in project.items() if k in fields}


@mcp.tool()
def search_library(query: str, limit: int = 10) -> list[dict[str, Any]]:
    """Search the user's projects by title, summary, or source title."""
    q = query.lower()
    results = [p for p in _PROJECTS if q in p["title"].lower() or q in p["summary"].lower()]
    return results[:limit]


@mcp.tool()
def read_memory_facts(kind: str | None = None) -> list[dict[str, Any]]:
    """Return curated memory facts with optional kind filter."""
    if kind:
        return [f for f in _MEMORY_FACTS if f["kind"] == kind]
    return _MEMORY_FACTS


@mcp.tool()
def get_pending_handoffs(limit: int = 5) -> list[dict[str, Any]]:
    """Retrieve projects explicitly sent from the ORANO app to this agent.
    Each handoff is acknowledged once on read."""
    return [
        {
            "handoff_id": "h-001",
            "project_id": "demo-1",
            "delivered_at": datetime.now(UTC).isoformat(),
            "acknowledged": False,
        }
    ][:limit]


# --- HTTP transport wrapper ---
async def healthz(request):
    return JSONResponse({"status": "ok", "server": SERVER_NAME, "version": SERVER_VERSION})


app = Starlette(
    routes=[
        Mount("/mcp", app=mcp.streamable_http_app()),
        Mount("/healthz", app=healthz),
    ]
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
