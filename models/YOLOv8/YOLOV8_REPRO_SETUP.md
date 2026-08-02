# YOLOv8 reproducibility setup

## Recovered protocol

| Setting | Value |
|---|---|
| Variants | YOLOv8n / YOLOv8s / YOLOv8m |
| Package/source version | Ultralytics 8.2.35 |
| Official source commit | `8ea945cc8e3ecbd466dde73f89ae018b3d7079f1` |
| Initialization | pretrained |
| Epochs | 400 |
| Batch size | 32 |
| Input size | 640 x 640 |
| Optimizer request | `auto` |
| Reconstructed resolved optimizer | SGD, learning rate 0.01, momentum 0.9 |
| Initial learning rate | 0.01 |
| Final learning-rate factor | 0.01 |
| Momentum | 0.937 |
| Weight decay | 0.0005 |
| Patience | 100 |
| Seed | 0 |
| Close mosaic | final 10 epochs |

The optimizer state and console log were not retained. The resolved choice can
nevertheless be reconstructed from the bundled 8.2.35 source: `auto` selects SGD
when calculated iterations exceed 10,000. With 400 epochs and the reported
training-set size, this threshold is exceeded. The same rule replaces the
requested momentum of 0.937 with 0.9 and uses learning rate 0.01. This is a
deterministic reconstruction, not a separately retained run artifact.

## Command template

Run from `models/YOLOv8` with the bundled Ultralytics 8.2.35 source:

```bash
yolo detect train model=yolov8n.pt data=data/my_data.yaml epochs=400 \
  batch=32 imgsz=640 optimizer=auto lr0=0.01 lrf=0.01 momentum=0.937 \
  weight_decay=0.0005 patience=100 seed=0 close_mosaic=10
```

Replace `yolov8n.pt` with `yolov8s.pt` or `yolov8m.pt` for the other variants.
