# Faster R-CNN release manifest

## Included

- Recovered training, inference, annotation, summary, and evaluation scripts
- Original dependency specification
- Source-backed training configuration record
- Final-checkpoint filenames, sizes, and SHA-256 hashes

## Intentionally excluded

- `.pth` checkpoint binaries
- Generated logs, TensorBoard events, output images, and VOC data
- Machine-specific paths and caches

## Missing from the supplied archive

- `nets/`
- `utils/`
- `model_data/`
- Any additional run-level tuning log beyond the settings embedded in
  `train.py`
