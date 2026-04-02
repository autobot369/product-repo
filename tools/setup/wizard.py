"""
wizard.py — interactive setup wizard using questionary + rich.

Steps:
  1  Identity          (team name, PM name, site name)
  2  Atlassian creds   (base URL, email, API token)  → live validation
  3  Jira              (project keys, default key)   → live validation
  4  Confluence        (space key, optional page IDs) → live validation
  5  Claude / BMM      (model, language, skill level)
  6  Template review   (open .claude/agents/*.md one by one)
  7  Migration         (optional confluence-migration run)

run_reconfigure() presents a menu for partial re-runs of any step.
"""
from __future__ import annotations

import os
import pathlib
import subprocess
from typing import Any

import questionary
from questionary import Style
from rich.console import Console
from rich.rule import Rule

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
console = Console()

STYLE = Style(
    [
        ("qmark", "fg:#00bcd4 bold"),
        ("question", "bold"),
        ("answer", "fg:#00e676 bold"),
        ("pointer", "fg:#00bcd4 bold"),
        ("selected", "fg:#00e676"),
        ("separator", "fg:#6c6c6c"),
        ("instruction", "fg:#6c6c6c"),
    ]
)

CLAUDE_MODELS = [
    "claude-sonnet-4-6",
    "claude-opus-4-6",
    "claude-haiku-4-5-20251001",
]

SKILL_LEVELS = ["beginner", "intermediate", "expert"]

AGENT_FILES = sorted((REPO_ROOT / ".claude" / "agents").glob("*.md"))
SKILL_FILES = sorted((REPO_ROOT / ".claude" / "skills").glob("*.md"))


# ── helpers ─────────────────────────────────────────────────────────────────────

def _section(title: str) -> None:
    console.print()
    console.print(Rule(f"[bold cyan]{title}[/bold cyan]", style="cyan"))
    console.print()


def _ok(msg: str) -> None:
    console.print(f"  [green]✓[/green] {msg}")


def _fail(msg: str) -> None:
    console.print(f"  [red]✗[/red] {msg}")


def _info(msg: str) -> None:
    console.print(f"  [dim]{msg}[/dim]")


def _prompt(question_fn, **kwargs):
    """Run a questionary prompt; exit cleanly on Ctrl-C."""
    result = question_fn(style=STYLE, **kwargs).ask()
    if result is None:
        raise KeyboardInterrupt
    return result


# ── Step 1: Identity ────────────────────────────────────────────────────────────

def step_identity() -> dict[str, str]:
    _section("Step 1 — Team Identity")
    _info("Designating Your Squad. (Who's rolling out with us?)")
    console.print()

    team_name = _prompt(questionary.text, message="Team / squad name:", default="Product Team")
    pm_name = _prompt(questionary.text, message="Your name (PM):", default="PM")
    site_name = _prompt(
        questionary.text,
        message="MkDocs site name:",
        default=f"{team_name} Docs",
    )

    return {"team_name": team_name, "pm_name": pm_name, "site_name": site_name}


# ── Step 2: Atlassian credentials ───────────────────────────────────────────────

def step_atlassian(defaults: dict[str, str] | None = None) -> dict[str, str]:
    from tools.setup.validators import validate_atlassian_credentials

    _section("Step 2 — Atlassian Credentials")
    _info("Connecting the AllSpark. Mapping the documentation matrix.")
    _info("Encrypting your keys. This stays in your local .env — even Soundwave couldn't intercept this.")
    console.print()

    d = defaults or {}

    while True:
        base_url = _prompt(
            questionary.text,
            message="Atlassian base URL:",
            default=d.get("base_url", "https://your-org.atlassian.net"),
        )
        email = _prompt(
            questionary.text,
            message="Atlassian email:",
            default=d.get("email", ""),
        )
        token = _prompt(questionary.password, message="Atlassian API token:")

        console.print("  Validating credentials ...", end="")
        ok, msg = validate_atlassian_credentials(base_url, email, token)
        console.print()

        if ok:
            _ok(f"Energon Levels: Optimal.  {msg}")
            console.print("  [dim]Connection established. You're looking more optimized than a refreshed product vision, Shiv.[/dim]")
            return {"base_url": base_url, "email": email, "token": token}
        else:
            _fail(f"Jira is acting like a Decepticon again. {msg}")
            retry = _prompt(
                questionary.confirm,
                message="Retry with different values?",
                default=True,
            )
            if not retry:
                _info("Skipping validation — you can run `pm check` later.")
                return {"base_url": base_url, "email": email, "token": token}


