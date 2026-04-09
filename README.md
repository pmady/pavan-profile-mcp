# Pavan Madduri — Personal Knowledge MCP Server

[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blue?style=for-the-badge)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

A **Model Context Protocol (MCP) server** that exposes my professional profile — certifications, industry articles, open source contributions, and live GitHub activity — as a queryable API for AI agents.

> **Why?** Instead of a static resume, this is a **Personal Knowledge API**. Any AI agent (Claude, Gemini, Copilot) can query my career data in real-time. This is AI infrastructure, not just AI usage.

---

## What's Inside

### Resources (Static Data)

| Resource URI | Description |
|---|---|
| `profile://about` | Bio, links, expertise areas |
| `profile://certifications` | CNCF Golden Kubestronaut (all 15 certs + LFCS) |
| `profile://articles` | 9 industry articles (CNCF Blog, IEEE ComSoc, CloudNativeNow, PlatformEngineering.com, d7y.io) |
| `profile://open-source-summary` | 26 PRs across 15 projects |
| `profile://contributions/cncf` | Detailed CNCF project PRs |
| `profile://contributions/aswf` | Detailed ASWF project PRs |

### Tools (Dynamic Functions)

| Tool | Description |
|---|---|
| `search_contributions(project)` | Search contributions by project name |
| `search_articles(keyword)` | Search industry articles by keyword, category, or publication |
| `get_expertise(domain)` | Check expertise in a technical domain |
| `get_eb1a_evidence(criterion)` | Retrieve EB-1A extraordinary ability evidence |
| `get_github_activity(repo, limit)` | Live GitHub PR data via API |
| `get_github_stats()` | Live GitHub profile statistics |
| `get_profile_summary()` | One-page comprehensive summary |

---

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Install & Run

```bash
# Clone
git clone https://github.com/pmady/pavan-profile-mcp.git
cd pavan-profile-mcp

# Option A: uv (recommended)
uv sync
uv run server.py

# Option B: pip
pip install -e .
python server.py
```

### Environment Variables (Optional)

```bash
# For higher GitHub API rate limits (optional — works without it)
export GITHUB_TOKEN="ghp_your_token_here"
```

---

## Connect to Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pavan_profile": {
      "command": "uv",
      "args": ["--directory", "/path/to/pavan-profile-mcp", "run", "server.py"]
    }
  }
}
```

Restart Claude Desktop. You'll see the tools appear in the MCP panel.

### Example Prompts

- *"What are Pavan's contributions to Dragonfly?"*
- *"Show me his published articles on AI infrastructure"*
- *"What EB-1A evidence does Pavan have for original contributions?"*
- *"Get his latest GitHub activity"*
- *"Does he have expertise in GPU scheduling?"*

---

## Connect to Other Clients

### Cursor / Windsurf

Add to your MCP config:

```json
{
  "pavan_profile": {
    "command": "uv",
    "args": ["--directory", "/path/to/pavan-profile-mcp", "run", "server.py"]
  }
}
```

### Render (Public Hosting)

**One-Click Deploy**: [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/pmady/pavan-profile-mcp)

This server deploys on [Render](https://render.com) with HTTP transport for remote access.

**Live Production Server**: `https://pavan-profile-mcp.onrender.com/mcp`

Connect any MCP client to the remote endpoint:

```json
{
  "mcpServers": {
    "pavan_profile": {
      "url": "https://pavan-profile-mcp.onrender.com/mcp"
    }
  }
}
```

**Manual deployment:**
1. Fork this repo
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New" → "Blueprint"
4. Connect your forked repo
5. Render auto-detects `render.yaml` and deploys
6. Your MCP endpoint will be at `https://<your-service-name>.onrender.com/mcp`

---

## Architecture

```
AI Agent (Claude / Gemini / Copilot)
        │
        ▼
┌─────────────────────────────┐
│   MCP Protocol (stdio/SSE)   │
├─────────────────────────────┤
│   FastMCP Server            │
│                             │
│   Resources:                │
│   ├── profile://about       │
│   ├── profile://certs       │
│   ├── profile://articles    │
│   └── profile://oss-summary │
│                             │
│   Tools:                    │
│   ├── search_contributions  │
│   ├── search_articles       │
│   ├── get_expertise         │
│   ├── get_eb1a_evidence     │
│   ├── get_github_activity ──┼──► GitHub API (live)
│   ├── get_github_stats    ──┼──► GitHub API (live)
│   └── get_profile_summary   │
│                             │
│   Data: data/profile.json   │
└─────────────────────────────┘
```

---

## Project Structure

```
pavan-profile-mcp/
├── server.py              # MCP server — all resources and tools
├── data/
│   └── profile.json       # Structured profile data (certs, articles, PRs)
├── Dockerfile             # Railway/Render deployment
├── pyproject.toml         # Python project config
├── SKILL.md               # Smithery skill definition
├── smithery.yaml          # Smithery.ai config
├── claude_desktop_config.example.json
├── README.md
└── LICENSE
```

---

## About the Author

**Pavan Madduri** — Senior DevOps/Platform Engineer

- **CNCF Golden Kubestronaut** (all 15 CNCF certifications + LFCS)
- **Published author** on CNCF Blog, IEEE ComSoc, CloudNativeNow, PlatformEngineering.com
- **26 PRs** across **15 CNCF & ASWF projects** (Dragonfly, Volcano, KEDA, Kubernetes, TiKV, OpenColorIO, and more)
- **Dragonfly Community Member** (CNCF Incubating)

[GitHub](https://github.com/pmady) · [LinkedIn](https://www.linkedin.com/in/pavanmadduri/) · [Blog](https://pavanmadduri.wordpress.com/)

---

## License

MIT
