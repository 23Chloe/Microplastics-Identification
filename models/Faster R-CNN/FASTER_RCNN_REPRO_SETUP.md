# Faster R-CNN reproducibility setup

## Recovered training protocol

| Setting | Value |
|---|---|
| Backbone | ResNet-50 |
| Input size | 600 x 600 |
| Optimizer | Adam |
| Initial learning rate | 1e-4 |
| Minimum learning rate | 1e-6 |
| Scheduler | cosine |
| Frozen stage | epochs 0-19, batch size 4 |
| Unfrozen stage | epochs 20-149, batch size 2 |
| Weight decay | 0 |
| Seed | 11 |

These values are directly encoded in `train.py`. Before running the script,
restore and verify the missing `nets/`, `utils/`, and `model_data/` directories
from the exact source version used by the authors. Do not mix arbitrary newer
implementations into this archive and call the result an exact reproduction.
