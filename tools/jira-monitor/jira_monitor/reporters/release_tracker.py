"""
Workstream 2 — Release Candidate Tracker

For each configured project (MOBILE, ISD):
  - Fetches Jira versions (releases)
  - Filters to unreleased or recently released (last 30 days)
  - Produces a per-platform build status table
  - Surfaces issues still open against each release

Replaces: AUTO-88–94 manual candidate build notification tasks.
Publishes to: jira_monitor.confluence.release_tracker_page_id (global config)
"""

from datetime import date, datetime, timedelta

from ..client import AtlassianClient

ISSUE_FIELDS = ["summary", "status", "issuetype", "assignee", "priority"]
LOOKBACK_DAYS = 30


def run(client: AtlassianClient, config: dict) -> str:
    """Return a Markdown report string."""
    projects = config.get("jira", {}).get("projects", {})
    target_keys = [projects.get("mobile"), projects.get("isd")]
    target_keys = [k for k in target_keys if k]

    sections = []
    for project_key in target_keys:
        section = _report_project(client, project_key)
        if section:
            sections.append(section)

    if not sections:
        return "_No active or recent releases found._"

    return "\n\n---\n\n".join(sections)


def _report_project(client: AtlassianClient, project_key: str) -> str | None:
    try:
        versions = client.get_versions(project_key)
    except Exception as e:
        return f"### {project_key} Releases\n\n_Could not fetch versions: {e}_"

    cutoff = date.today() - timedelta(days=LOOKBACK_DAYS)
    relevant = []
    for v in versions:
        if not v.get("released", False):
            relevant.append(v)  # unreleased — always include
        else:
            release_date = v.get("releaseDate", "")
            if release_date and datetime.strptime(release_date, "%Y-%m-%d").date() >= cutoff:
                relevant.append(v)  # released within lookback window

    if not relevant:
        return None

    lines = [f"### {project_key} — Release Tracker"]
    lines.append("")
    lines.append("| Version | Status | Release Date | Open Issues | Description |")
    lines.append("|---------|--------|--------------|-------------|-------------|")

    for v in sorted(relevant, key=lambda x: x.get("releaseDate", "9999-99-99")):
        name         = v.get("name", "—")
        released     = v.get("released", False)
        status_emoji = "✅ Released" if released else "🔄 Unreleased"
        rel_date     = v.get("releaseDate", "TBD")
        description  = v.get("description", "—")[:60]

        # Count open issues against this version
        open_count = _count_open_issues(client, project_key, name)
        open_str   = str(open_count) if open_count is not None else "—"

        lines.append(f"| {name} | {status_emoji} | {rel_date} | {open_str} | {description} |")

    # Detail block: list open P1/P2 issues for unreleased versions
    blockers = _get_blockers(client, project_key, relevant)
    if blockers:
        lines.append("")
        lines.append("**Open blockers (P1/P2):**")
        for issue in blockers:
            priority = issue["fields"].get("priority", {}).get("name", "?")
            assignee = (issue["fields"].get("assignee") or {}).get("displayName", "Unassigned")
            lines.append(
                f"- [{issue['key']}] {issue['fields']['summary']} "
                f"— {priority} / {assignee}"
            )

    return "\n".join(lines)


def _count_open_issues(client: AtlassianClient, project_key: str, version_name: str) -> int | None:
    try:
        issues = client.search_issues(
            jql=(
                f'project = {project_key} '
                f'AND fixVersion = "{version_name}" '
                f'AND statusCategory != Done'
            ),
            fields=["summary"],
            max_results=1,
        )
        # search_issues paginates but we just need total — do a single call
        data = client.jira_get("search", {
            "jql":        f'project = {project_key} AND fixVersion = "{version_name}" AND statusCategory != Done',
            "maxResults": 0,
        })
        return data.get("total", 0)
    except Exception:
        return None


def _get_blockers(client: AtlassianClient, project_key: str, versions: list[dict]) -> list[dict]:
    unreleased_names = [v["name"] for v in versions if not v.get("released", False)]
    if not unreleased_names:
        return []

    version_jql = " OR ".join(f'fixVersion = "{n}"' for n in unreleased_names)
    try:
        return client.search_issues(
            jql=(
                f'project = {project_key} '
                f'AND ({version_jql}) '
                f'AND statusCategory != Done '
                f'AND priority in ("Highest", "High")'
            ),
            fields=ISSUE_FIELDS,
            max_results=20,
        )
    except Exception:
        return []
