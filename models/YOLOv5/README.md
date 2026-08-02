# YOLOv5 release package

This directory contains the recovered YOLOv5 source snapshot and the
reproducibility records available for the YOLOv5n, YOLOv5s, and YOLOv5m
experiments. Its layout follows the verified YOLOv7 package: source code is at
the model root, lightweight run settings are under `runs/`, and weight hashes
are recorded under `weights/`.

## Training entry point

- Entry point: `train.py`
- Dataset configuration: `data/my_data.yaml`
- Model configurations: `models/yolov5n.yaml`, `models/yolov5s.yaml`, and
  `models/yolov5m.yaml`
- Recovered settings: see `YOLOV5_REPRO_SETUP.md` and the YAML files under
  `runs/`

Datasets, checkpoints, caches, and generated run outputs are intentionally
excluded from ordinary Git history.

## Verification boundary

The optimizer identity was not independently recoverable from the supplied
archive and is not inferred here. Replace the verification placeholder in a
training command only after checking the retained author record.
