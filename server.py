"""
Pavan Madduri — Personal Knowledge MCP Server

A Model Context Protocol server that exposes professional profile data
(certifications, industry articles, open source contributions, GitHub activity)
as queryable Resources and Tools for AI agents.

Author: Pavan Madduri (https://github.com/pmady)
"""

import json
import os
from pathlib import Path
from typing import Optional

import httpx
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Initialise server
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "Pavan-Madduri-Profile",
    instructions=(
        "Personal Knowledge API for Pavan Madduri — Senior DevOps/Platform Engineer, "
        "CNCF Golden Kubestronaut, published author on CNCF Blog, IEEE ComSoc, "
        "CloudNativeNow & PlatformEngineering.com, and open source contributor "
        "across 15+ CNCF & ASWF projects. Query certifications, articles, contributions, "
        "and live GitHub activity."
    ),
)

# ---------------------------------------------------------------------------
# Load profile data
# ---------------------------------------------------------------------------
DATA_DIR = Path(__file__).parent / "data"


def _load_profile() -> dict:
    with open(DATA_DIR / "profile.json", "r") as f:
        return json.load(f)


PROFILE = _load_profile()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_USERNAME = "pmady"

# ---------------------------------------------------------------------------
# RESOURCES — static, structured data an agent can read directly
# ---------------------------------------------------------------------------


@mcp.resource("profile://about")
def get_about() -> str:
    """Returns a summary bio for Pavan Madduri."""
    p = PROFILE
    return json.dumps(
        {
            "name": p["name"],
            "title": p["title"],
            "summary": p["summary"],
            "links": p["links"],
            "cloud_platforms": p["cloud_platforms"],
            "expertise_areas": p["expertise_areas"],
        },
        indent=2,
    )


@mcp.resource("profile://certifications")
def get_certifications() -> str:
    """Returns Pavan's verified certifications including CNCF Golden Kubestronaut status (all 15 certs + LFCS)."""
    return json.dumps(PROFILE["certifications"], indent=2)


@mcp.resource("profile://articles")
def get_articles() -> str:
    """Returns all 9 published industry articles on CNCF Blog, IEEE ComSoc, CloudNativeNow, PlatformEngineering.com, and d7y.io."""
    return json.dumps(PROFILE["articles"], indent=2)


@mcp.resource("profile://open-source-summary")
def get_oss_summary() -> str:
    """Returns a high-level summary of open source contributions (26 PRs, 15 projects, 2 foundations)."""
    oss = PROFILE["open_source_contributions"]
    return json.dumps(
        {
            "total_prs": oss["total_prs"],
            "total_projects": oss["total_projects"],
            "foundations": oss["foundations"],
            "community_roles": oss["community_roles"],
            "personal_projects": oss["personal_projects"],
        },
        indent=2,
    )


@mcp.resource("profile://contributions/cncf")
def get_cncf_contributions() -> str:
    """Returns detailed CNCF project contributions with PR links."""
    return json.dumps(
        PROFILE["open_source_contributions"]["cncf_projects"], indent=2
    )


@mcp.resource("profile://contributions/aswf")
def get_aswf_contributions() -> str:
    """Returns detailed ASWF (Academy Software Foundation) project contributions."""
    return json.dumps(
        PROFILE["open_source_contributions"]["aswf_projects"], indent=2
    )


# ---------------------------------------------------------------------------
# TOOLS — dynamic, parameterised functions an agent can invoke
# ---------------------------------------------------------------------------


@mcp.tool()
def search_contributions(project: str) -> str:
    """Search Pavan's open source contributions by project name.

    Args:
        project: Project name to search for (e.g. 'dragonfly', 'volcano', 'keda',
                 'opencolorio', 'kubernetes', 'tikv', 'opencue', etc.)
    """
    query = project.lower().strip()
    results = []

    for proj in PROFILE["open_source_contributions"]["cncf_projects"]:
        if query in proj["name"].lower():
            results.append(proj)
    for proj in PROFILE["open_source_contributions"]["aswf_projects"]:
        if query in proj["name"].lower():
            results.append(proj)
    for proj in PROFILE["open_source_contributions"]["personal_projects"]:
        if query in proj["name"].lower():
            results.append(proj)

    if not results:
        return f"No contributions found for project matching '{project}'. Try: dragonfly, volcano, keda, opencolorio, kubernetes, tikv, opencue, openimageio, rawtoaces, xstudio, kpt, metal3, opentelemetry."

    return json.dumps(results, indent=2)


