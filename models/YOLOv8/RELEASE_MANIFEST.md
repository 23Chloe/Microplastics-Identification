# YOLOv8 release manifest

## Included

- Official Ultralytics source at tag `v8.2.35`, commit
  `8ea945cc8e3ecbd466dde73f89ae018b3d7079f1`
- YOLOv8n, YOLOv8s, and YOLOv8m architecture configurations
- Portable dataset configuration
- Original `pyproject.toml` dependency metadata
- Lightweight run-specific reproduction configurations
- Final-checkpoint filenames, byte sizes, and SHA-256 hashes

## Intentionally excluded

- Final, intermediate, and pretrained `.pt` checkpoints
- Generated experiment outputs and dataset caches
- Dataset images and labels
- Python bytecode and machine-specific paths

## Remaining limitation

The optimizer was configured as `auto`; no optimizer state or console log was
retained. From the bundled 8.2.35 selection rule and the reported training-set
size, the resolved optimizer is reconstructed as SGD with learning rate 0.01
and momentum 0.9. This reconstruction is explicitly distinguished from a saved
run artifact.
