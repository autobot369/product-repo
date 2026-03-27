"""
Jira Monitor — automated sprint, release, demand, and pipeline reporting.

Runs as: python -m jira_monitor [--mode MODE] [--dry-run] [--no-gate]

Modes:
  all       Run all 4 workstreams in parallel (default)
  sprint    Sprint review prep only
  release   Release candidate tracker only
  demand    Demand review digest only
  pipeline  Feature pipeline monitor only

Flags:
  --dry-run   Generate report, skip Confluence publish
  --no-gate   Skip the confirmation gate before publishing

Reports are written to output/<mode>-<date>.md regardless of --dry-run.
"""

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

from .config import load_config
from .client import AtlassianClient
from .gates import gate, GateSkipped
from .publisher import prepend_entry
from .reporters import sprint_review, release_tracker, demand_review, feature_pipeline

WORKSTREAMS = {
    "sprint":   (sprint_review,   "Sprint Review"),
    "release":  (release_tracker, "Release Tracker"),
    "demand":   (demand_review,   "Demand Review"),
    "pipeline": (feature_pipeline, "Feature Pipeline"),
}

CONFLUENCE_PAGE_KEYS = {
    "sprint":   ("confluence", "pages", "sprint_reviews_parent"),
    "release":  ("confluence", "release_tracker_page_id"),
    "demand":   ("confluence", "demand_review_page_id"),
    "pipeline": ("confluence", "pipeline_page_id"),
}


def _get_page_id(config: dict, mode: str) -> str | None:
    keys = CONFLUENCE_PAGE_KEYS.get(mode, ())
    obj  = config
    for k in keys:
        obj = obj.get(k, {}) if isinstance(obj, dict) else None
        if obj is None:
            return None
    return obj if isinstance(obj, str) and obj else None


def _run_workstream(module, name: str, client: AtlassianClient, config: dict) -> tuple[str, str]:
    """Run a single reporter and return (name, markdown_report)."""
    print(f"  → Running {name}...")
    try:
        report = module.run(client, config)
    except Exception as e:
        report = f"_Error running {name}: {e}_"
    return name, report


def main():
    parser = argparse.ArgumentParser(description="Jira Monitor — sprint, release, demand & pipeline reporter.")
    parser.add_argument(
        "--mode",
        choices=["all", "sprint", "release", "demand", "pipeline"],
        default="all",
        help="Which workstream(s) to run (default: all)",
    )
    parser.add_argument("--dry-run",  action="store_true", help="Generate reports but do not publish to Confluence")
    parser.add_argument("--no-gate",  action="store_true", help="Skip confirmation gate before publishing")
    args = parser.parse_args()

    config = load_config()
    client = AtlassianClient(config)
    today  = date.today().isoformat()

    modes = list(WORKSTREAMS.keys()) if args.mode == "all" else [args.mode]

    # ── Run workstreams (parallel for --mode all) ────────────────────────────
    print(f"\n[jira-monitor] Running {len(modes)} workstream(s) in {'parallel' if len(modes) > 1 else 'foreground'}...\n")

    results: dict[str, str] = {}

    if len(modes) > 1:
        with ThreadPoolExecutor(max_workers=len(modes)) as pool:
            futures = {
                pool.submit(_run_workstream, WORKSTREAMS[m][0], WORKSTREAMS[m][1], client, config): m
                for m in modes
            }
            for future in as_completed(futures):
                mode = futures[future]
                try:
                    name, report = future.result()
                    results[mode] = report
                    print(f"  ✓ {name} complete")
                except Exception as e:
                    results[mode] = f"_Workstream failed: {e}_"
    else:
        m = modes[0]
        name, report = _run_workstream(WORKSTREAMS[m][0], WORKSTREAMS[m][1], client, config)
        results[m] = report

    # ── Write reports to output/ ─────────────────────────────────────────────
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    for mode, report in results.items():
        out_path = output_dir / f"{mode}-{today}.md"
        out_path.write_text(f"# {WORKSTREAMS[mode][1]} — {today}\n\n{report}\n")
        print(f"  Report saved → {out_path}")

    # ── Publish to Confluence ────────────────────────────────────────────────
    if args.dry_run:
        print("\n[dry-run] Skipping Confluence publish.")
    else:
        should_gate = config.get("gates", {}).get("pause_before_publish", True) and not args.no_gate
        for mode, report in results.items():
            page_id = _get_page_id(config, mode)
            if not page_id:
                print(f"  ⚠  No Confluence page ID configured for '{mode}' — skipping publish.")
                continue

            if should_gate:
                try:
                    gate(
                        title=f"GATE — Publish {WORKSTREAMS[mode][1]} to Confluence",
                        instructions=(
                            f"Review output/{mode}-{today}.md\n"
                            f"Target page ID: {page_id}"
                        ),
                    )
                except GateSkipped:
                    print(f"  Skipped publish for {mode}.")
                    continue

            try:
                url = prepend_entry(client, page_id, report, WORKSTREAMS[mode][1])
                print(f"  ✓ Published {mode} → {url}")
            except Exception as e:
                print(f"  ✗ Failed to publish {mode}: {e}")

    print("\nDone.\n")


if __name__ == "__main__":
    main()
