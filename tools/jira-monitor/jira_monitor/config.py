"""
Config loader — reads tools/config.yml (global) and injects credentials from .env.
No local config file; all jira-monitor settings live in the global tools/config.yml
under the `jira_monitor:` key.
"""

import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

REPO_ROOT    = Path(__file__).parents[3]
GLOBAL_CONFIG = REPO_ROOT / "tools" / "config.yml"

load_dotenv(REPO_ROOT / ".env")


def load_config() -> dict:
    if not GLOBAL_CONFIG.exists():
        print(f"Error: global config not found at '{GLOBAL_CONFIG}'")
        sys.exit(1)

    with GLOBAL_CONFIG.open() as f:
        config = yaml.safe_load(f)

    # Pull this tool's section to top level
    tool_section = config.pop("jira_monitor", {})
    for key, value in tool_section.items():
        if key in config and isinstance(config[key], dict) and isinstance(value, dict):
            config[key] = {**config[key], **value}
        else:
            config[key] = value

    # Inject credentials
    config.setdefault("atlassian", {})
    config["atlassian"]["email"]     = os.environ.get("ATLASSIAN_EMAIL")
    config["atlassian"]["api_token"] = os.environ.get("ATLASSIAN_API_TOKEN")

    missing = [v for v in ("ATLASSIAN_EMAIL", "ATLASSIAN_API_TOKEN") if not os.environ.get(v)]
    if missing:
        print(f"Error: missing environment variables: {', '.join(missing)}")
        sys.exit(1)

    Path("output").mkdir(exist_ok=True)
    return config
