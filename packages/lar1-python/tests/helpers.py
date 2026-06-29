"""Conformance fixture loader."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CONFORMANCE_ROOT = REPO_ROOT / "SPEC" / "conformance"


def load_fixtures(subdir: str) -> list[dict]:
    directory = CONFORMANCE_ROOT / subdir
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(directory.glob("*.json"))
    ]
