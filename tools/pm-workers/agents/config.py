"""
Config loader for pm-workers — reads tools/config.yml (global), promotes the
pm_workers section to top level, and injects credentials from .env at repo root.
"""

import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

REPO_ROOT     = Path(__file__).parents[3]
GLOBAL_CONFIG = REPO_ROOT / "tools" / "config.yml"
SKILLS_DIR    = REPO_ROOT / ".claude" / "skills"

load_dotenv(REPO_ROOT / ".env")


def _deep_merge(base: dict, override: dict) -> dict:
    result = dict(base)
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = _deep_merge(result[key], val)
        else:
            result[key] = val
    return result


def load_config() -> dict:
    if not GLOBAL_CONFIG.exists():
        print(f"Error: global config not found at '{GLOBAL_CONFIG}'")
        sys.exit(1)

    with GLOBAL_CONFIG.open() as f:
        global_cfg = yaml.safe_load(f)

    # Promote pm_workers section to top level, merge with global
    pm_workers_cfg = global_cfg.pop("pm_workers", {})
    config = _deep_merge(global_cfg, pm_workers_cfg)

    # Inject credentials
    config["anthropic_api_key"]  = os.environ.get("ANTHROPIC_API_KEY")
    config.setdefault("atlassian", {})
    config["atlassian"]["email"]     = os.environ.get("ATLASSIAN_EMAIL")
    config["atlassian"]["api_token"] = os.environ.get("ATLASSIAN_API_TOKEN")

    missing = [
        v for v in ("ANTHROPIC_API_KEY", "ATLASSIAN_EMAIL", "ATLASSIAN_API_TOKEN")
        if not os.environ.get(v)
    ]
    if missing:
        print(f"Error: missing environment variables: {', '.join(missing)}")
        sys.exit(1)

    config["skills_dir"] = SKILLS_DIR
    return config


def load_skill(name: str) -> str:
    """Read a skill markdown file from .claude/skills/."""
    # normalise: create-prd → create-prd.md, omni-monitor → omni-researcher.md
    aliases = {"omni-monitor": "omni-researcher"}
    resolved = aliases.get(name, name)

    path = SKILLS_DIR / f"{resolved}.md"
    if not path.exists():
        available = [p.stem for p in SKILLS_DIR.glob("*.md")]
        print(f"Error: skill '{name}' not found. Available: {', '.join(available)}")
        sys.exit(1)

    return path.read_text()
