"""
Confluence → Product Repository Migration
==========================================
Runs as: python -m confluence_migration

Stage gates pause execution and ask for human review before proceeding.
Each stage writes its output to disk so you can inspect, edit, and re-run
from any stage without re-fetching from Confluence.

Stages:
  1. fetch      — pull all pages from configured spaces → cache/pages.json
  [GATE]        — review page list, edit cache/pages.json to remove unwanted pages
  2. classify   — categorise each page → output/classification.yml
  [GATE]        — review and correct classifications before any files are written
  3. convert    — render Confluence storage XML → Markdown → output/preview/
  [GATE]        — (optional) review converted Markdown before writing to docs/
  4. write      — write approved Markdown to docs/PRDs/, experiments/, docs/specs/
"""

import argparse
import sys
from pathlib import Path

from .config import load_config
from .gates import gate
from .fetcher import fetch_spaces
from .classifier import classify_pages
from .converter import convert_pages
from .writer import write_pages


def main():
    parser = argparse.ArgumentParser(
        description="Migrate Confluence spaces to the product repository."
    )
    parser.add_argument(
        "--space",
        metavar="KEY",
        help=(
            "Confluence space key to migrate (e.g. SHOP). "
            "Overrides the spaces list in config and uses a per-space "
            "cache and output directory so multiple migrations don't conflict."
        ),
    )
    parser.add_argument(
        "--space-label",
        metavar="LABEL",
        help="Human-readable label for the space (default: same as KEY)",
    )
    parser.add_argument(
        "--parent-page",
        metavar="PAGE_ID",
        help=(
            "Confluence page ID to scope the fetch to (fetches descendants only). "
            "Use when migrating a single folder/section rather than a full space."
        ),
    )
    parser.add_argument(
        "--parent-label",
        metavar="LABEL",
        help="Human-readable label for the parent page (used in gate messages)",
    )
    parser.add_argument(
        "--from-stage",
        choices=["fetch", "classify", "convert", "write"],
        default="fetch",
        help="Resume from a specific stage (uses cached output from prior stages)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run all stages but do not write files to docs/",
    )
    parser.add_argument(
        "--no-gate",
        action="store_true",
        help="Skip all review gates and run all stages unattended",
    )
    args = parser.parse_args()

    config = load_config()

    # ── Per-space overrides ───────────────────────────────────────────────────
    if args.space:
        from pathlib import Path as _Path
        space_key   = args.space.upper()
        space_label = args.space_label or space_key

        # Restrict fetcher to just this space
        config["spaces"] = [{"key": space_key, "label": space_label}]

        # Separate cache and intermediate dirs per space (append space key as subdir)
        config["cache"]["dir"] = str(_Path(config["cache"]["dir"]) / space_key)
        config["work_dir"]     = str(_Path(config["work_dir"]) / space_key)

        # Space-specific doc output dirs (docs/PRDs/SHOP/, docs/specs/SHOP/, etc.)
        for key in config.get("output", {}):
            config["output"][key] = str(_Path(config["output"][key]) / space_key)

        # Ensure dirs exist
        _Path(config["cache"]["dir"]).mkdir(parents=True, exist_ok=True)
        _Path(config["work_dir"]).mkdir(parents=True, exist_ok=True)
        for dir_path in config["output"].values():
            _Path(dir_path).mkdir(parents=True, exist_ok=True)

        print(f"  Space override: fetching {space_key} only")

    if args.parent_page:
        config["parent_page_id"]    = args.parent_page
        config["parent_page_label"] = args.parent_label or args.parent_page
        print(f"  Scope: descendants of page {args.parent_page} ({config['parent_page_label']})")
    stages = ["fetch", "classify", "convert", "write"]
    start = stages.index(args.from_stage)

    # ── Stage 1: Fetch ────────────────────────────────────────────────────────
    if start <= 0:
        print("\n[Stage 1/4] Fetching pages from Confluence spaces...")
        fetch_spaces(config)
        cache_dir = config["cache"]["dir"].rstrip("/")
        print(f"  ✓ Pages written to {cache_dir}/pages.json")

        if config["gates"]["pause_after_fetch"]:
            gate(
                title="GATE 1 — Review fetched pages",
                instructions=(
                    f"Open  {cache_dir}/pages.json\n"
                    "Remove any pages you do not want to migrate, then continue."
                ),
                skip=args.no_gate,
            )

    # ── Stage 2: Classify ─────────────────────────────────────────────────────
    if start <= 1:
        print("\n[Stage 2/4] Classifying pages...")
        classify_pages(config)
        work_dir = config["work_dir"]
        print(f"  ✓ Classification written to {work_dir}/classification.yml")

        if config["gates"]["pause_after_classify"]:
            gate(
                title="GATE 2 — Review classifications",
                instructions=(
                    f"Open  {work_dir}/classification.yml\n"
                    "Check each page is assigned the right category:\n"
                    "  prd | abtest | spec | skip\n"
                    "Edit the file, then continue."
                ),
                skip=args.no_gate,
            )

    # ── Stage 3: Convert ──────────────────────────────────────────────────────
    if start <= 2:
        work_dir = config["work_dir"]
        print("\n[Stage 3/4] Converting pages to Markdown...")
        convert_pages(config)
        print(f"  ✓ Markdown previews written to {work_dir}/preview/")

        if config["gates"]["pause_after_convert"]:
            gate(
                title="GATE 3 — Review converted Markdown",
                instructions=(
                    f"Open  {work_dir}/preview/\n"
                    "Check formatting, front matter tags, and content quality.\n"
                    "Edit preview files directly if needed, then continue."
                ),
                skip=args.no_gate,
            )

    # ── Stage 4: Write ────────────────────────────────────────────────────────
    if start <= 3:
        work_dir = config["work_dir"]
        if args.dry_run:
            print("\n[Stage 4/4] Dry run — skipping write to docs/")
        else:
            print("\n[Stage 4/4] Writing files to repository...")
            report = write_pages(config)
            print(f"  ✓ Migration report written to {work_dir}/migration-report.md")
            print(f"  ✓ {report['written']} files written, {report['skipped']} skipped")

    print("\nDone.\n")


if __name__ == "__main__":
    main()
