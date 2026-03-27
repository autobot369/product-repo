"""
Workstream 3 — Demand Review Digest

For each configured project:
  - Fetches all epics in Discover / Backlog / Ready for Review
  - Flags stale items (no update in > stale_epic_days)
  - Ranks agenda: unblocked new → stale → recently updated
  - Surfaces unassigned epics needing an owner

Replaces: AUTO-130 manual Demand Review epic and its child tasks.
Publishes to: jira_monitor.confluence.demand_review_page_id (global config)
"""

from datetime import datetime, timedelta, timezone

from ..client import AtlassianClient

FIELDS = ["summary", "status", "assignee", "priority", "created", "updated", "description", "labels"]

DEMAND_STATUSES = {
    "discover", "backlog", "ready for review", "to do", "open", "new",
}


def run(client: AtlassianClient, config: dict) -> str:
    """Return a Markdown report string."""
    projects = config.get("jira", {}).get("projects", {})
    target_keys = [projects.get("isd"), projects.get("auto"), projects.get("oip")]
    target_keys = [k for k in target_keys if k]

    stale_days = config.get("stale_epic_days", 60)
    all_epics  = []

    for project_key in target_keys:
        epics = _fetch_demand_epics(client, project_key)
        for e in epics:
            e["_project"] = project_key
        all_epics.extend(epics)

    if not all_epics:
        return "_No epics in demand review pipeline._"

    return _build_report(all_epics, stale_days)


def _fetch_demand_epics(client: AtlassianClient, project_key: str) -> list[dict]:
    status_jql = " OR ".join(f'status = "{s}"' for s in DEMAND_STATUSES)
    try:
        return client.search_issues(
            jql=f'project = {project_key} AND issuetype = Epic AND ({status_jql}) ORDER BY updated DESC',
            fields=FIELDS,
            max_results=100,
        )
    except Exception as e:
        print(f"  Warning: could not fetch epics for {project_key}: {e}")
        return []


def _build_report(epics: list[dict], stale_days: int) -> str:
    now   = datetime.now(timezone.utc)
    stale_cutoff = now - timedelta(days=stale_days)

    stale, unassigned, active = [], [], []

    for e in epics:
        updated_str = e["fields"].get("updated", "")
        updated     = _parse_dt(updated_str)
        assignee    = e["fields"].get("assignee")
        is_stale    = updated is not None and updated < stale_cutoff
        is_unassigned = assignee is None

        if is_stale:
            stale.append(e)
        elif is_unassigned:
            unassigned.append(e)
        else:
            active.append(e)

    lines = [
        f"### Demand Review Digest",
        f"",
        f"**{len(epics)} epics** in demand pipeline across {len({e['_project'] for e in epics})} projects.",
        f"Stale (>{stale_days}d no update): **{len(stale)}** · "
        f"Unassigned: **{len(unassigned)}** · "
        f"Active: **{len(active)}**",
        "",
    ]

    if unassigned:
        lines.append("#### 🔴 Needs Owner")
        lines.append("")
        lines.append("| Key | Summary | Project | Created |")
        lines.append("|-----|---------|---------|---------|")
        for e in sorted(unassigned, key=lambda x: x["fields"].get("created", ""), reverse=True):
            created = e["fields"].get("created", "")[:10]
            lines.append(
                f"| {e['key']} | {e['fields']['summary'][:60]} "
                f"| {e['_project']} | {created} |"
            )
        lines.append("")

    if stale:
        lines.append("#### 🟡 Stale — Action Required")
        lines.append("")
        lines.append("| Key | Summary | Owner | Last Updated | Project |")
        lines.append("|-----|---------|-------|-------------|---------|")
        for e in sorted(stale, key=lambda x: x["fields"].get("updated", "")):
            owner   = (e["fields"].get("assignee") or {}).get("displayName", "Unassigned")
            updated = e["fields"].get("updated", "")[:10]
            lines.append(
                f"| {e['key']} | {e['fields']['summary'][:55]} "
                f"| {owner} | {updated} | {e['_project']} |"
            )
        lines.append("")

    if active:
        lines.append("#### 🟢 Active — Ready for Review")
        lines.append("")
        lines.append("| Key | Summary | Owner | Status | Project |")
        lines.append("|-----|---------|-------|--------|---------|")
        for e in sorted(active, key=lambda x: x["fields"].get("updated", ""), reverse=True)[:20]:
            owner  = (e["fields"].get("assignee") or {}).get("displayName", "—")
            status = e["fields"]["status"]["name"]
            lines.append(
                f"| {e['key']} | {e['fields']['summary'][:55]} "
                f"| {owner} | {status} | {e['_project']} |"
            )

    return "\n".join(lines)


def _parse_dt(dt_str: str) -> datetime | None:
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except ValueError:
        return None
