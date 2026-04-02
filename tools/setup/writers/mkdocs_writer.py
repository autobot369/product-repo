"""
mkdocs_writer.py — patches mkdocs.yml using ruamel.yaml.

Only `site_name` and `copyright` are touched.
All theme settings, plugins, and nav are preserved.
"""
from __future__ import annotations

import pathlib

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
MKDOCS_PATH = REPO_ROOT / "mkdocs.yml"

_yaml = YAML()
_yaml.preserve_quotes = True
_yaml.width = 4096


def _load() -> CommentedMap:
    with open(MKDOCS_PATH, encoding="utf-8") as f:
        return _yaml.load(f)


def _save(data: CommentedMap) -> None:
    with open(MKDOCS_PATH, "w", encoding="utf-8") as f:
        _yaml.dump(data, f)


def write_mkdocs(site_name: str, team_name: str) -> None:
    """
    Update mkdocs.yml site_name and copyright.
    Nav and all other keys are left untouched.
    """
    data = _load()
    data["site_name"] = site_name
    data["copyright"] = team_name
    _save(data)
