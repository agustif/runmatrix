from __future__ import annotations

import json
from pathlib import Path

from runmatrix.domain.manifest import Manifest


def load_json_manifest(path: Path) -> Manifest:
    return Manifest.model_validate(json.loads(path.read_text(encoding="utf-8")))
