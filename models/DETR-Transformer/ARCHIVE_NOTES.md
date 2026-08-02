# DETR source archive notes

This directory contains the DETR source files recovered from the author archive.
Large `.pth` checkpoints, run outputs, and Python caches are intentionally
excluded from ordinary Git history.

The archived training entry point imports a `datasets/` package (including
`coco_eval.py` and `panoptic_eval.py`) that was not present in the supplied
source archive. The model definitions, utilities, hub
entry point, and author prediction scripts are preserved here, but the training
entry point should not be described as standalone until that missing package is
restored and verified.
