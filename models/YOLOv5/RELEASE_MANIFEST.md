# YOLOv5 release manifest

## Included

- Recovered YOLOv5 source snapshot
- YOLOv5n, YOLOv5s, and YOLOv5m architecture configurations
- Portable dataset configuration
- Original dependency specification
- Lightweight run-specific reproduction configurations
- Final-checkpoint filenames, byte sizes, and SHA-256 hashes

## Intentionally excluded

- Final and intermediate `.pt` checkpoints
- Optimizer states and generated experiment output
- Dataset images, labels, caches, and machine-specific paths
- Python bytecode and `__pycache__`

## Remaining limitation

The exact upstream commit and the run-resolved optimizer identity were not
preserved in the supplied archive. Neither value is inferred.
