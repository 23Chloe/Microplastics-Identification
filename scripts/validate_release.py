"""Perform dependency-free checks on the published release structure."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL_DIRS = (
    "YOLOv5",
    "YOLOv7",
    "YOLOv8",
    "DETR-Transformer",
    "Faster R-CNN",
)
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
WINDOWS_ABSOLUTE = re.compile(r"[A-Za-z]:[\\/]")


def require(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"Missing required path: {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []

    require(ROOT / "README.md", errors)
    require(ROOT / "RELEASE_STATUS.md", errors)
    require(ROOT / "pipeline" / "readme.md", errors)

    for model_name in MODEL_DIRS:
        model_root = ROOT / "models" / model_name
        require(model_root / "README.md", errors)
        if model_name == "YOLOv7":
            require(model_root / "REPLACEMENT_MANIFEST.md", errors)
        else:
            require(model_root / "RELEASE_MANIFEST.md", errors)

    for path in (ROOT / "pipeline").rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".py", ".md"}:
            continue
        text = path.read_text(encoding="utf-8")
        if HAN.search(text):
            errors.append(f"Chinese text remains in pipeline file: {path.relative_to(ROOT)}")
        if WINDOWS_ABSOLUTE.search(text):
            errors.append(f"Windows absolute path remains in pipeline file: {path.relative_to(ROOT)}")

    for relative in (
        Path("models/YOLOv5/data/my_data.yaml"),
        Path("models/YOLOv8/data/my_data.yaml"),
    ):
        text = (ROOT / relative).read_text(encoding="utf-8")
        if WINDOWS_ABSOLUTE.search(text):
            errors.append(f"Absolute dataset path remains in {relative}")

    if errors:
        print("Release validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Release structure validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
