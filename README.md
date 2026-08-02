# Microplastics Identification

Source code supporting microplastic image detection, classification, and evaluation.

## Repository layout

- `pipeline/`: data conversion, augmentation, dataset splitting, tiled inference, timing, and counting utilities.
- `models/YOLOv5/yolov5/`: recovered YOLOv5 source package.
- `models/YOLOv7/`: verified YOLOv7 reproduction package. This directory was not changed by the later source-code uploads.
- `models/YOLOv8/`: recovered YOLOv8 source package.
- `models/DETR-Transformer/`: source files recovered from the supplied DETR archive.
- `models/Faster R-CNN/`: source files recovered from the supplied Faster R-CNN archive.

## Data and model weights

The image dataset, trained checkpoints, experiment outputs, and other large binary artifacts are not stored in ordinary Git history. Dataset configurations use repository-relative paths and expect the corresponding images and labels under `dataset/` when the dataset is supplied separately. See the model-specific documentation for weight placement.

## Reproducibility status

Machine-specific absolute paths were replaced with command-line arguments or repository-relative paths in the published utilities. The supplied DETR and Faster R-CNN archives did not contain every locally imported dependency; their exact limitations are recorded in the respective `ARCHIVE_NOTES.md` files and are not silently inferred or reconstructed.