# ── Step 3: Jira ─────────────────────────────────────────────────────────────────

def step_jira(atlassian: dict[str, str]) -> dict[str, Any]:
    from tools.setup.validators import validate_jira_project

    _section("Step 3 — Jira")
    _info("The Conflict at Confluence. Aligning the Autobots and the stakeholders.")
    console.print()

    keys_raw = _prompt(
        questionary.text,
        message="Jira project key(s)  [comma-separated]:",
        default="SQUAD1",
    )
    project_keys = [k.strip().upper() for k in keys_raw.split(",") if k.strip()]

    # Validate each key
    valid_keys: list[str] = []
    for key in project_keys:
        console.print(f"  Checking project {key} ...", end="")
        ok, msg = validate_jira_project(
            atlassian["base_url"], atlassian["email"], atlassian["token"], key
        )
        console.print()
        if ok:
            _ok(msg)
            valid_keys.append(key)
        else:
            _fail(f"{key}: {msg}")

    if not valid_keys:
        _info("No valid projects confirmed — using entered keys as-is.")
        valid_keys = project_keys

    default_key = valid_keys[0] if valid_keys else project_keys[0]
    if len(valid_keys) > 1:
        default_key = _prompt(
            questionary.select,
            message="Default Jira project key:",
            choices=valid_keys,
        )

    return {"project_keys": valid_keys, "default_jira_project": default_key}


# ── Step 4: Confluence ──────────────────────────────────────────────────────────

def step_confluence(atlassian: dict[str, str]) -> dict[str, Any]:
    from tools.setup.validators import validate_confluence_space

    _section("Step 4 — Confluence")
    _info("Scanning the Horizon. Plotting the coordinates for Q4.")
    _info("Searching the Knowledge Base... it's a bit of a scrapheap in there, but we'll find a signal.")
    _info("Page IDs are optional — leave blank to skip that publish target.")
    _info("Find a page ID in its URL: .../pages/<PAGE_ID>/...")
    console.print()

    space_key = _prompt(
        questionary.text,
        message="Confluence space key:",
        default="TEAM",
    ).upper()

    console.print(f"  Checking space {space_key} ...", end="")
    ok, msg = validate_confluence_space(
        atlassian["base_url"], atlassian["email"], atlassian["token"], space_key
    )
    console.print()
    if ok:
        _ok(msg)
    else:
        _fail(msg)
        _info("Proceeding — you can correct this in tools/config.yml later.")

    read_space = _prompt(
        questionary.text,
        message="Space key for agents to read context from:",
        default=space_key,
    ).upper()

    prd_parent = _prompt(
        questionary.text,
        message="PRD parent page ID  [optional]:",
        default="",
    ).strip()

    research_parent = _prompt(
        questionary.text,
        message="Market research parent page ID  [optional]:",
        default="",
    ).strip()

    sprint_reviews_parent = _prompt(
        questionary.text,
        message="Sprint reviews parent page ID  [optional]:",
        default="",
    ).strip()

    demand_review_page = _prompt(
        questionary.text,
        message="Demand review page ID  [optional]:",
        default="",
    ).strip()

    release_tracker_page = _prompt(
        questionary.text,
        message="Release tracker page ID  [optional]:",
        default="",
    ).strip()

    return {
        "space_key": space_key,
        "read_space": read_space,
        "prd_parent_page_id": prd_parent,
        "market_research_parent_page_id": research_parent,
        "jira_monitor": {
            "sprint_reviews_parent": sprint_reviews_parent,
            "demand_review_page_id": demand_review_page,
            "release_tracker_page_id": release_tracker_page,
        },
    }


