# DETR-Transformer recovered release package

This directory contains the DETR source files and checkpoint inventory
recovered from the author archive. Its publication structure follows the
verified YOLOv7 package, but its completeness status is different and is stated
explicitly.

## Available content

- Model definitions, transformer utilities, training engine, and entry points
- Original dependency specification
- Entrypoint-default configuration record under `runs/detr-r50/`
- Checkpoint filenames, sizes, and SHA-256 hashes under `weights/`

## Blocking limitation

The supplied archive does not contain the imported `datasets/` package,
including `coco_eval.py` and `panoptic_eval.py`. The training entry point is
therefore not standalone. `ARCHIVE_NOTES.md` and `RELEASE_MANIFEST.md` define
the exact publication boundary.
