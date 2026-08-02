# Model metadata recovery record

This document records values recovered directly from the retained checkpoints
and distinguishes them from deterministic reconstruction or unresolved fields.

## YOLOv5 n/s/m

The three retained `best.pt` checkpoints contain the following run arguments:

- optimizer request: `SGD`
- epochs: 400
- batch size: 32
- image size: 640
- `lr0`: 0.01
- `lrf`: 0.01
- momentum: 0.937
- weight decay: 0.0005
- warm-up: 3 epochs
- patience: 100
- seed: 0

The serialized optimizer state was removed from the published checkpoint
(`optimizer: null`), but the retained run-argument dictionary explicitly names
`SGD`; optimizer identity is therefore recovered. The checkpoint's Git fields
are all null (`remote`, `branch`, and `commit`), so an exact upstream commit
cannot be recovered from this evidence. The bundled source identifies itself as
YOLOv5 version 7.0, which is less specific than a commit hash.

## YOLOv8 n/s/m

All retained checkpoints report Ultralytics version `8.2.35` and preserve the
request `optimizer: auto`. The optimizer state itself was stripped. Under the
bundled 8.2.35 trainer, `auto` selects SGD when the calculated number of
iterations exceeds 10,000, otherwise AdamW. With 400 epochs and the reported
7:2:1 split of 6,785 images, the training set necessarily exceeds the threshold;
the resolved choice is therefore deterministically reconstructed as SGD.

For `auto`, Ultralytics 8.2.35 replaces the supplied momentum value with 0.9 and
uses an SGD learning rate of 0.01. Thus `momentum=0.937` is the stored request,
not the resolved optimizer momentum. This reconstruction is source- and
dataset-size-backed, but no separate console log or optimizer state was retained.

## DETR R50

The author-archive `detr-r50_3.pth` contains 458 tensors. Its classification
head has shape `[4, 256]`, consistent with three microplastic classes plus the
DETR no-object class; its query embedding has shape `[100, 256]`. The file is
therefore structurally compatible with the recovered three-class R50 model.
It does not retain a run epoch, optimizer, or model-selection log, so its role
as the definitive best checkpoint is not proven.

The two files under `runs/` are approximately 0.8 MB and do not expose a DETR
model state dictionary. They must not be published as final model weights.

## Faster R-CNN R50

Both retained `best_epoch_weights.pth` and `last_epoch_weights.pth` contain 328
tensors matching the recovered ResNet-50 Faster R-CNN structure. The classifier
score head has shape `[4, 2048]` and the localization head has shape
`[16, 2048]`, consistent with three foreground classes plus background. The
filename and architecture evidence support publishing `best_epoch_weights.pth`
as the selected archive checkpoint; the archive contains no additional
run-level tuning log.
