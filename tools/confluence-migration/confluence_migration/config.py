"""
Config loader — reads tools/config.yml (global) then deep-merges
tools/confluence-migration/config.yml (tool-specific) on top.

Credentials are never stored in config files; they are injected from
the .env file at repo root via python-dotenv.
"""

import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

# Repo root is 3 levels above this file:
#   confluence_migration/config.py → confluence_migration/ → confluence-migration/ → tools/ → repo/
REPO_ROOT = Path(__file__).parents[3]

load_dotenv(REPO_ROOT / ".env")

GLOBAL_CONFIG = REPO_ROOT / "tools" / "config.yml"
LOCAL_CONFIG  = Path(__file__).parents[1] / "config.yml"


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base; override wins on conflicts."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config() -> dict:
    # 1. Load global shared config
    if not GLOBAL_CONFIG.exists():
        print(f"Error: global config not found at '{GLOBAL_CONFIG}'")
        sys.exit(1)
    with GLOBAL_CONFIG.open() as f:
        config = yaml.safe_load(f)

    # 2. Pull this tool's section to the top level (cache, gates)
    tool_section = config.pop("confluence_migration", {})
    config = _deep_merge(config, tool_section)

    # 3. Deep-merge local tool config (classifier, skip_patterns, etc.)
    if LOCAL_CONFIG.exists():
        with LOCAL_CONFIG.open() as f:
            local = yaml.safe_load(f) or {}
        config = _deep_merge(config, local)

    # 4. Inject credentials from environment — never from config files
    config.setdefault("confluence", {})
    config["confluence"]["email"]     = os.environ.get("ATLASSIAN_EMAIL")
    config["confluence"]["api_token"] = os.environ.get("ATLASSIAN_API_TOKEN")

    missing = [
        v for v in ("ATLASSIAN_EMAIL", "ATLASSIAN_API_TOKEN")
        if not os.environ.get(v)
    ]
    if missing:
        print(f"Error: missing environment variables: {', '.join(missing)}")
        sys.exit(1)

    # 5. Convenience aliases used by fetcher and other modules
    #    config["spaces"]              — list read by fetcher
    #    config["confluence"]["base_url"] — REST API base used by fetcher
    config["spaces"] = config.get("confluence", {}).get("spaces", [])
    config["confluence"].setdefault(
        "base_url", config.get("atlassian", {}).get("base_url", "")
    )

    # 6. Resolve all paths relative to REPO_ROOT so the tool works from any CWD
    TOOL_ROOT = REPO_ROOT / "tools" / "confluence-migration"
    for key, rel_path in config.get("output", {}).items():
        config["output"][key] = str(REPO_ROOT / rel_path)
    cache_rel = config.get("cache", {}).get("dir", "tools/confluence-migration/cache/")
    config["cache"]["dir"] = str(REPO_ROOT / cache_rel)

    # Default work_dir for intermediate files (classification.yml, preview/)
    config.setdefault("work_dir", str(TOOL_ROOT / "output"))

    # 7. Ensure dirs exist
    for dir_path in config.get("output", {}).values():
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    Path(config["cache"]["dir"]).mkdir(parents=True, exist_ok=True)
    Path(config["work_dir"]).mkdir(parents=True, exist_ok=True)

    return config
