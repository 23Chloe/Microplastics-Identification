# Faster R-CNN recovered release package

This directory contains the Faster R-CNN scripts and reproducibility evidence
recovered from the author archive. Its publication structure follows the
verified YOLOv7 package while retaining an explicit incomplete-archive status.

## Recovered configuration

- Backbone: ResNet-50
- Input: 600 x 600 pixels
- Optimizer: Adam
- Initial learning rate: 1e-4
- Cosine decay to 1e-6
- Frozen through epoch 20 with batch size 4
- Unfrozen through epoch 150 with batch size 2
- Seed: 11

See `FASTER_RCNN_REPRO_SETUP.md` and
`runs/faster-rcnn-resnet50/reproduction_config.yaml`.

## Restored source boundary

The missing `nets/` and `utils/` modules and MIT license were restored from
`bubbliiiing/faster-rcnn-pytorch` commit
`d81ba09f9c961e7ae07612e638a242f18e2c50fe`. The three-class mapping was
restored under `model_data/classes.txt`. The package is structurally runnable
after dependencies, data, and a verified checkpoint are supplied. Final
checkpoint publication remains pending.
