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

The run-argument dictionaries identify the optimizer as SGD. The exact upstream
commit was not preserved: checkpoint fields for Git remote, branch, and commit
are null. The bundled source identifies itself as YOLOv5 version 7.0, but that
does not establish an exact commit.
