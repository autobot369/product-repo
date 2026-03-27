"""
Classifier — assigns each cached page a category.

Priority order:
  1. Exact title overrides   (exact_titles in config)
  2. Skip patterns           (skip_patterns in config)
  3. Confluence labels       (label_map in config)
  4. Title heuristics        (heuristics in config)
  5. Claude API fallback     (for ambiguous pages)
  6. 'unknown'               (human review required)

Reads:  cache/pages.json
Writes: output/classification.yml

classification.yml schema:
  - id: "12345"
    title: "Search Re-ranking PRD"
    space_key: SEA
    url: https://...
    category: prd        # prd | abtest | spec | skip | unknown
    confidence: label    # label | heuristic | claude | none
    reason: "label 'prd' matched"
"""

import json
import re
import yaml
from pathlib import Path


CATEGORIES = ("prd", "abtest", "spec", "research", "skip", "unknown")


def classify_pages(config: dict) -> None:
    cache_path = Path(config["cache"]["dir"]) / "pages.json"
    with cache_path.open() as f:
        pages = json.load(f)

    classifier_config = config.get("classifier", {})
    results = []

    for page in pages:
        category, confidence, reason = _classify(page, classifier_config)
        results.append({
            "id": page["id"],
            "title": page["title"],
            "space_key": page["space_key"],
            "url": page["url"],
            "category": category,
            "confidence": confidence,
            "reason": reason,
        })

    counts = {c: sum(1 for r in results if r["category"] == c) for c in CATEGORIES}
    print(f"  Classification summary: {counts}")

    work_dir = Path(config.get("work_dir", "output"))
    work_dir.mkdir(parents=True, exist_ok=True)
    out_path = work_dir / "classification.yml"
    with out_path.open("w") as f:
        yaml.dump(results, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def _classify(page: dict, cfg: dict) -> tuple[str, str, str]:
    labels = [l.lower() for l in page.get("labels", [])]
    title = page.get("title", "")

    # 1. Exact title overrides — highest priority
    exact_titles = cfg.get("exact_titles", {})
    if title in exact_titles:
        return exact_titles[title], "exact", f"exact title match"

    # 2. Skip patterns
    for pattern in cfg.get("skip_patterns", []):
        if re.search(pattern, title, re.IGNORECASE):
            return "skip", "heuristic", f"title matched skip pattern '{pattern}'"

    # 3. Label map
    label_map = cfg.get("label_map", {})
    for label in labels:
        if label in label_map:
            return label_map[label], "label", f"label '{label}' matched"

    # 4. Title heuristics
    heuristics = cfg.get("heuristics", {})
    for category, keywords in heuristics.items():
        for kw in keywords:
            if kw.lower() in title.lower():
                return category, "heuristic", f"title contains '{kw}'"

    # 4. Claude fallback (placeholder — wired up in classifier/claude.py)
    if cfg.get("use_claude", False):
        from .claude import classify_with_claude
        return classify_with_claude(page)

    return "unknown", "none", "no label, heuristic, or Claude match"