@mcp.tool()
def search_articles(keyword: str) -> str:
    """Search Pavan's published industry articles by keyword, category, or publication.

    Args:
        keyword: Keyword to search in article titles, categories, or publications
                 (e.g. 'AI', 'kubernetes', 'gitops', 'SRE', 'platform', 'argocd',
                  'zero-trust', 'dragonfly', 'CNCF', 'IEEE')
    """
    query = keyword.lower().strip()
    matches = [
        a
        for a in PROFILE["articles"]
        if query in a["title"].lower()
        or query in a["category"].lower()
        or query in a["publication"].lower()
    ]
    if not matches:
        return f"No articles found matching '{keyword}'. Publications: CNCF Blog, IEEE ComSoc, CloudNativeNow, PlatformEngineering.com, d7y.io. Categories: AI/ML Infrastructure, AI & Telecom, SRE & Self-Healing Infrastructure, Kubernetes & Cloud Infrastructure, Cloud-Native Security, Platform Engineering & GitOps."
    return json.dumps(matches, indent=2)


@mcp.tool()
def get_expertise(domain: str) -> str:
    """Check if Pavan has expertise in a specific technical domain.

    Args:
        domain: Technical domain to check (e.g. 'GPU', 'kubernetes', 'gitops',
                'observability', 'security', 'AI', 'platform engineering')
    """
    query = domain.lower().strip()
    matched = [e for e in PROFILE["expertise_areas"] if query in e.lower()]
    if not matched:
        return f"No direct expertise match for '{domain}'. Full list: {', '.join(PROFILE['expertise_areas'])}"
    return json.dumps(
        {"domain": domain, "matched_expertise": matched, "has_expertise": True},
        indent=2,
    )


@mcp.tool()
def get_eb1a_evidence(criterion: str) -> str:
    """Retrieve evidence supporting a specific EB-1A extraordinary ability criterion.

    Args:
        criterion: EB-1A criterion — one of: 'original_contribution',
                   'authorship', 'judging', 'membership', 'published_material',
                   'leading_role', 'high_salary', 'all'
    """
    evidence: dict[str, dict] = {
        "original_contribution": {
            "criterion": "Original contributions of major significance",
            "evidence": [
                "GPU NUMA topology-aware scheduling merged into Volcano (CNCF Incubating) — enables AI/HPC workloads to leverage hardware topology",
                "Hugging Face (hf://) and ModelScope protocol support merged into Dragonfly (CNCF Incubating) — P2P-accelerated AI model distribution",
                "KEDA GPU Scaler — open source external gRPC scaler for GPU/AI inference autoscaling",
                "KubeAI Autoscaler — Kubernetes-native AI inference workload autoscaler",
                "Ingress2Gateway — tool to convert Kubernetes Ingress to Gateway API",
                "Vulkan unit test framework for OpenColorIO (ASWF)",
            ],
        },
        "authorship": {
            "criterion": "Authorship of scholarly articles / published material in professional publications",
            "evidence": [
                f"{len(PROFILE['articles'])} published articles across top industry publications",
                "Published on CNCF Blog (official Cloud Native Computing Foundation blog)",
                "Published on IEEE ComSoc Technology Blog (Institute of Electrical and Electronics Engineers)",
                "Published on CloudNativeNow — leading cloud-native industry publication",
                "Published on PlatformEngineering.com — the platform engineering community hub",
                "Published on d7y.io — official Dragonfly (CNCF Incubating) project blog",
                "Topics span: AI model distribution, agentic AI in telecom, self-healing Kubernetes, ArgoCD drift prevention, zero-trust security, platform engineering",
            ],
        },
        "membership": {
            "criterion": "Membership in associations requiring outstanding achievements",
            "evidence": [
                "CNCF Golden Kubestronaut — achieved all 15 CNCF cloud-native certifications plus LFCS",
                "Dragonfly Community Member (CNCF Incubating) — achieved via community vote, March 2026",
                "Active contributor across CNCF and ASWF foundations (15+ projects)",
            ],
        },
        "judging": {
            "criterion": "Judging the work of others",
            "evidence": [
                "Code reviewer for Dragonfly (CNCF Incubating project)",
                "Technical reviewer for Volcano GPU scheduling PRs",
                "KEDA architectural analysis for GPU scaler design (#7538)",
            ],
        },
        "published_material": {
            "criterion": "Published material about the alien in professional publications",
            "evidence": [
                "CNCF Blog — 'Peer-to-Peer Acceleration for AI Model Distribution with Dragonfly' (official CNCF publication)",
                "IEEE ComSoc Technology Blog — 'The Financial Trap of Autonomous Networks: Scaling Agentic AI in the Telecom Core'",
                "CloudNativeNow — 4 articles on self-healing Kubernetes, ArgoCD, zero-trust, and Kubernetes v1.35",
                "PlatformEngineering.com — 2 articles on ArgoCD v3 and Internal Developer Platforms",
                "d7y.io (official Dragonfly project blog) — P2P-accelerated AI model downloads",
                "Technical documentation merged into Kubernetes, Dragonfly, and OpenColorIO",
            ],
        },
        "leading_role": {
            "criterion": "Leading or critical role in distinguished organizations",
            "evidence": [
                "Community Member of Dragonfly (CNCF Incubating, backed by Ant Group & Alibaba Cloud)",
                "On track to Approver/Maintainer role — owning AI/ML model distribution area",
                "Creator and maintainer of keda-gpu-scaler, kubeai-autoscaler, ingress2gateway",
            ],
        },
    }

    c = criterion.lower().strip()
    if c == "all":
        return json.dumps(evidence, indent=2)
    if c in evidence:
        return json.dumps(evidence[c], indent=2)
    return f"Unknown criterion '{criterion}'. Valid: {', '.join(list(evidence.keys()) + ['all'])}"