# ── Step 5: Claude / BMM ────────────────────────────────────────────────────────

def step_bmm() -> dict[str, str]:
    _section("Step 5 — Claude & BMM Settings")
    console.print()

    model = _prompt(
        questionary.select,
        message="Primary Claude model:",
        choices=CLAUDE_MODELS,
        default="claude-sonnet-4-6",
    )

    language = _prompt(
        questionary.text,
        message="Communication language:",
        default="English",
    )

    skill_level = _prompt(
        questionary.select,
        message="Your PM skill level  (used to calibrate agent responses):",
        choices=SKILL_LEVELS,
        default="intermediate",
    )

    return {"primary_model": model, "language": language, "skill_level": skill_level}


# ── Step 6: Template verification ───────────────────────────────────────────────

def step_templates() -> None:
    _section("Step 6 — Agent Personas & Skills")
    console.print(
        "  Want to review the blueprints?\n"
        "  Inspecting the agent personas and skills now prevents a total system collapse during the sprint.\n"
        "  Each agent file ships with placeholder names — make them yours.\n"
        "  Each skill file declares its BMM phase, output contract, and handoff signals.\n"
    )

    if not AGENT_FILES and not SKILL_FILES:
        _info("No agent or skill files found — skipping.")
        return

    reviewable: list[tuple[str, pathlib.Path]] = []
    for path in AGENT_FILES:
        reviewable.append(("agent", path))
    for path in SKILL_FILES:
        reviewable.append(("skill", path))

    if AGENT_FILES:
        console.print("  [bold]Agent personas[/bold] (.claude/agents/):")
        for path in AGENT_FILES:
            console.print(f"    [cyan]{path.name}[/cyan]")
    if SKILL_FILES:
        console.print("  [bold]Skill playbooks[/bold] (.claude/skills/):")
        for path in SKILL_FILES:
            console.print(f"    [cyan]{path.name}[/cyan]")

    console.print()

    # Let user choose scope — agents only, skills only, or both
    scope = _prompt(
        questionary.select,
        message="Which files would you like to review?",
        choices=[
            "Agent personas only  (names, tone, principles)",
            "Skill playbooks only  (BMM phase, output contracts)",
            "Both agents and skills",
            "Skip — I'll review them later",
        ],
    )

    if "Skip" in scope:
        console.print()
        _info("You can review them later:")
        _info("  .claude/agents/   — agent persona files")
        _info("  .claude/skills/   — skill playbook files")
        return

    files_to_open: list[pathlib.Path] = []
    if "Agent" in scope or "Both" in scope:
        files_to_open.extend(AGENT_FILES)
    if "Skill" in scope or "Both" in scope:
        files_to_open.extend(SKILL_FILES)

    editor = _resolve_editor()

    for i, path in enumerate(files_to_open, 1):
        label = "agent" if path.parent.name == "agents" else "skill"
        console.print()
        console.print(f"  [{i}/{len(files_to_open)}] Opening [bold]{path.name}[/bold] [{label}] ...")
        _open_in_editor(editor, path)
        _prompt(
            questionary.press_any_key_to_continue,
            message=f"Press Enter when done with {path.name}",
        )

    _ok("Templates reviewed.")


def _resolve_editor() -> str:
    """Return the best available editor command."""
    for var in ("VISUAL", "EDITOR"):
        val = os.environ.get(var, "").strip()
        if val:
            return val
    # Fallbacks by platform
    candidates = ["code", "nano", "vim", "vi", "notepad"]
    for candidate in candidates:
        if _command_exists(candidate):
            return candidate
    return "notepad"  # last resort on Windows


