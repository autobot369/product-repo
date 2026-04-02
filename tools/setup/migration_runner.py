"""
migration_runner.py — thin wrapper around tools/confluence-migration.

Writes a temporary config for the migration, then shells out to:
  python -m confluence_migration --config <path> [--dry-run]

The migration module already handles all stage gates and rich output,
so we just need to configure it and hand off.
"""
from __future__ import annotations

import os
import pathlib
import subprocess
import sys
import tempfile

import yaml
from rich.console import Console

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
MIGRATION_DIR = REPO_ROOT / "tools" / "confluence-migration"
EXAMPLE_CONFIG = MIGRATION_DIR / "config.example.yml"

console = Console()


def _build_migration_config(
    base_url: str,
    space_keys: list[str],
) -> dict:
    """
    Build a config dict for confluence_migration.
    Merges our global classifier defaults from config.example.yml.
    """
    base: dict = {}
    if EXAMPLE_CONFIG.exists():
        with open(EXAMPLE_CONFIG) as f:
            base = yaml.safe_load(f) or {}

    # Atlassian base URL
    base["atlassian"] = {"base_url": base_url}

    # Spaces to migrate
    base["spaces"] = space_keys

    # Output paths (relative paths that the migration module resolves from CWD)
    base["output"] = {
        "prds": "docs/PRDs",
        "abtests": "docs/experiments",
        "specs": "docs/specs",
        "research": "docs/research",
    }

    return base


def run_migration(
    base_url: str,
    email: str,
    token: str,
    space_keys: list[str],
    dry_run: bool = True,
) -> None:
    """
    Configure and run the confluence-migration pipeline.

    Credentials are passed via environment variables, never written to disk.
    A temporary config file is created for the run and cleaned up afterwards.
    """
    config_data = _build_migration_config(base_url, space_keys)

    # Write temp config
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".yml", prefix="pm_migration_")
    try:
        with os.fdopen(tmp_fd, "w") as f:
            yaml.dump(config_data, f)

        cmd = [
            sys.executable,
            "-m", "confluence_migration",
            "--config", tmp_path,
        ]
        if dry_run:
            cmd.append("--dry-run")

        env = {
            **os.environ,
            "ATLASSIAN_EMAIL": email,
            "ATLASSIAN_API_TOKEN": token,
            # Prepend repo root so confluence_migration is importable
            "PYTHONPATH": os.pathsep.join(
                filter(None, [str(REPO_ROOT), os.environ.get("PYTHONPATH", "")])
            ),
        }

        console.print()
        console.print(
            f"  [cyan]Running confluence migration for spaces:[/cyan] "
            f"[bold]{', '.join(space_keys)}[/bold]"
            + (" [dim](dry run)[/dim]" if dry_run else "")
        )
        console.print("  [dim]Moving data is like a transformation sequence — it looks cool, but one wrong move")
        console.print("  and everything gets stuck mid-gear. Stage gates will prompt you before any writes.[/dim]")
        console.print()

        result = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            env=env,
        )

        if result.returncode == 0:
            console.print()
            console.print("  [green]✓[/green] Migration complete.")
            if dry_run:
                console.print(
                    "  [dim]Dry run finished — no files written to docs/.\n"
                    "  Re-run without dry run to commit the output.[/dim]"
                )
        else:
            console.print()
            console.print(
                f"  [red]✗[/red] Migration exited with code {result.returncode}. "
                "Check output above for details."
            )
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
