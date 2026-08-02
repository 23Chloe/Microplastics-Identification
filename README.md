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
- `models/DETR-Transformer/`: recovered author archive with the evidence-matched upstream `datasets/` module restored.
- `models/Faster R-CNN/`: recovered author archive with evidence-matched upstream `nets/`, `utils/`, and `model_data/` components restored.

Each model directory follows the same publication pattern where the evidence
permits it: a model-level README, a release manifest, a reproducibility setup,
lightweight run configurations, and a checkpoint inventory under `weights/`.

## Data and model weights

The image dataset, trained checkpoints, experiment outputs, and other large binary artifacts are not stored in ordinary Git history. Selected checkpoints are published in the [`model-weights-v1`](https://github.com/23Chloe/Microplastics-Identification/releases/tag/model-weights-v1) release; model-specific `weights/README.md` files record direct URLs, sizes, and SHA-256 values. Dataset configurations use repository-relative paths and expect the corresponding images and labels under `dataset/` when the dataset is supplied separately.

## Reproducibility status

Machine-specific absolute paths were replaced with command-line arguments or repository-relative paths in the published utilities. Missing DETR and Faster R-CNN source modules were restored only where the retained files matched identified upstream revisions; unresolved run-level evidence remains explicit in the respective `ARCHIVE_NOTES.md` files.

The repository validation workflow performs dependency-free syntax and release
structure checks. It does not claim that incomplete model packages can train or
that unavailable datasets and checkpoints have been independently verified.

Evidence records:

- [`docs/MODEL_METADATA_RECOVERY.md`](docs/MODEL_METADATA_RECOVERY.md)
- [`docs/ANNOTATION_AND_SPLIT_PROVENANCE.md`](docs/ANNOTATION_AND_SPLIT_PROVENANCE.md)
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)
- [`LICENSE_SCOPE.md`](LICENSE_SCOPE.md)
