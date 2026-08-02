# DETR source archive notes

This directory contains the DETR source files recovered from the author archive.
Large `.pth` checkpoints, run outputs, and Python caches are intentionally
excluded from ordinary Git history.

The author archive omitted the imported `datasets/` package. It has now been
restored from the archived official `facebookresearch/detr` repository at
commit `29901c51d7fe8712168b8d0d64351170bc0f83e0`, whose shared source files
match the retained archive except for the author's explicit `main.py` run-default
changes. The upstream Apache-2.0 license is included.

This source restoration makes the import structure complete. It does not prove
the exact run arguments or identify which author checkpoint produced the
reported benchmark.

The redundant hard-coded `predict_csdn.py` scratch example was not retained in
the release package; the maintained prediction entry point is `predict.py`.
