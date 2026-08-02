# Faster R-CNN model weights

The selected checkpoint is excluded from ordinary Git history and published in
the `model-weights-v1` GitHub Release.

| Archived file | Bytes | SHA-256 | Published URL |
|---|---:|---|---|
| `runs/best_epoch_weights.pth` | 113,510,182 | `786ae32dab7eff26f5c796a2712409e3f9dab8a4d2e3d731f2f2abd4c957c402` | [faster_rcnn_resnet50_best.pth](https://github.com/23Chloe/Microplastics-Identification/releases/download/model-weights-v1/faster_rcnn_resnet50_best.pth) |
| `runs/last_epoch_weights.pth` | 113,510,182 | `8f8fddb1e6ad405683e3ae65c11677c192b050853a29ba26962aaed72c976b8f` | Not published; optional recovery artifact, not the selected checkpoint |

Hashes were calculated from the author-supplied archive before publication.
Both files contain 328 tensors matching the recovered ResNet-50 Faster R-CNN
implementation and its three-class-plus-background output heads. Publish the
`best_epoch_weights.pth` file as the selected archive checkpoint; retain the
last-epoch file only as an optional recovery artifact.