def _command_exists(cmd: str) -> bool:
    import shutil
    return shutil.which(cmd) is not None


def _open_in_editor(editor: str, path: pathlib.Path) -> None:
    # VS Code returns immediately unless --wait is passed
    cmd = [editor, "--wait", str(path)] if editor == "code" else [editor, str(path)]
    try:
        subprocess.run(cmd, check=False)
    except FileNotFoundError:
        _fail(f"Could not launch '{editor}'. Open manually: {path}")


# ── Step 7: Confluence migration (optional) ──────────────────────────────────────

def step_migration(atlassian: dict[str, str]) -> None:
    from tools.setup.migration_runner import run_migration

    _section("Step 7 — Confluence Migration  (optional)")
    console.print(
        "  Import your existing Confluence docs into this repo's knowledge base.\n"
        "  The migration pipeline runs in stages with review gates between each step.\n"
    )

    run_it = _prompt(
        questionary.confirm,
        message="Import docs from Confluence now?",
        default=False,
    )
    if not run_it:
        console.print("  [bold yellow][INERTIA DETECTED][/bold yellow]")
        _info("Skipping? I get it — sometimes the MVP is just 'nothing.'")
        _info("You can manually trigger this module later:")
        _info("  python -m confluence_migration --config tools/confluence-migration/config.yml")
        return

    console.print()
    space_raw = _prompt(
        questionary.text,
        message="Confluence space key(s) to migrate  [comma-separated]:",
        default="TEAM",
    )
    spaces = [s.strip().upper() for s in space_raw.split(",") if s.strip()]

    dry_run = _prompt(
        questionary.confirm,
        message="Dry run first? (fetch + classify only, no writes to docs/)",
        default=True,
    )

    run_migration(
        base_url=atlassian["base_url"],
        email=atlassian["email"],
        token=atlassian["token"],
        space_keys=spaces,
        dry_run=dry_run,
    )


# ── Write all config ────────────────────────────────────────────────────────────

def _write_all(
    identity: dict,
    atlassian: dict,
    jira: dict,
    confluence: dict,
    bmm: dict,
) -> None:
    from tools.setup.writers.env_writer import write_env, ensure_env_example
    from tools.setup.writers.config_writer import write_config
    from tools.setup.writers.bmm_config_writer import write_bmm_config
    from tools.setup.writers.mkdocs_writer import write_mkdocs

    _section("Writing configuration")

    ensure_env_example()
    write_env({
        "ATLASSIAN_EMAIL": atlassian["email"],
        "ATLASSIAN_API_TOKEN": atlassian["token"],
    })
    _ok(".env updated")

    write_config(
        base_url=atlassian["base_url"],
        project_keys=jira["project_keys"],
        confluence_space_key=confluence["space_key"],
        pm_workers={
            "read_space": confluence["read_space"],
            "publish_space": confluence["space_key"],
            "prd_parent_page_id": confluence["prd_parent_page_id"],
            "market_research_parent_page_id": confluence["market_research_parent_page_id"],
            "default_jira_project": jira["default_jira_project"],
            "story_label": "pm-agent-generated",
        },
        jira_monitor=confluence.get("jira_monitor"),
    )
    _ok("tools/config.yml updated")

    write_bmm_config(
        project_name=identity["team_name"].lower().replace(" ", "-"),
        user_name=identity["pm_name"],
        user_skill_level=bmm["skill_level"],
        primary_model=bmm["primary_model"],
        communication_language=bmm["language"],
    )
    _ok("tools/bmm/config.yaml updated")

    write_mkdocs(
        site_name=identity["site_name"],
        team_name=identity["team_name"],
    )
    _ok("mkdocs.yml updated")


# ── Full wizard ─────────────────────────────────────────────────────────────────

