# YOLOv7 GitHub replacement guide

This directory is the verified lightweight replacement for
`models/YOLOv7`.

It contains the corrected architecture-specific source files, reproducibility
settings, and curated result records for YOLOv7, YOLOv7x, and YOLOv7-E6E.
Model weights are distributed separately because the corrected YOLOv7x and
YOLOv7-E6E files are too large for ordinary Git storage.

## Replacement

1. Keep the existing `models/YOLOv7` outside the repository as a local backup.
2. Replace the entire repository `models/YOLOv7` directory with this directory.
3. Do not merge the old `runs`, checkpoints, pretrained weights, bytecode, or
   machine-specific dataset caches back into this directory.
4. Publish the three verified weights supplied in the sibling
   `02_三个正确模型权重_单独发布` directory using Git LFS, GitHub Releases,
   Zenodo, Figshare, or another stable archive.
5. Add the resulting download URLs to `weights/README.md`.

## Correct training entry points and configurations

- YOLOv7: `train.py` with `cfg/training/yolov7.yaml`
- YOLOv7x: `train.py` with `cfg/training/yolov7x.yaml`
- YOLOv7-E6E: `train_aux.py` with `cfg/training/yolov7-e6e.yaml`

The included `runs` directories contain lightweight final records only. They
do not contain optimizer states, intermediate checkpoints, TensorBoard event
files, dataset caches, or training-batch previews.

