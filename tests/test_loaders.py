from __future__ import annotations

from pathlib import Path

from runmatrix.plugins.loaders.json_loader import load_json_manifest
from runmatrix.plugins.loaders.toml_loader import load_toml_manifest
from runmatrix.plugins.loaders.yaml_loader import load_yaml_manifest


def test_yaml_loader(tmp_path: Path) -> None:
    path = tmp_path / "manifest.yaml"
    path.write_text(
        """
defaults:
  PROFILE: smoke
tasks:
  - id: base
    command: echo base
""".strip()
    )
    manifest = load_yaml_manifest(path)
    assert manifest.tasks[0].id == "base"


def test_json_loader(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text('{"tasks":[{"id":"base","command":"echo base"}]}')
    manifest = load_json_manifest(path)
    assert manifest.tasks[0].command == "echo base"


def test_toml_loader(tmp_path: Path) -> None:
    path = tmp_path / "manifest.toml"
    path.write_text(
        """
[[tasks]]
id = "base"
command = "echo base"
""".strip()
    )
    manifest = load_toml_manifest(path)
    assert manifest.tasks[0].id == "base"
