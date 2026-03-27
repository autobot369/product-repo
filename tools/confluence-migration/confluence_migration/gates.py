"""
Stage gate — pauses execution and waits for human confirmation.
"""

import sys


class GateSkipped(Exception):
    """Raised when the user chooses to skip (not abort) a gate."""


def gate(title: str, instructions: str, skip: bool = False) -> None:
    """
    Print a review prompt and block until the user types 'yes' or 'y'.
    Typing 'abort' exits the process cleanly.
    Pass skip=True (or run with --no-gate) to auto-continue without prompting.
    Also auto-continues when stdin is not a TTY (e.g. piped or Claude Code).
    """
    border = "─" * 60
    print(f"\n{border}")
    print(f"  ⏸  {title}")
    print(border)
    print(f"\n{instructions}\n")

    if skip or not sys.stdin.isatty():
        print("  (non-interactive — gate auto-continued)\n")
        return

    while True:
        try:
            response = input("  Continue? [yes / abort]: ").strip().lower()
        except EOFError:
            print("\n  (EOF — gate auto-continued)\n")
            return
        if response in ("yes", "y"):
            print()
            return
        if response in ("abort", "no", "n", "q"):
            print("\n  Aborted. Re-run with --from-stage to resume.\n")
            raise SystemExit(0)
        print("  Type 'yes' to continue or 'abort' to stop.")
