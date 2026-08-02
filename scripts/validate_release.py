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
NON_ASCII = re.compile(r"[^\x00-\x7f]")
WINDOWS_ABSOLUTE = re.compile(r"[A-Za-z]:[\\/]")


def require(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"Missing required path: {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []

    require(ROOT / "README.md", errors)
    require(ROOT / "RELEASE_STATUS.md", errors)
    require(ROOT / "THIRD_PARTY_NOTICES.md", errors)
    require(ROOT / "LICENSE_SCOPE.md", errors)
    require(ROOT / "pipeline" / "readme.md", errors)
    require(ROOT / "pipeline" / "group_manifest.example.csv", errors)
    require(ROOT / "models" / "YOLOv7" / "METRICS_PROVENANCE.md", errors)

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

    for model_name in ("DETR-Transformer", "Faster R-CNN"):
        for path in (ROOT / "models" / model_name).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            if NON_ASCII.search(text):
                errors.append(f"Non-ASCII source text remains in {path.relative_to(ROOT)}")

    for source_root in (ROOT / "pipeline", ROOT / "models"):
        for path in source_root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            if HAN.search(text):
                errors.append(f"Chinese source text remains in {path.relative_to(ROOT)}")

    weight_readmes = tuple(
        ROOT / "models" / model_name / "weights" / "README.md"
        for model_name in MODEL_DIRS
    )
    for path in weight_readmes:
        require(path, errors)
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if "Add after publishing" in text or "URL pending" in text:
                errors.append(f"Unresolved weight URL placeholder remains in {path.relative_to(ROOT)}")

    for legacy_path in (
        Path("models/DETR-Transformer/models/not.py"),
        Path("models/DETR-Transformer/predict_csdn.py"),
        Path("models/Faster R-CNN/import datetime.py"),
        Path("models/Faster R-CNN/get_map50- 95.py"),
    ):
        if (ROOT / legacy_path).exists():
            errors.append(f"Legacy scratch filename remains: {legacy_path}")

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
