"""
bmm_config_writer.py — patches tools/bmm/config.yaml using ruamel.yaml.

Fields written:
  project_name
  user_name
  user_skill_level
  primary_model
  communication_language
  document_output_language
"""
from __future__ import annotations

import pathlib

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
BMM_CONFIG_PATH = REPO_ROOT / "tools" / "bmm" / "config.yaml"

_yaml = YAML()
_yaml.preserve_quotes = True
_yaml.width = 4096


def _load() -> CommentedMap:
    with open(BMM_CONFIG_PATH, encoding="utf-8") as f:
        return _yaml.load(f)


def _save(data: CommentedMap) -> None:
    with open(BMM_CONFIG_PATH, "w", encoding="utf-8") as f:
        _yaml.dump(data, f)


def write_bmm_config(
    project_name: str,
    user_name: str,
    user_skill_level: str,
    primary_model: str,
    communication_language: str,
) -> None:
    """
    Patch tools/bmm/config.yaml with the provided values.
    All other fields (paths, prd_intake_mode, strategic_core_template) are preserved.
    """
    data = _load()

    data["project_name"] = project_name
    data["user_name"] = user_name
    data["user_skill_level"] = user_skill_level
    data["primary_model"] = primary_model
    data["communication_language"] = communication_language
    data["document_output_language"] = communication_language

    _save(data)