def run_wizard() -> None:
    identity = step_identity()
    atlassian = step_atlassian()
    jira = step_jira(atlassian)
    confluence = step_confluence(atlassian)
    bmm = step_bmm()

    _write_all(identity, atlassian, jira, confluence, bmm)

    step_templates()
    step_migration(atlassian)

    _section("ACTIVATION COMPLETE")
    console.print("  [green bold]The PM_OS is fully transformed.[/green bold]")
    console.print("  [dim]The roadmap is clear, the dependencies are neutralized, and the backlog is primed.[/dim]")
    console.print()
    console.print("  [bold cyan]Product Managers: Roll out.[/bold cyan]")
    console.print()
    console.print("  Next steps:")
    console.print("    [cyan]mkdocs serve[/cyan]                  — preview your knowledge base")
    console.print("    [cyan]python -m tools.setup check[/cyan]   — verify all integrations")
    console.print()


# ── Reconfigure (menu) ──────────────────────────────────────────────────────────

_RECONFIG_SECTIONS = [
    ("Identity (team name, PM name, site name)", "identity"),
    ("Atlassian credentials", "atlassian"),
    ("Jira (project keys)", "jira"),
    ("Confluence (space key, page IDs)", "confluence"),
    ("Claude / BMM settings", "bmm"),
    ("Agent persona templates", "templates"),
    ("Run Confluence migration", "migration"),
    ("Exit", "exit"),
]


def run_reconfigure() -> None:
    _section("Reconfigure")
    _info("Select a section to update. Changes are written immediately.")

    # Load existing values from config for pre-filling
    atlassian = _load_existing_atlassian()

    while True:
        console.print()
        choice = _prompt(
            questionary.select,
            message="Which section would you like to update?",
            choices=[label for label, _ in _RECONFIG_SECTIONS],
        )
        key = dict(_RECONFIG_SECTIONS)[choice]

        if key == "exit":
            break
        elif key == "identity":
            identity = step_identity()
            from tools.setup.writers.mkdocs_writer import write_mkdocs
            from tools.setup.writers.bmm_config_writer import write_bmm_config
            import yaml
            bmm_path = REPO_ROOT / "tools" / "bmm" / "config.yaml"
            with open(bmm_path) as f:
                bmm_cfg = yaml.safe_load(f)
            write_mkdocs(identity["site_name"], identity["team_name"])
            write_bmm_config(
                project_name=identity["team_name"].lower().replace(" ", "-"),
                user_name=identity["pm_name"],
                user_skill_level=bmm_cfg.get("user_skill_level", "intermediate"),
                primary_model=bmm_cfg.get("primary_model", "claude-sonnet-4-6"),
                communication_language=bmm_cfg.get("communication_language", "English"),
            )
            _ok("Identity updated")
        elif key == "atlassian":
            atlassian = step_atlassian(defaults=atlassian)
            from tools.setup.writers.env_writer import write_env
            write_env({
                "ATLASSIAN_EMAIL": atlassian["email"],
                "ATLASSIAN_API_TOKEN": atlassian["token"],
            })
            import yaml
            cfg_path = REPO_ROOT / "tools" / "config.yml"
            with open(cfg_path) as f:
                cfg = yaml.safe_load(f)
            from tools.setup.writers.config_writer import write_config
            jira_projects = list((cfg.get("jira", {}).get("projects", {}) or {}).values())
            spaces = cfg.get("confluence", {}).get("spaces", [{}])
            space_key = spaces[0].get("key", "TEAM") if spaces else "TEAM"
            pm = cfg.get("pm_workers", {})
            write_config(
                base_url=atlassian["base_url"],
                project_keys=jira_projects or ["SQUAD1"],
                confluence_space_key=space_key,
                pm_workers={k: pm.get(k, "") for k in [
                    "read_space", "publish_space", "prd_parent_page_id",
                    "market_research_parent_page_id", "default_jira_project", "story_label",
                ]},
            )
            _ok("Atlassian credentials + base URL updated")
        elif key == "jira":
            jira = step_jira(atlassian)
            _apply_jira_patch(atlassian, jira)
            _ok("Jira config updated")
        elif key == "confluence":
            confluence = step_confluence(atlassian)
            _apply_confluence_patch(atlassian, confluence)
            _ok("Confluence config updated")
        elif key == "bmm":
            bmm = step_bmm()
            import yaml
            bmm_path = REPO_ROOT / "tools" / "bmm" / "config.yaml"
            with open(bmm_path) as f:
                bmm_cfg = yaml.safe_load(f)
            from tools.setup.writers.bmm_config_writer import write_bmm_config
            write_bmm_config(
                project_name=bmm_cfg.get("project_name", "product-repo"),
                user_name=bmm_cfg.get("user_name", "PM"),
                user_skill_level=bmm["skill_level"],
                primary_model=bmm["primary_model"],
                communication_language=bmm["language"],
            )
            _ok("BMM config updated")
        elif key == "templates":
            step_templates()
        elif key == "migration":
            step_migration(atlassian)

    console.print()
    _ok("Reconfiguration complete.")


