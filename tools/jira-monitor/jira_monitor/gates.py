"""
Stage gate — blocks execution for human review before publishing to Confluence.
Identical pattern to confluence-migration/gates.py.
"""


def gate(title: str, instructions: str) -> None:
    width = 72
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)
    print(instructions)
    print("-" * width)

    while True:
        try:
            answer = input("  Publish to Confluence? [yes / skip / abort]: ").strip().lower()
        except EOFError:
            print("  Non-interactive mode — skipping gate (use --no-gate to suppress this).")
            return

        if answer in ("yes", "y"):
            return
        elif answer in ("skip", "s"):
            raise GateSkipped()
        elif answer in ("abort", "a", "q"):
            print("  Aborted.")
            raise SystemExit(0)
        else:
            print("  Please type 'yes', 'skip', or 'abort'.")


class GateSkipped(Exception):
    """Raised when the user chooses to skip publishing for this workstream."""
