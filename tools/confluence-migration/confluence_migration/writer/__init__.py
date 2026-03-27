"""
Writer — moves approved preview files into the repository docs/ folders.

Reads:  output/preview/  +  output/classification.yml
Writes: docs/PRDs/ | experiments/ | docs/specs/ | docs/research/ | output/unclassified/

Refuses to overwrite a file that does not have a `confluence_id` in its front
matter, protecting handcrafted docs from being stomped.

Writes: output/migration-report.md
"""

import yaml
import shutil
from pathlib import Path
from datetime import date


CATEGORY_DIR_KEY = {
    "prd":      "prds",
    "abtest":   "abtests",
    "spec":     "specs",
    "research": "research",
}


def write_pages(config: dict) -> dict:
    work_dir = Path(config.get("work_dir", "output"))
    with (work_dir / "classification.yml").open() as f:
        classifications = yaml.safe_load(f)

    written, skipped, protected = 0, 0, 0
    report_lines = [
        f"# Migration Report — {date.today().isoformat()}\n",
        "| Title | Category | Status | Destination |",
        "|-------|----------|--------|-------------|",
    ]

    for entry in classifications:
        if entry["category"] in ("skip", "unknown"):
            skipped += 1
            report_lines.append(f"| {entry['title']} | {entry['category']} | skipped | — |")
            continue

        dir_key = CATEGORY_DIR_KEY.get(entry["category"])
        if not dir_key:
            skipped += 1
            continue

        dest_dir = Path(config["output"][dir_key])
        preview_path = work_dir / "preview" / entry["category"] / f"{_slug(entry['title'])}.md"

        if not preview_path.exists():
            skipped += 1
            report_lines.append(f"| {entry['title']} | {entry['category']} | no preview | — |")
            continue

        dest_path = dest_dir / preview_path.name

        # Safety check — don't overwrite handcrafted files
        if dest_path.exists() and not _is_migrated_file(dest_path):
            protected += 1
            report_lines.append(f"| {entry['title']} | {entry['category']} | PROTECTED | {dest_path} |")
            continue

        shutil.copy2(preview_path, dest_path)
        written += 1
        report_lines.append(f"| {entry['title']} | {entry['category']} | written | {dest_path} |")

    report_lines.append(f"\n**{written} written · {skipped} skipped · {protected} protected**\n")

    (work_dir / "migration-report.md").write_text("\n".join(report_lines))
    return {"written": written, "skipped": skipped, "protected": protected}


def _slug(title: str) -> str:
    from slugify import slugify
    return slugify(title)


def _is_migrated_file(path: Path) -> bool:
    """Return True if the file was written by a previous migration run."""
    content = path.read_text()
    return "confluence_id:" in content
