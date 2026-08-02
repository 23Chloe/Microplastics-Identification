# Verified replacement manifest for `models/YOLOv7`

## Included

- YOLOv7 source code at commit
  `a207844b1ce82d204ab36d87d496728d3d2348e7`
- `train.py` and `train_aux.py`
- Correct YOLOv7, YOLOv7x, and YOLOv7-E6E architecture configurations
- P5 and P6 hyperparameter configurations
- Portable dataset configuration template
- Reproduction environment and package lock
- Corrected 400-epoch result records for all three YOLOv7 variants
- PR, F1, precision, recall, confusion-matrix, and loss-summary figures
- Architecture-specific reproduction configuration records
- Weight hashes and parameter counts
- Final-epoch versus best-fitness metric provenance in `METRICS_PROVENANCE.md`

## Intentionally excluded from the GitHub folder

- Old invalid YOLOv7x and YOLOv7-E6E checkpoints
- Optimizer-state and intermediate checkpoints
- Root-level pretrained `.pt` files
- Python bytecode and `__pycache__`
- Dataset caches and machine-specific absolute paths
- TensorBoard event files and training-batch preview images

## Weight distribution

The three verified final weights are published in the `model-weights-v1`
GitHub Release. Direct URLs and SHA-256 values are recorded in
`weights/README.md`.

