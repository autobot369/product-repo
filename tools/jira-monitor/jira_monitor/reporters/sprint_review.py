"""
Workstream 1 — Sprint Review Reporter

For each configured project:
  - Finds the active sprint
  - Lists all stories by status bucket (Done / In Progress / Blocked / Not Started)
  - Flags sprint goal risk (>30% not started with <3 days remaining)
  - Generates a demo agenda (Done items, grouped by epic)

Publishes to: confluence.pages.sprint_reviews_parent (global config)
"""

from datetime import datetime, timezone

from ..client import AtlassianClient

FIELDS = ["summary", "status", "assignee", "issuetype", "priority", "parent", "labels", "duedate"]

STATUS_BUCKETS = {
    "done":        {"done", "closed", "resolved", "approved"},
    "in_progress": {"in progress", "develop", "ready for testing", "in review"},
    "blocked":     {"blocked", "impediment"},
}


def run(client: AtlassianClient, config: dict) -> str:
    """Return a Markdown report string."""
    projects = config.get("jira", {}).get("projects", {})
    target_keys = [k for k in projects.values() if k]

    sections = []
    risk_threshold = config.get("sprint_review", {}).get("risk_threshold", 0.30)

    for project_key in target_keys:
        section = _report_project(client, project_key, risk_threshold)
        if section:
            sections.append(section)

    if not sections:
        return "_No active sprints found across configured projects._"

    return "\n\n---\n\n".join(sections)


def _report_project(client: AtlassianClient, project_key: str, risk_threshold: float) -> str | None:
    # Find boards for the project
    try:
        boards = client.get_boards(project_key)
    except Exception as e:
        return f"### {project_key}\n\n_Could not fetch boards: {e}_"

    if not boards:
        return None

    board_id = boards[0]["id"]

    # Get active sprint
    sprint = client.get_active_sprint(board_id)
    if not sprint:
        return None

    sprint_name = sprint.get("name", "Active Sprint")
    sprint_end  = sprint.get("endDate", "")
    days_left   = _days_remaining(sprint_end)

    # Fetch issues
    try:
        issues = client.get_sprint_issues(sprint["id"], FIELDS)
    except Exception as e:
        return f"### {project_key} — {sprint_name}\n\n_Could not fetch issues: {e}_"

    buckets = _bucket_issues(issues)
    total   = len(issues)
    done_n  = len(buckets["done"])
    ip_n    = len(buckets["in_progress"])
    blocked_n = len(buckets["blocked"])
    todo_n  = len(buckets["not_started"])

    # Risk flag
    risk_flag = ""
    if total > 0 and days_left is not None and days_left <= 3:
        not_done_pct = (total - done_n) / total
        if not_done_pct > risk_threshold:
            risk_flag = f"\n\n> ⚠️ **Sprint at risk** — {total - done_n}/{total} items not done with {days_left}d remaining."

    # Demo agenda (Done items grouped by epic)
    demo_section = _demo_agenda(buckets["done"])

    lines = [
        f"### {project_key} — {sprint_name}",
        f"**End date:** {sprint_end[:10] if sprint_end else 'unknown'}"
        + (f" ({days_left}d remaining)" if days_left is not None else ""),
        risk_flag,
        "",
        f"| Status | Count |",
        f"|--------|-------|",
        f"| ✅ Done | {done_n} |",
        f"| 🔄 In Progress | {ip_n} |",
        f"| 🚫 Blocked | {blocked_n} |",
        f"| ⬜ Not Started | {todo_n} |",
        f"| **Total** | **{total}** |",
        "",
    ]

    if buckets["blocked"]:
        lines.append("**Blocked items:**")
        for issue in buckets["blocked"]:
            lines.append(f"- [{issue['key']}] {issue['fields']['summary']}")
        lines.append("")

    lines.append(demo_section)

    return "\n".join(lines)


def _bucket_issues(issues: list[dict]) -> dict:
    buckets = {"done": [], "in_progress": [], "blocked": [], "not_started": []}
    for issue in issues:
        status = issue["fields"]["status"]["name"].lower()
        if status in STATUS_BUCKETS["done"]:
            buckets["done"].append(issue)
        elif status in STATUS_BUCKETS["blocked"]:
            buckets["blocked"].append(issue)
        elif status in STATUS_BUCKETS["in_progress"]:
            buckets["in_progress"].append(issue)
        else:
            buckets["not_started"].append(issue)
    return buckets


def _demo_agenda(done_issues: list[dict]) -> str:
    if not done_issues:
        return "_No completed items to demo._"

    # Group by epic name (parent summary field)
    by_epic: dict[str, list] = {}
    for issue in done_issues:
        epic = _epic_name(issue)
        by_epic.setdefault(epic, []).append(issue)

    lines = ["**Demo agenda (completed items):**"]
    for epic, items in sorted(by_epic.items()):
        lines.append(f"\n_{epic}_")
        for issue in items:
            assignee = (issue["fields"].get("assignee") or {}).get("displayName", "Unassigned")
            lines.append(f"- [{issue['key']}] {issue['fields']['summary']} — {assignee}")

    return "\n".join(lines)


def _epic_name(issue: dict) -> str:
    parent = issue["fields"].get("parent")
    if parent:
        return parent.get("fields", {}).get("summary", parent.get("key", "No Epic"))
    return "No Epic"


def _days_remaining(end_date_str: str) -> int | None:
    if not end_date_str:
        return None
    try:
        end = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        return max(0, (end - now).days)
    except ValueError:
        return None
