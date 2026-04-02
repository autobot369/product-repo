"""
env_writer.py — writes / merges credentials into .env at repo root.

Rules:
- Credentials are NEVER written to tracked YAML files.
- If .env already exists, only update keys that were explicitly collected.
- Keys absent from the new values dict are left untouched.
- .env.example is always kept in sync with structure (no real values).
"""
from __future__ import annotations

import pathlib
import re


REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
ENV_PATH = REPO_ROOT / ".env"
ENV_EXAMPLE_PATH = REPO_ROOT / ".env.example"

_EXAMPLE_CONTENT = """\
# Copy this file to .env and fill in your values.
# .env is gitignored — never commit credentials.

# Atlassian (Confluence + Jira)
# Create an API token at https://id.atlassian.com/manage-profile/security/api-tokens
ATLASSIAN_EMAIL=you@yourcompany.com
ATLASSIAN_API_TOKEN=your-atlassian-api-token

# Anthropic (Claude)
# Used by pm-workers agents and as fallback classifier in confluence-migration
# Create a key at https://console.anthropic.com/
ANTHROPIC_API_KEY=your-anthropic-api-key
"""


def _parse_env(path: pathlib.Path) -> list[str]:
    """Return raw lines from an env file, or empty list if missing."""
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


def _set_key(lines: list[str], key: str, value: str) -> list[str]:
    """
    Replace the value for `key` in existing lines, or append it.
    Leaves comments and blank lines intact.
    """
    pattern = re.compile(rf"^{re.escape(key)}\s*=")
    replaced = False
    result = []
    for line in lines:
        if pattern.match(line):
            result.append(f"{key}={value}\n")
            replaced = True
        else:
            result.append(line)
    if not replaced:
        if result and not result[-1].endswith("\n"):
            result.append("\n")
        result.append(f"{key}={value}\n")
    return result


def write_env(values: dict[str, str]) -> None:
    """
    Merge `values` (key → value) into .env.
    Creates .env from .env.example if it doesn't exist.
    """
    if not ENV_PATH.exists():
        if ENV_EXAMPLE_PATH.exists():
            lines = _parse_env(ENV_EXAMPLE_PATH)
        else:
            lines = _EXAMPLE_CONTENT.splitlines(keepends=True)
    else:
        lines = _parse_env(ENV_PATH)

    for key, value in values.items():
        lines = _set_key(lines, key, value)

    ENV_PATH.write_text("".join(lines), encoding="utf-8")


def ensure_env_example() -> None:
    """Create .env.example if it doesn't already exist."""
    if not ENV_EXAMPLE_PATH.exists():
        ENV_EXAMPLE_PATH.write_text(_EXAMPLE_CONTENT, encoding="utf-8")
