# Faster R-CNN model weights

The supplied checkpoints are excluded from ordinary Git history. Publish them
with Git LFS, a GitHub Release, or a stable external archive, then replace the
URL placeholders below.

| Archived file | Bytes | SHA-256 | Published URL |
|---|---:|---|---|
| `runs/best_epoch_weights.pth` | 113,510,182 | `786ae32dab7eff26f5c796a2712409e3f9dab8a4d2e3d731f2f2abd4c957c402` | Add after publishing |
| `runs/last_epoch_weights.pth` | 113,510,182 | `8f8fddb1e6ad405683e3ae65c11677c192b050853a29ba26962aaed72c976b8f` | Add after publishing |

Hashes were calculated from the author-supplied archive before publication.
Both files contain 328 tensors matching the recovered ResNet-50 Faster R-CNN
implementation and its three-class-plus-background output heads. Publish the
`best_epoch_weights.pth` file as the selected archive checkpoint; retain the
last-epoch file only as an optional recovery artifact.
