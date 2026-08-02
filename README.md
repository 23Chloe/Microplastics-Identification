# Microplastics Identification

Source code supporting microplastic image detection, classification, and evaluation.

## Branch structure

- `main`: stable publication branch.
- `original-pool-batch`: the only integration branch for the recovered source
  and reproducibility package.

See [`RELEASE_STATUS.md`](RELEASE_STATUS.md) for the evidence boundary and all
known publication blockers. Short-lived agent branches are not release branches.

## Repository layout

- `pipeline/`: data conversion, augmentation, dataset splitting, tiled inference, timing, and counting utilities.
- `models/YOLOv5/`: recovered YOLOv5 source package with run configurations and checkpoint hashes.
- `models/YOLOv7/`: verified YOLOv7 reproduction package. This directory was not changed by the later source-code uploads.
- `models/YOLOv8/`: official Ultralytics v8.2.35 source with recovered run configurations and checkpoint hashes.
- `models/DETR-Transformer/`: partial source archive with missing dataset modules explicitly documented.
- `models/Faster R-CNN/`: partial source archive with missing local modules explicitly documented.

Each model directory follows the same publication pattern where the evidence
permits it: a model-level README, a release manifest, a reproducibility setup,
lightweight run configurations, and a checkpoint inventory under `weights/`.

## Data and model weights

The image dataset, trained checkpoints, experiment outputs, and other large binary artifacts are not stored in ordinary Git history. Dataset configurations use repository-relative paths and expect the corresponding images and labels under `dataset/` when the dataset is supplied separately. See the model-specific documentation for weight placement.

## Reproducibility status

Machine-specific absolute paths were replaced with command-line arguments or repository-relative paths in the published utilities. The supplied DETR and Faster R-CNN archives did not contain every locally imported dependency; their exact limitations are recorded in the respective `ARCHIVE_NOTES.md` files and are not silently inferred or reconstructed.

The repository validation workflow performs dependency-free syntax and release
structure checks. It does not claim that incomplete model packages can train or
that unavailable datasets and checkpoints have been independently verified.

Evidence records:

- [`docs/MODEL_METADATA_RECOVERY.md`](docs/MODEL_METADATA_RECOVERY.md)
- [`docs/ANNOTATION_AND_SPLIT_PROVENANCE.md`](docs/ANNOTATION_AND_SPLIT_PROVENANCE.md)
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)
- [`LICENSE_SCOPE.md`](LICENSE_SCOPE.md)
