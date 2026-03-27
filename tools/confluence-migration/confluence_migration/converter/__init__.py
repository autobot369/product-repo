"""
Converter — transforms Confluence storage XML to clean Markdown.

Reads:  cache/pages.json  +  output/classification.yml  (skips 'skip' and 'unknown')
Writes: output/preview/<category>/<slug>.md

Each file gets YAML front matter:
  title, confluence_id, confluence_url, category, labels, space_key, last_updated
"""

import json
import re
import yaml
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify
from slugify import slugify


def convert_pages(config: dict) -> None:
    with (Path(config["cache"]["dir"]) / "pages.json").open() as f:
        pages = {p["id"]: p for p in json.load(f)}

    work_dir = Path(config.get("work_dir", "output"))
    with (work_dir / "classification.yml").open() as f:
        classifications = yaml.safe_load(f)

    preview_root = work_dir / "preview"
    preview_root.mkdir(parents=True, exist_ok=True)

    converted = 0
    for entry in classifications:
        if entry["category"] in ("skip", "unknown"):
            continue

        page = pages.get(entry["id"])
        if not page:
            continue

        md = _to_markdown(page["body_storage"])
        front_matter = {
            "title": page["title"],
            "confluence_id": page["id"],
            "confluence_url": page["url"],
            "category": entry["category"],
            "labels": page.get("labels", []),
            "space_key": page["space_key"],
            "last_updated": date.today().isoformat(),
        }

        slug = slugify(page["title"])
        out_dir = preview_root / entry["category"]
        out_dir.mkdir(exist_ok=True)
        out_path = out_dir / f"{slug}.md"

        with out_path.open("w") as f:
            f.write("---\n")
            yaml.dump(front_matter, f, default_flow_style=False, allow_unicode=True)
            f.write("---\n\n")
            f.write(md)

        converted += 1

    print(f"  Converted {converted} pages")


def _to_markdown(storage_xml: str) -> str:
    if not storage_xml:
        return ""

    soup = BeautifulSoup(storage_xml, "lxml")

    # Confluence info/note/warning/tip → MkDocs admonitions
    _convert_panels(soup)

    # Strip Confluence-specific macros with no Markdown equivalent
    for macro in soup.find_all("ac:structured-macro"):
        macro_name = macro.get("ac:name", "")
        if macro_name in ("toc", "table-of-contents"):
            macro.decompose()  # MkDocs generates its own TOC
        elif macro_name == "expand":
            # Unwrap expand — keep the content
            macro.unwrap()

    html = str(soup)
    md = markdownify(html, heading_style="ATX", bullets="-")

    # Clean up excessive blank lines
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return md


def _convert_panels(soup: BeautifulSoup) -> None:
    """Map Confluence panel macros to MkDocs Material admonitions."""
    panel_map = {
        "info": "info",
        "note": "note",
        "warning": "warning",
        "tip": "tip",
        "success": "success",
    }
    for macro in soup.find_all("ac:structured-macro"):
        name = macro.get("ac:name", "")
        if name in panel_map:
            body = macro.find("ac:rich-text-body")
            content = str(body) if body else ""
            admonition = f'!!! {panel_map[name]}\n    {content}\n'
            macro.replace_with(BeautifulSoup(admonition, "lxml").body)
