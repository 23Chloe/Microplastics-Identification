# YOLOv7 reproducibility setup

## Code and environment

- Upstream repository: `WongKinYiu/yolov7`
- Upstream commit: `a207844b1ce82d204ab36d87d496728d3d2348e7`
- Python: 3.9.25
- PyTorch: 1.12.1+cu113
- torchvision: 0.13.1+cu113
- CUDA runtime: 11.3
- cuDNN: 8.3.2
- GPU used: NVIDIA GeForce RTX 3090 (24 GB)

The complete package snapshot is recorded in
`requirements-repro-lock.txt`. The dataset paths in `data/my_data.yaml`
are placeholders and must be changed for the local machine.

## Architecture-specific mapping

| Model | Training configuration | Initial checkpoint | Entry point | Hyperparameters |
|---|---|---|---|---|
| YOLOv7 | `cfg/training/yolov7.yaml` | `yolov7_training.pt` | `train.py` | `data/hyp.scratch.p5.yaml` |
| YOLOv7x | `cfg/training/yolov7x.yaml` | `yolov7x_training.pt` | `train.py` | `data/hyp.scratch.p5.yaml` |
| YOLOv7-E6E | `cfg/training/yolov7-e6e.yaml` | `yolov7-e6e_training.pt` | `train_aux.py` | `data/hyp.scratch.p6.yaml` |

`train_aux.py` is mandatory for YOLOv7-E6E because this architecture has
auxiliary detection heads and uses `ComputeLossAuxOTA`.

## Fixed training protocol

- Epochs: 400
- Physical batch size: 4
- Input size: 640 x 640
- Optimizer: SGD
- Initial learning rate: 0.01
- Weight decay: 0.0005
- Warm-up: 3 epochs
- Label smoothing: 0.0
- Mosaic probability: 1.0
- MixUp probability: 0.15
- Multi-scale training: disabled
- Early stopping: not used

The P5 runs use `lrf=0.1`; the P6 YOLOv7-E6E run uses `lrf=0.2`.

## Training commands

```bash
python train.py --workers 4 --device 0 --batch-size 4 \
  --data data/my_data.yaml --img-size 640 640 \
  --cfg cfg/training/yolov7.yaml \
  --weights weights/yolov7_training.pt \
  --name paper_yolov7_640 --hyp data/hyp.scratch.p5.yaml --epochs 400
```

```bash
python train.py --workers 4 --device 0 --batch-size 4 \
  --data data/my_data.yaml --img-size 640 640 \
  --cfg cfg/training/yolov7x.yaml \
  --weights weights/yolov7x_training.pt \
  --name paper_yolov7x_640 --hyp data/hyp.scratch.p5.yaml --epochs 400
```

```bash
python train_aux.py --workers 4 --device 0 --batch-size 4 \
  --data data/my_data.yaml --img-size 640 640 \
  --cfg cfg/training/yolov7-e6e.yaml \
  --weights weights/yolov7-e6e_training.pt \
  --name paper_yolov7_e6e_640 --hyp data/hyp.scratch.p6.yaml --epochs 400
```

## Weight distribution

The correct YOLOv7x and YOLOv7-E6E checkpoints exceed GitHub's normal
100 MB per-file limit. They must be distributed through Git LFS, a GitHub
Release, or an external archival repository. Do not substitute the smaller
base-YOLOv7 checkpoints under different filenames.

See `weights/README.md` for the final weight-release checklist.
