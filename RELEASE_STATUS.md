# Release status and verification boundary

## Branch policy

- `main` is the stable publication branch.
- `original-pool-batch` is the single integration branch for the recovered
  source and reproducibility package.
- Short-lived agent branches are not part of the public release structure.
- Changes from `original-pool-batch` should reach `main` through one reviewed
  pull request after the checks in this document pass.

## Package status

| Component | Source status | Run settings | Runnable now | Remaining blocker |
|---|---|---|---|---|
| YOLOv5 n/s/m | Recovered source snapshot; identifies as v7.0 | Checkpoint-backed; optimizer recovered as SGD | Yes after dependencies and data are supplied; weights are published | Exact upstream commit is absent from the checkpoint and remains unresolved |
| YOLOv7 / x / E6E | Verified replacement package | Table 1 traced to final-epoch records; released checkpoints selected by best fitness | Yes after dependencies and data are supplied; weights are published | No retained source-disjoint test re-evaluation of every released best checkpoint |
| YOLOv8 n/s/m | Official Ultralytics 8.2.35 source, commit `8ea945cc8e3ecbd466dde73f89ae018b3d7079f1` | Checkpoint-backed; `auto` reconstructed as SGD under the 8.2.35 rule | Yes after dependencies and data are supplied; weights are published | No separate optimizer state or console log was retained |
| DETR R50 | Recovered archive plus evidence-matched official `datasets/` at commit `29901c5` | Entrypoint defaults only | Structurally yes after dependencies/data; compatible candidate weight is published | Exact run-specific settings and definitive author checkpoint remain unresolved |
| Faster R-CNN R50 | Recovered archive plus evidence-matched upstream modules at commit `d81ba09` | Source-backed | Structurally yes after dependencies/data; selected weight is published | No additional run-level tuning log was retained |
| Data-processing pipeline | Deterministic source-group splitter with a written manifest | Source-backed | Syntax validated | Historical text says augmentation preceded the split; source-disjoint membership is not retained |

## Required before a reproducibility claim

1. The selected checkpoints are published in the
   [`model-weights-v1`](https://github.com/23Chloe/Microplastics-Identification/releases/tag/model-weights-v1)
   release with recorded SHA-256 values. The DETR author checkpoint remains a
   compatible candidate because its definitive benchmark-selection role is not
   independently documented.
2. Recover the exact YOLOv5 upstream source revision, if independent evidence
   exists; the checkpoint identifies SGD but its Git fields are null.
3. Retain any available YOLOv8 console log or optimizer state; SGD is currently
   a deterministic reconstruction from the 8.2.35 rule rather than a saved log.
4. Perform a source-group leakage audit or a group-aware rerun. Historical text
   says augmentation preceded the 7:2:1 split, and split membership is absent.
5. Publish the retained annotation audit table. LabelMe `5.5.0` is confirmed by
   27 retained JSON records, but the full audit trail is not yet in the repository.

See `docs/MODEL_METADATA_RECOVERY.md` and
`docs/ANNOTATION_AND_SPLIT_PROVENANCE.md` for the evidence boundary.

Unresolved values must remain explicit. They must not be reconstructed by
guessing from framework defaults.
