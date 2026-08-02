# YOLOv8 GitHub release guide

This directory publishes the Ultralytics `v8.2.35` source snapshot used for the
YOLOv8n, YOLOv8s, and YOLOv8m experiments. Its layout follows the verified
YOLOv7 package: official source code is at the model root, lightweight run
settings are under `runs/`, and checkpoint hashes are under `weights/`.

## Training entry point

- Official tag: `v8.2.35`
- Upstream commit: `8ea945cc8e3ecbd466dde73f89ae018b3d7079f1`
- Python API/CLI package: `ultralytics/`
- Dataset configuration: `data/my_data.yaml`
- Recovered settings: `YOLOV8_REPRO_SETUP.md` and
  `runs/*/reproduction_config.yaml`

Datasets, checkpoints, caches, and generated run outputs are intentionally
excluded from ordinary Git history.

The optimizer was requested as `auto`; the optimizer ultimately selected at
runtime was not retained as a separate artifact and is not inferred.
