# YOLOv5 reproducibility setup

## Recovered protocol

| Setting | Value |
|---|---|
| Variants | YOLOv5n / YOLOv5s / YOLOv5m |
| Epochs | 400 |
| Batch size | 32 |
| Input size | 640 x 640 |
| Initial learning rate | 0.01 |
| Final learning-rate factor | 0.01 |
| Momentum | 0.937 |
| Weight decay | 0.0005 |
| Warm-up | 3 epochs |
| Patience | 100 |
| Seed | 0 |
| Optimizer | SGD |

The settings above were recovered from archived checkpoint/run metadata. The
serialized optimizer state was stripped, but the retained run-argument
dictionary explicitly records `optimizer=SGD` for all three variants.

## Command template

Run from `models/YOLOv5` after placing the separately distributed initial or
resume checkpoint under `weights/`:

```bash
python train.py --data data/my_data.yaml --img 640 --batch 32 --epochs 400 \
  --cfg models/yolov5n.yaml --weights weights/<verified-initial-weight>.pt \
  --hyp data/hyps/hyp.scratch-low.yaml --patience 100 --seed 0
```

Use the corresponding `yolov5s.yaml` or `yolov5m.yaml` for the other variants.
Before claiming an exact rerun, verify that the selected hyperparameter file
reproduces `lr0=0.01`, `lrf=0.01`, momentum `0.937`, weight decay `0.0005`, and
three warm-up epochs. The exact upstream source commit remains unresolved
because the checkpoint Git fields are null.
