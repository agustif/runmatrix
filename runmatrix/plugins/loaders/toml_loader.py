from __future__ import annotations

import tomllib
from pathlib import Path

from runmatrix.domain.manifest import Manifest


def load_toml_manifest(path: Path) -> Manifest:
    with path.open("rb") as handle:
        return Manifest.model_validate(tomllib.load(handle))
