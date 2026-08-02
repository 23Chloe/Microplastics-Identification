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

These values are directly encoded in `train.py`. The missing local modules were
restored from the evidence-matched upstream commit
`d81ba09f9c961e7ae07612e638a242f18e2c50fe`, and the three-class mapping is
included. A verified final checkpoint and dataset are still required for a run.
