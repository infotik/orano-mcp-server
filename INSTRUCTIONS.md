# Push instructions — read this first

This folder contains everything needed to create the public `github.com/infotik/orano-mcp-server` repo. Once published, you can immediately submit to:

- **Glama** at https://glama.ai/mcp/servers/submit
- **MCPFind** at https://mcpfind.org/submit (existing handoff: `growth/drafts/handoffs/2026-08-26-mcpfind-mcpso.md`)
- **MCP servers** at https://mcpservers.org/submit
- **mcp.so** at https://mcp.so/submit (paid $39 — declined per marketing plan; skip unless budget changes)

## Push to GitHub in 3 commands

From any terminal where the GitHub CLI is authenticated as `infotik`:

```bash
cd growth/drafts/orano-mcp-server-public
gh repo create infotik/orano-mcp-server --public --source=. --remote=origin --push --description "Personal, read-only MCP server for ORANO — exposes a user's library as tools for their own AI agent"
```

(Requires `gh auth login` first if not authenticated. Use the `infotik` GitHub account.)

If you prefer the manual UI:

1. Open https://github.com/organizations/infotik/repositories/new
2. Repository name: `orano-mcp-server`
3. Visibility: **Public**
4. **Do not** initialize with README, .gitignore, or license (the files are already here)
5. Click **Create repository**
6. Then in a terminal:

```bash
cd growth/drafts/orano-mcp-server-public
git init
git add .
git commit -m "Initial public MCP server manifest for ORANO"
git branch -M main
git remote add origin git@github.com:infotik/orano-mcp-server.git
git push -u origin main
```

## Submit to MCP listings (immediately after push)

### Glama

1. Open https://glama.ai/mcp/servers/submit
2. Fill the form:
   - **Server Name:** `ORANO MCP Server`
   - **GitHub Repository URL:** `https://github.com/infotik/orano-mcp-server`
   - **Package Name:** `@infotik/orano-mcp-server`
   - **Short Description:** "Personal, read-only MCP server that exposes a user's ORANO library as grounded context for any compatible AI agent. Live on iOS App Store."
   - **Package Type:** `npm`
   - **Category:** `Search & Knowledge`
3. Submit. Glama indexes immediately.

### MCPFind

1. Open https://mcpfind.org/submit
2. Fill the form:
   - **Server Name:** `ORANO MCP Server`
   - **GitHub Repository URL:** `https://github.com/infotik/orano-mcp-server`
   - **Package Name:** `@infotik/orano-mcp-server`
   - **Short Description:** "ORANO turns saved short-form video into structured notes, action items, and decisions on iOS. Ships a public MCP server so any AI agent can query the user's library directly."
   - **Package Type:** `npm`
   - **Category:** `Search & Knowledge`
3. Click **Open GitHub Editor** → MCPFind will prefill a YAML PR against the MCPFind repo. Submit the PR.

### MCP servers (mcpservers.org)

1. Open https://mcpservers.org/submit
2. Same fields as MCPFind.
3. Submit.

## Files in this folder

| File | Purpose |
|---|---|
| `README.md` | Repository README — describes the ORANO MCP server, tools, auth model, and links |
| `server.json` | Canonical MCP server manifest (per official schema) |
| `package.json` | npm package descriptor (for MCPFind/Glama submission) |
| `LICENSE` | MIT license |
| `INSTRUCTIONS.md` | This file — push + submission instructions |

## Why a manifest-only public repo?

The production MCP server code is part of the private ORANO backend
(`ExecutionOSBackend/app/mcp_server.py`, 787 lines, plus 290 lines of
auth/handshake helpers). It depends on internal SQLAlchemy models, ingest
services, and rate-limit helpers that aren't appropriate for an early public
release.

The `server.json` manifest in this repo is sufficient for MCPFind, Glama,
and MCP servers indexing. The production server still runs at
`https://api.oranoai.com/mcp/` for end users with personal API keys. A full
open-source extraction of the production server is on the product roadmap
but is out of scope for the initial launch.

## Verification after push

After `gh repo create ... --push` succeeds:

1. Open https://github.com/infotik/orano-mcp-server in a browser — README, server.json, package.json, LICENSE should all render.
2. Open https://glama.ai/mcp/servers?q=orano — the listing should appear within minutes.
3. Open https://mcpfind.org/ — search for ORANO; the indexed entry should appear after PR merge (typically 1–2 days).

## Estimated time

5 minutes total:
- 2 min: `gh repo create` (or manual UI)
- 3 min: Glama + MCPFind submissions (paste from this file)