@mcp.tool()
async def get_github_activity(repo: Optional[str] = None, limit: int = 10) -> str:
    """Fetch Pavan's latest GitHub pull requests (live from GitHub API).

    Args:
        repo: Optional GitHub repo in 'owner/repo' format (e.g. 'dragonflyoss/client').
              If omitted, fetches recent activity across all tracked repos.
        limit: Max number of PRs to return (default 10, max 30).
    """
    limit = min(limit, 30)
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    async with httpx.AsyncClient(timeout=15.0) as client:
        if repo:
            # Fetch PRs for a specific repo
            url = f"https://api.github.com/repos/{repo}/pulls"
            params = {"state": "all", "per_page": limit}
            resp = await client.get(url, headers=headers, params=params)
            if resp.status_code != 200:
                return f"GitHub API error ({resp.status_code}): {resp.text[:200]}"
            all_prs = resp.json()
            prs = [pr for pr in all_prs if pr.get("user", {}).get("login") == GITHUB_USERNAME]
        else:
            # Search across all repos
            query = f"author:{GITHUB_USERNAME} type:pr"
            url = "https://api.github.com/search/issues"
            params = {"q": query, "sort": "updated", "order": "desc", "per_page": limit}
            resp = await client.get(url, headers=headers, params=params)
            if resp.status_code != 200:
                return f"GitHub API error ({resp.status_code}): {resp.text[:200]}"
            prs = resp.json().get("items", [])

    results = []
    for pr in prs[:limit]:
        results.append(
            {
                "title": pr.get("title"),
                "url": pr.get("html_url") or pr.get("pull_request", {}).get("html_url"),
                "state": pr.get("state"),
                "created_at": pr.get("created_at"),
                "updated_at": pr.get("updated_at"),
                "repo": pr.get("repository_url", "").replace("https://api.github.com/repos/", "")
                if "repository_url" in pr
                else repo,
            }
        )
    if not results:
        return f"No PRs found for {GITHUB_USERNAME}" + (f" in {repo}" if repo else "") + "."
    return json.dumps(results, indent=2)


@mcp.tool()
async def get_github_stats() -> str:
    """Fetch Pavan's live GitHub profile statistics (repos, followers, contributions)."""
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(
            f"https://api.github.com/users/{GITHUB_USERNAME}", headers=headers
        )
        if resp.status_code != 200:
            return f"GitHub API error ({resp.status_code}): {resp.text[:200]}"
        user = resp.json()

    return json.dumps(
        {
            "username": user.get("login"),
            "name": user.get("name"),
            "bio": user.get("bio"),
            "public_repos": user.get("public_repos"),
            "followers": user.get("followers"),
            "following": user.get("following"),
            "created_at": user.get("created_at"),
            "profile_url": user.get("html_url"),
        },
        indent=2,
    )


@mcp.tool()
def get_profile_summary() -> str:
    """Get a comprehensive one-page summary of Pavan Madduri's professional profile.
    Ideal for AI agents that need a quick overview."""
    p = PROFILE
    oss = p["open_source_contributions"]
    return json.dumps(
        {
            "name": p["name"],
            "title": p["title"],
            "summary": p["summary"],
            "certifications_count": len(p["certifications"]),
            "highlight_cert": "CNCF Golden Kubestronaut — all 15 CNCF certifications + LFCS",
            "articles_count": len(p["articles"]),
            "publications": list(
                set(a["publication"] for a in p["articles"])
            ),
            "open_source": {
                "total_prs": oss["total_prs"],
                "total_projects": oss["total_projects"],
                "foundations": oss["foundations"],
                "community_roles": oss["community_roles"],
                "key_projects": [
                    proj["name"] for proj in oss["cncf_projects"]
                ]
                + [proj["name"] for proj in oss["aswf_projects"]],
                "personal_projects": [
                    proj["name"] for proj in oss["personal_projects"]
                ],
            },
            "expertise": p["expertise_areas"],
            "links": p["links"],
        },
        indent=2,
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()
