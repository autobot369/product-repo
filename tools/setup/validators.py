"""
validators.py — live Atlassian + Anthropic API validation.

Each validate_* function returns (ok: bool, message: str).
run_health_check() prints a full status table using rich.
"""
from __future__ import annotations

import os
from typing import Optional

import requests
from requests.auth import HTTPBasicAuth
from rich.console import Console
from rich.table import Table

console = Console()


# ── Atlassian helpers ───────────────────────────────────────────────────────────

def _atlassian_auth(email: str, token: str) -> HTTPBasicAuth:
    return HTTPBasicAuth(email, token)


def validate_atlassian_credentials(
    base_url: str,
    email: str,
    token: str,
    timeout: int = 8,
) -> tuple[bool, str]:
    """Ping /rest/api/3/myself to confirm credentials are valid."""
    url = f"{base_url.rstrip('/')}/rest/api/3/myself"
    try:
        resp = requests.get(url, auth=_atlassian_auth(email, token), timeout=timeout)
        if resp.status_code == 200:
            display_name = resp.json().get("displayName", email)
            return True, f"Authenticated as {display_name}"
        if resp.status_code == 401:
            return False, "Invalid credentials (401) — check email and API token"
        return False, f"Unexpected status {resp.status_code}"
    except requests.exceptions.ConnectionError:
        return False, f"Could not reach {base_url} — check the URL"
    except requests.exceptions.Timeout:
        return False, "Request timed out"


def validate_jira_project(
    base_url: str,
    email: str,
    token: str,
    project_key: str,
    timeout: int = 8,
) -> tuple[bool, str]:
    """Check that a Jira project key exists and is accessible."""
    url = f"{base_url.rstrip('/')}/rest/api/3/project/{project_key}"
    try:
        resp = requests.get(url, auth=_atlassian_auth(email, token), timeout=timeout)
        if resp.status_code == 200:
            name = resp.json().get("name", project_key)
            return True, f'"{name}" ({project_key})'
        if resp.status_code == 404:
            return False, f"Jira is acting like a Decepticon again. Project {project_key!r} not found — check the key"
        if resp.status_code == 403:
            return False, f"No access to project {project_key!r} — the Decepticons have this one locked down"
        return False, f"Status {resp.status_code}"
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as exc:
        return False, str(exc)


def validate_confluence_space(
    base_url: str,
    email: str,
    token: str,
    space_key: str,
    timeout: int = 8,
) -> tuple[bool, str]:
    """Check that a Confluence space key exists and is accessible."""
    url = f"{base_url.rstrip('/')}/wiki/rest/api/space/{space_key}"
    try:
        resp = requests.get(url, auth=_atlassian_auth(email, token), timeout=timeout)
        if resp.status_code == 200:
            name = resp.json().get("name", space_key)
            return True, f'"{name}" ({space_key})'
        if resp.status_code == 404:
            return False, f"Space {space_key!r} not found — it's a bit of a scrapheap in there, check the key"
        if resp.status_code == 403:
            return False, f"No access to space {space_key!r} — signal blocked, check your permissions"
        return False, f"Status {resp.status_code}"
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as exc:
        return False, str(exc)


def validate_anthropic_key(api_key: str) -> tuple[bool, str]:
    """Validate the Anthropic API key with a minimal models list call."""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        # Cheapest possible call — list models endpoint
        client.models.list(limit=1)
        return True, "API key valid"
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "authentication" in msg.lower() or "api_key" in msg.lower():
            return False, "Invalid API key"
        return False, f"Error: {msg[:80]}"


# ── Health check (post-setup) ───────────────────────────────────────────────────

def run_health_check(
    base_url: Optional[str] = None,
    email: Optional[str] = None,
    token: Optional[str] = None,
    anthropic_key: Optional[str] = None,
) -> bool:
    """
    Run all validations and print a status table.
    Falls back to reading values from tools/config.yml and .env if not provided.
    Returns True if all checks pass.
    """
    # Load from env / config if not explicitly passed
    from dotenv import load_dotenv
    import yaml
    import pathlib

    repo_root = pathlib.Path(__file__).resolve().parents[2]
    load_dotenv(repo_root / ".env")

    if not email:
        email = os.getenv("ATLASSIAN_EMAIL", "")
    if not token:
        token = os.getenv("ATLASSIAN_API_TOKEN", "")
    if not anthropic_key:
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")

    config_path = repo_root / "tools" / "config.yml"
    cfg: dict = {}
    if config_path.exists():
        with open(config_path) as f:
            cfg = yaml.safe_load(f) or {}
        if not base_url:
            base_url = cfg.get("atlassian", {}).get("base_url", "")

    table = Table(title="System Diagnostics: Is the Matrix of Leadership Intact?", show_header=True, header_style="bold cyan")
    table.add_column("Check", style="bold")
    table.add_column("Status")
    table.add_column("Detail")

    all_ok = True

    def _row(label: str, ok: bool, detail: str) -> None:
        nonlocal all_ok
        if not ok:
            all_ok = False
        status = "[green]✓ OK[/green]" if ok else "[red]✗ FAIL[/red]"
        table.add_row(label, status, detail)

    if base_url and email and token:
        ok, msg = validate_atlassian_credentials(base_url, email, token)
        _row("Atlassian credentials", ok, msg)

        for key in (cfg.get("jira", {}).get("projects", {}) or {}).values():
            ok, msg = validate_jira_project(base_url, email, token, key)
            _row(f"Jira project {key}", ok, msg)
        for space in (cfg.get("confluence", {}).get("spaces", []) or []):
            sk = space.get("key", "") if isinstance(space, dict) else space
            ok, msg = validate_confluence_space(base_url, email, token, sk)
            _row(f"Confluence space {sk}", ok, msg)
    else:
        _row("Atlassian credentials", False, "Missing base_url, email, or token in config/.env")

    if anthropic_key:
        ok, msg = validate_anthropic_key(anthropic_key)
        _row("Anthropic API key", ok, msg)
    else:
        _row("Anthropic API key", False, "ANTHROPIC_API_KEY not set in .env")

    console.print(table)
    if all_ok:
        console.print("\n[green bold]All checks passed.[/green bold]")
    else:
        console.print("\n[red bold]Some checks failed — review the table above.[/red bold]")

    return all_ok
