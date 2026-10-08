# ORANO MCP Server

A personal, read-only MCP (Model Context Protocol) server that lets a user's
own AI agent (ChatGPT, Claude, Cursor, Ollama) read their ORANO library as
grounded context.

> **Note:** This public repository contains documentation, the MCP server
> manifest, and a reference implementation. The production MCP server runs as
> an authenticated endpoint mounted at `/mcp` on the ORANO backend
> (FastAPI + Postgres + pgvector). See [the ORANO product
> site](https://oranoai.com/mcp) for the live endpoint and authentication flow.

## What is ORANO?

ORANO turns saved Reels, TikToks, YouTube Shorts, and reference material into
structured projects — summary, key takeaways, ordered tasks, research context,
and a learning roadmap. Live on the iOS App Store
([App Store listing](https://apps.apple.com/us/app/orano-ai/id6791454509)).

A personal, read-only MCP server so a user's own AI agent can read that
context is the differentiator.

## MCP tools exposed

The ORANO MCP server exposes the following tools:

| Tool | Description |
|---|---|
| `list_projects` | List the user's projects with optional status filters (`active`, `completed`, `skipped`, `archived`). |
| `get_project` | Return a single project's full structured understanding + summary + tasks + resources + research + roadmap. |
| `get_project_context` | Return only the requested context fields (`summary`, `overview`, `caption`, `transcript`, `visual_context`, `links`, `tasks`, `roadmap`, `source`, or `raw_source`) in structured, Markdown, or text output. |
| `search_library` | Search the user's projects by title, summary, source title, or URL. |
| `read_memory_facts` | Return curated memory facts (preferences, skills, goals) with confidence and freshness signals. |
| `get_pending_handoffs` | Retrieve projects explicitly sent from the ORANO app to a target agent. Each handoff is acknowledged once on read so concurrent polls do not duplicate. |

## Authentication

- **Mechanism:** Bearer personal API key, scope `orano:read`.
- **No OAuth.** Manual key creation only (per `landing/mcp-access.html`).
- **Per-user budget:** 240 calls per 60 minutes.
- **Maximum active keys per user:** 10.

## MCP server manifest (server.json)

The canonical MCP server manifest follows the [official MCP server.json
schema](https://modelcontextprotocol.io/docs/concepts/architecture#server-discovery):

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/server.json",
  "name": "io.github.infotik/orano-mcp-server",
  "displayName": "ORANO",
  "description": "Personal, read-only MCP server that exposes the user's ORANO library (projects, tasks, research, roadmaps, memory facts) as tools for their own AI agent.",
  "version": "0.1.0",
  "repository": {
    "type": "git",
    "url": "https://github.com/infotik/orano-mcp-server"
  },
  "homepage": "https://oranoai.com/mcp",
  "categories": [
    "knowledge-management",
    "personal-assistant",
    "productivity",
    "second-brain"
  ],
  "tools": [
    { "name": "list_projects", "description": "List the user's ORANO projects with optional status filters." },
    { "name": "get_project", "description": "Return a single project's full structured understanding." },
    { "name": "get_project_context", "description": "Return only the requested context fields (summary, overview, transcript, visual_context, links, tasks, roadmap, source, raw_source)." },
    { "name": "search_library", "description": "Search the user's projects by title, summary, source title, or URL." },
    { "name": "read_memory_facts", "description": "Return curated memory facts with confidence and freshness signals." },
    { "name": "get_pending_handoffs", "description": "Retrieve acknowledged-once projects explicitly sent from the ORANO app to a target agent." }
  ],
  "transports": [
    { "type": "http", "endpoint": "https://orano-ai-backend-1037939693300.us-central1.run.app/mcp/" }
  ],
  "authentication": {
    "type": "bearer",
    "scope": "orano:read",
    "user_specific": true,
    "rate_limit": "240 calls / 60 minutes / user"
  }
}
```

## Reference implementation (Python)

The production server runs as part of the ORANO backend (FastAPI + SQLAlchemy +
pgvector). The reference implementation pattern is:

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings
from mcp.server.auth.provider import AccessToken

mcp = FastMCP(
    name="orano",
    auth=AuthSettings(issuer_url="https://orano-ai-backend-1037939693300.us-central1.run.app", required_scopes=["orano:read"]),
)

@mcp.tool()
async def list_projects(status: str | None = None) -> list[dict]:
    """List the user's ORANO projects."""
    ...

@mcp.tool()
async def get_project(project_id: str, fields: list[str] | None = None) -> dict:
    """Return a single project's full structured understanding."""
    ...

# ... plus get_project_context, search_library, read_memory_facts,
# get_pending_handoffs
```

The full production server (787 lines + 290 lines of auth/handshake helpers)
lives in `ExecutionOSBackend/app/mcp_server.py` and is part of the private
ORANO backend repository. Open-sourcing the full production code requires
extracting the SQLAlchemy models + ingest services into a public package,
which is on the product roadmap but not yet complete.

## How to use

End users:

1. Install the ORANO iOS app from
   [the App Store](https://apps.apple.com/us/app/orano-ai/id6791454509).
2. Sign in, save at least one Reel/TikTok/YouTube Short to generate your
   first project.
3. Open Settings → MCP access → Create new key (scope `orano:read`).
4. Connect your AI agent (ChatGPT, Claude, Cursor, Ollama) to your personal
   MCP endpoint with the key as a bearer token.

## Privacy and trust

- The MCP server is **read-only**. It does not write to projects, sources,
  tasks, memory, or account data.
- The single state mutation is `get_pending_handoffs` acknowledging a queued
  app-triggered delivery by setting its delivery timestamp.
- No agent write access is promised; no one-click OAuth flow exists.

## License

MIT — see [LICENSE](./LICENSE).

## Links

- [Product site](https://oranoai.com/)
- [MCP overview](https://oranoai.com/mcp)
- [MCP access flow](https://oranoai.com/mcp-access.html)
- [App Store listing](https://apps.apple.com/us/app/orano-ai/id6791454509)
- [Deck](https://oranoai.com/deck/)
