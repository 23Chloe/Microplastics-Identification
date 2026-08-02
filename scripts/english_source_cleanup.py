"""Remove non-English comments and translate retained runtime messages.

This one-time provenance cleanup targets the recovered DETR and Faster R-CNN
archives. It does not change executable statements other than user-facing text
and a non-breaking space in one DETR docstring.
"""

from __future__ import annotations

import io
import re
import sys
import tokenize
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGETS = (ROOT / "models" / "DETR-Transformer", ROOT / "models" / "Faster R-CNN")


def translated_string(relative: str, token_text: str) -> str:
    normalized = token_text.replace("\xa0", " ")
    if not any(ord(char) > 127 for char in normalized):
        return normalized

    if relative.endswith("import datetime.py"):
        return '"XML <filename>, <folder>, and <path> fields were updated."'
    if relative.endswith("nets/vgg16.py"):
        return "'''Feature-map sizes for a 600 x 600 input follow the VGG16 pooling stages.'''"
    if relative.endswith("predict.py"):
        return "'''Use directory iteration for batch prediction and save returned images when required.'''"
    if relative.endswith("train.py"):
        if normalized.lstrip().startswith(("'''", '\"\"\"')):
            return "'''Training expects paired VOC JPEG images and XML annotations with matching class names.'''"
        if "Successful Load Key Num" in normalized:
            return '"\\nSuccessful Load Key Num:"'
        if "Fail To Load Key num" in normalized:
            return '"\\nFail To Load Key Num:"'
        if "head" in normalized and "Backbone" in normalized:
            return '"\\n[Notice] Missing head keys are expected; missing backbone keys indicate a problem."'
        if "Unfreeze_batch_size" in normalized:
            return '"\\n[Warning] This run has %d training samples, batch size %d, %d epochs, and %d total steps."'
        if normalized.count("%d") >= 3:
            return '"[Warning] Total steps %d are below the recommended %d; consider %d epochs."'
        if "%s" in normalized and "%d" in normalized:
            return '"\\n[Warning] When using the %s optimizer, at least %d total training steps are recommended."'
        if "dataset" in normalized.lower() or "数据集" in normalized:
            return "'The dataset is too small for training; add more samples.'"
    if relative.endswith("voc_annotation.py"):
        if "500" in normalized:
            return '"The training set contains fewer than 500 images; consider more epochs to provide enough optimization steps."'
        if "空格" in normalized:
            return '"Dataset directory paths and image filenames must not contain spaces."'
        if "目标" in normalized:
            return '"No targets were found. Verify classes_path and annotation class names."'
        if "三遍" in normalized:
            return '"Please verify this before training."'
    if relative.endswith("utils/utils_map.py"):
        if "种类" in normalized:
            return '"No classes were detected. Verify the annotations and classes_path setting."'
        if "目标" in normalized:
            return '"No detections were found."'

    raise ValueError(f"No English replacement for non-ASCII string in {relative}: {token_text[:120]!r}")


def clean(path: Path) -> None:
    relative = path.relative_to(ROOT).as_posix()
    raw = path.read_bytes()
    output = []
    for token in tokenize.tokenize(io.BytesIO(raw).readline):
        text = token.string
        if token.type == tokenize.COMMENT and any(ord(char) > 127 for char in text):
            text = ""
        elif token.type == tokenize.STRING and any(ord(char) > 127 for char in text):
            text = translated_string(relative, text)
        output.append(token._replace(string=text))
    cleaned = tokenize.untokenize(output).decode("utf-8")
    cleaned = re.sub(r"[ \t]+(?=\r?$)", "", cleaned, flags=re.MULTILINE)
    path.write_text(cleaned, encoding="utf-8", newline="\n")


def main() -> int:
    for target in TARGETS:
        for path in sorted(target.rglob("*.py")):
            clean(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
