# Faster R-CNN release manifest

## Included

- Recovered training, inference, annotation, summary, and evaluation scripts
- `nets/`, `utils/`, and MIT license restored from
  `bubbliiiing/faster-rcnn-pytorch` commit
  `d81ba09f9c961e7ae07612e638a242f18e2c50fe`
- Three-class `model_data/classes.txt` reconstructed from retained dataset
  configurations
- Original dependency specification
- Source-backed training configuration record
- Final-checkpoint filenames, sizes, and SHA-256 hashes

## Intentionally excluded

- `.pth` checkpoint binaries
- Generated logs, TensorBoard events, output images, and VOC data
- Machine-specific paths and caches

## Remaining evidence limitation

- Any additional run-level tuning log beyond the settings embedded in
  `train.py`

The selected archive checkpoint is published in the `model-weights-v1`
GitHub Release, with its URL and SHA-256 recorded in `weights/README.md`.
