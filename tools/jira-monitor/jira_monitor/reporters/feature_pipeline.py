"""
Workstream 4 — Feature Pipeline Monitor

For each active epic in ISD / AUTO:
  - Calculates story completion % (Done / Total)
  - Surfaces blocked or unassigned stories
  - Cross-references docs/research/ISD/ for competitive signals that map
    to in-flight features — closing the omni-monitor → roadmap → sprint loop

Replaces: AUTO-125 (Early Access MVP) and AUTO-145 (Personalization MVP)
          manual feature tracking stories.
Publishes to: jira_monitor.confluence.pipeline_page_id (global config)
"""

import re
from pathlib import Path

from ..client import AtlassianClient

EPIC_FIELDS  = ["summary", "status", "assignee", "priority", "updated", "description"]
STORY_FIELDS = ["summary", "status", "assignee", "priority", "issuetype", "parent", "labels"]

DONE_STATUSES    = {"done", "closed", "resolved", "approved"}
BLOCKED_STATUSES = {"blocked", "impediment"}
IN_PROGRESS      = {"in progress", "develop", "ready for testing", "in review"}


def run(client: AtlassianClient, config: dict) -> str:
    """Return a Markdown report string."""
    projects = config.get("jira", {}).get("projects", {})
    target_keys = [projects.get("isd"), projects.get("auto")]
    target_keys = [k for k in target_keys if k]

    research_dir = Path(config.get("output", {}).get("research", "docs/research")) / "ISD"
    signals      = _load_research_signals(research_dir)

    sections = []
    for project_key in target_keys:
        section = _report_project(client, project_key, signals)
        if section:
            sections.append(section)

    if not sections:
        return "_No active epics found in feature pipeline._"

    return "\n\n---\n\n".join(sections)


def _report_project(client: AtlassianClient, project_key: str, signals: list[dict]) -> str | None:
    try:
        epics = client.search_issues(
            jql=(
                f'project = {project_key} '
                f'AND issuetype = Epic '
                f'AND statusCategory in ("In Progress", "To Do") '
                f'ORDER BY updated DESC'
            ),
            fields=EPIC_FIELDS,
            max_results=30,
        )
    except Exception as e:
        return f"### {project_key} — Feature Pipeline\n\n_Could not fetch epics: {e}_"

    if not epics:
        return None

    lines = [f"### {project_key} — Feature Pipeline", ""]
    lines.append("| Epic | Summary | % Done | Blocked | Assignee |")
    lines.append("|------|---------|--------|---------|----------|")

    detail_blocks = []

    for epic in epics:
        key     = epic["key"]
        summary = epic["fields"]["summary"][:55]
        assignee = (epic["fields"].get("assignee") or {}).get("displayName", "Unassigned")

        # Fetch child stories
        try:
            stories = client.search_issues(
                jql=f'parent = {key}',
                fields=STORY_FIELDS,
                max_results=50,
            )
        except Exception:
            stories = []

        total    = len(stories)
        done_n   = sum(1 for s in stories if s["fields"]["status"]["name"].lower() in DONE_STATUSES)
        blocked  = [s for s in stories if s["fields"]["status"]["name"].lower() in BLOCKED_STATUSES]
        unassigned_stories = [
            s for s in stories
            if s["fields"].get("assignee") is None
            and s["fields"]["status"]["name"].lower() not in DONE_STATUSES
        ]

        pct      = f"{int(done_n / total * 100)}%" if total > 0 else "—"
        blocked_str = f"🚫 {len(blocked)}" if blocked else "—"

        lines.append(f"| {key} | {summary} | {pct} | {blocked_str} | {assignee} |")

        # Detail block for epics with blockers or unassigned work
        if blocked or unassigned_stories:
            block = [f"\n**{key} — {epic['fields']['summary']}**"]
            if blocked:
                block.append("_Blocked stories:_")
                for s in blocked:
                    block.append(f"- [{s['key']}] {s['fields']['summary']}")
            if unassigned_stories:
                block.append("_Unassigned open stories:_")
                for s in unassigned_stories[:5]:
                    block.append(f"- [{s['key']}] {s['fields']['summary']}")
            detail_blocks.append("\n".join(block))

        # Cross-reference research signals
        matched = _match_signals(epic["fields"]["summary"], signals)
        if matched:
            signal_note = f"\n**{key} — Competitive signal match:**"
            for sig in matched:
                signal_note += f"\n- {sig['title']}: _{sig['excerpt']}_"
            detail_blocks.append(signal_note)

    lines.append("")
    if detail_blocks:
        lines.append("#### Details")
        lines.extend(detail_blocks)

    return "\n".join(lines)


def _load_research_signals(research_dir: Path) -> list[dict]:
    """
    Read research docs and extract title + first non-empty body line as excerpt.
    Used for cross-referencing against epic summaries.
    """
    signals = []
    if not research_dir.exists():
        return signals

    for md_file in research_dir.glob("*.md"):
        if md_file.name == "index.md":
            continue
        try:
            text  = md_file.read_text()
            title = _extract_frontmatter_title(text) or md_file.stem.replace("-", " ").title()
            # First substantive line after front matter
            body_lines = [l.strip() for l in text.split("---", 2)[-1].split("\n") if l.strip() and not l.startswith("#")]
            excerpt    = body_lines[0][:100] if body_lines else ""
            # Keywords: words 4+ chars from the title
            keywords = [w.lower() for w in re.split(r"\W+", title) if len(w) >= 4]
            signals.append({"title": title, "excerpt": excerpt, "keywords": keywords, "file": md_file.name})
        except Exception:
            continue

    return signals


def _match_signals(epic_summary: str, signals: list[dict]) -> list[dict]:
    summary_lower = epic_summary.lower()
    matched = []
    for sig in signals:
        if any(kw in summary_lower for kw in sig["keywords"]):
            matched.append(sig)
    return matched[:2]  # cap at 2 per epic to keep report concise


def _extract_frontmatter_title(text: str) -> str | None:
    for line in text.split("\n"):
        if line.startswith("title:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return None
