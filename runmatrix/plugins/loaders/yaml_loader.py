from __future__ import annotations

from pathlib import Path

import yaml

from runmatrix.domain.manifest import Manifest


def load_yaml_manifest(path: Path) -> Manifest:
    return Manifest.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))
