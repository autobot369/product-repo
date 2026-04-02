"""
pm_setup.py — click CLI root for the PM Workspace Setup tool.

Commands:
  (default)     Full first-time setup wizard
  reconfigure   Menu-driven partial reconfiguration
  check         Verify all integrations are reachable
"""
import sys
import click
from rich.console import Console
from rich.panel import Panel

console = Console()

BANNER = """\
[bold cyan]AUTOBOT369 // PM_OS_PRIME[/bold cyan]
[dim]Transforming backlogs into outcomes. Initiating boot sequence...[/dim]"""


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """PM Workspace Setup — configure this repo for your product team."""
    if ctx.invoked_subcommand is None:
        # Default: run the full setup wizard
        ctx.invoke(setup)


@cli.command("setup")
def setup() -> None:
    """Run the full first-time setup wizard."""
    from tools.setup.wizard import run_wizard

    console.print(Panel(BANNER, expand=False, border_style="cyan"))
    console.print()

    try:
        run_wizard()
    except KeyboardInterrupt:
        console.print("\n[yellow]Setup cancelled.[/yellow]")
        sys.exit(0)


@cli.command("reconfigure")
def reconfigure() -> None:
    """Open a menu to update specific configuration sections."""
    from tools.setup.wizard import run_reconfigure

    console.print(Panel(BANNER, expand=False, border_style="cyan"))
    console.print()

    try:
        run_reconfigure()
    except KeyboardInterrupt:
        console.print("\n[yellow]Reconfiguration cancelled.[/yellow]")
        sys.exit(0)


@cli.command("check")
def check() -> None:
    """Verify all integrations are reachable (Atlassian, Anthropic)."""
    from tools.setup.validators import run_health_check

    console.print(Panel(BANNER, expand=False, border_style="cyan"))
    console.print()

    try:
        run_health_check()
    except KeyboardInterrupt:
        console.print("\n[yellow]Check cancelled.[/yellow]")
        sys.exit(0)
