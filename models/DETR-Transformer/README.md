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

## Restored source boundary

The missing official `datasets/` package and Apache-2.0 license were restored
from `facebookresearch/detr` commit
`29901c51d7fe8712168b8d0d64351170bc0f83e0`. The source import structure is
complete after dependencies and data are supplied. Exact run-specific settings
and the definitive author checkpoint remain unresolved; see `ARCHIVE_NOTES.md`
and `RELEASE_MANIFEST.md`.
