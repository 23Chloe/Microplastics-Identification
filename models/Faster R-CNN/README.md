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

## Blocking limitation

The supplied archive does not contain the locally imported `nets/`, `utils/`,
or `model_data/` directories. The scripts are therefore not a standalone
runnable package.
