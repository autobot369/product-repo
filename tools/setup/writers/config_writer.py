"""
config_writer.py — patches tools/config.yml using ruamel.yaml (preserves comments).

Sections written:
  atlassian.base_url
  jira.projects           (rebuilt from project_keys list)
  confluence.spaces       (rebuilt from space_keys list)
  pm_workers.*            (all pm_workers fields)
"""
from __future__ import annotations

import pathlib
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
CONFIG_PATH = REPO_ROOT / "tools" / "config.yml"

_yaml = YAML()
_yaml.preserve_quotes = True
_yaml.width = 4096  # prevent line wrapping


def _load() -> CommentedMap:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return _yaml.load(f)


def _save(data: CommentedMap) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        _yaml.dump(data, f)


def _ensure_section(data: CommentedMap, *keys: str) -> Any:
    """Walk/create nested keys, returning the innermost mapping."""
    node = data
    for key in keys:
        if key not in node or not isinstance(node[key], dict):
            node[key] = CommentedMap()
        node = node[key]
    return node


def write_config(
    base_url: str,
    project_keys: list[str],
    confluence_space_key: str,
    pm_workers: dict[str, Any],
    jira_monitor: dict[str, str] | None = None,
) -> None:
    """
    Patch tools/config.yml with the provided values.

    Args:
        base_url:            Atlassian base URL  (e.g. https://org.atlassian.net)
        project_keys:        List of Jira project keys  (e.g. ["CHKT", "PLAT"])
        confluence_space_key: Primary Confluence space key
        pm_workers:          Dict of pm_workers overrides (read_space, publish_space,
                             prd_parent_page_id, market_research_parent_page_id,
                             default_jira_project, story_label, scheduler.*)
        jira_monitor:        Optional dict of jira_monitor.confluence page IDs
                             (sprint_reviews_parent, demand_review_page_id,
                              release_tracker_page_id)
    """
    data = _load()

    # atlassian
    atl = _ensure_section(data, "atlassian")
    atl["base_url"] = base_url

    # jira.projects — rebuild as ordered mapping
    jira = _ensure_section(data, "jira")
    projects = CommentedMap()
    for i, key in enumerate(project_keys):
        label = f"squad{i + 1}" if i < 9 else key.lower()
        projects[label] = key
    jira["projects"] = projects

    # confluence.spaces
    conf = _ensure_section(data, "confluence")
    spaces = CommentedSeq()
    entry = CommentedMap()
    entry["key"] = confluence_space_key
    entry["label"] = "Product Team"
    spaces.append(entry)
    conf["spaces"] = spaces

    # pm_workers — merge provided keys
    pm = _ensure_section(data, "pm_workers")
    flat_keys = {
        "read_space", "publish_space", "prd_parent_page_id",
        "market_research_parent_page_id", "default_jira_project", "story_label",
    }
    for k, v in pm_workers.items():
        if k == "scheduler" and isinstance(v, dict):
            sched = _ensure_section(data, "pm_workers", "scheduler")
            for sk, sv in v.items():
                sched[sk] = sv
        elif k in flat_keys:
            pm[k] = v

    # jira_monitor.confluence page IDs
    if jira_monitor:
        jm_conf = _ensure_section(data, "jira_monitor", "confluence")
        writable_keys = {
            "sprint_reviews_parent", "demand_review_page_id",
            "release_tracker_page_id", "pipeline_page_id",
        }
        for k, v in jira_monitor.items():
            if k in writable_keys:
                jm_conf[k] = v

    _save(data)
