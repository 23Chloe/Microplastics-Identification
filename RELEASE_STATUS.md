# Release status and verification boundary

## Branch policy

- `main` is the stable publication branch.
- `original-pool-batch` is the single integration branch for the recovered
  source and reproducibility package.
- Short-lived agent branches are not part of the public release structure.
- Changes from `original-pool-batch` should reach `main` through one reviewed
  pull request after the checks in this document pass.

## Package status

| Component | Source status | Run settings | Runnable now | Remaining blocker |
|---|---|---|---|---|
| YOLOv5 n/s/m | Recovered source snapshot | Partial, archive-backed | Yes after dependencies and data are supplied | Exact upstream commit and resolved optimizer are not verified |
| YOLOv7 / x / E6E | Verified replacement package | Archive-backed | Yes after dependencies, data, and weights are supplied | Public checkpoint URLs remain unavailable |
| YOLOv8 n/s/m | Official Ultralytics 8.2.35 source, commit `8ea945cc8e3ecbd466dde73f89ae018b3d7079f1` | Archive-backed | Yes after dependencies, data, and weights are supplied | Resolved `optimizer=auto` choice was not retained |
| DETR R50 | Partial recovered archive | Entrypoint defaults only | No | Missing `datasets/` and exact run-specific settings |
| Faster R-CNN R50 | Partial recovered archive | Source-backed | No | Missing `nets/`, `utils/`, and `model_data/` |
| Data-processing pipeline | Portable command-line scripts | Source-backed | Syntax validated | Dataset split provenance and augmentation ordering require author verification |

## Required before a reproducibility claim

1. Publish each final checkpoint at a stable URL and retain its recorded SHA-256.
2. Restore the missing DETR and Faster R-CNN modules from evidence-matched source.
3. Verify the YOLOv5 optimizer identity and upstream source revision.
4. Record the resolved YOLOv8 optimizer selected by `optimizer=auto`, if recoverable.
5. Confirm that train, validation, and test membership was assigned before
   augmentation, or demonstrate that augmented derivatives of one source image
   never crossed dataset splits.
6. Add the retained LabelMe version and annotation audit record.

Unresolved values must remain explicit. They must not be reconstructed by
guessing from framework defaults.