def _load_existing_atlassian() -> dict[str, str]:
    """Load base_url from tools/config.yml and creds from .env for pre-filling."""
    from dotenv import load_dotenv
    import yaml

    load_dotenv(REPO_ROOT / ".env")
    cfg_path = REPO_ROOT / "tools" / "config.yml"
    base_url = "https://your-org.atlassian.net"
    if cfg_path.exists():
        with open(cfg_path) as f:
            cfg = yaml.safe_load(f)
        base_url = cfg.get("atlassian", {}).get("base_url", base_url)

    return {
        "base_url": base_url,
        "email": os.getenv("ATLASSIAN_EMAIL", ""),
        "token": os.getenv("ATLASSIAN_API_TOKEN", ""),
    }


def _apply_jira_patch(atlassian: dict, jira: dict) -> None:
    import yaml
    from tools.setup.writers.config_writer import write_config

    cfg_path = REPO_ROOT / "tools" / "config.yml"
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
    spaces = cfg.get("confluence", {}).get("spaces", [{}])
    space_key = spaces[0].get("key", "TEAM") if spaces else "TEAM"
    pm = cfg.get("pm_workers", {})
    write_config(
        base_url=atlassian["base_url"],
        project_keys=jira["project_keys"],
        confluence_space_key=space_key,
        pm_workers={
            "read_space": pm.get("read_space", space_key),
            "publish_space": pm.get("publish_space", space_key),
            "prd_parent_page_id": pm.get("prd_parent_page_id", ""),
            "market_research_parent_page_id": pm.get("market_research_parent_page_id", ""),
            "default_jira_project": jira["default_jira_project"],
            "story_label": pm.get("story_label", "pm-agent-generated"),
        },
    )


def _apply_confluence_patch(atlassian: dict, confluence: dict) -> None:
    import yaml
    from tools.setup.writers.config_writer import write_config

    cfg_path = REPO_ROOT / "tools" / "config.yml"
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
    project_keys = list((cfg.get("jira", {}).get("projects", {}) or {}).values())
    pm = cfg.get("pm_workers", {})
    write_config(
        base_url=atlassian["base_url"],
        project_keys=project_keys or ["SQUAD1"],
        confluence_space_key=confluence["space_key"],
        pm_workers={
            "read_space": confluence["read_space"],
            "publish_space": confluence["space_key"],
            "prd_parent_page_id": confluence["prd_parent_page_id"],
            "market_research_parent_page_id": confluence["market_research_parent_page_id"],
            "default_jira_project": pm.get("default_jira_project", project_keys[0] if project_keys else "SQUAD1"),
            "story_label": pm.get("story_label", "pm-agent-generated"),
        },
        jira_monitor=confluence.get("jira_monitor"),
    )
