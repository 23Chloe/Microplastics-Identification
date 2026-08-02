YOLOv7 Corrected Retraining Environment
=======================================

Scope
-----
This file documents the environment used for the corrected YOLOv7,
YOLOv7x, and YOLOv7-E6E supplementary experiments. It is not claimed to
be the historical environment used for every model in the original study.

Hardware and platform
---------------------
Operating system: Windows 64-bit
GPU: NVIDIA GeForce RTX 3090
GPU memory: 24576 MiB (24 GB)
NVIDIA driver at verification: 610.62

Core software
-------------
Python: 3.9.25
PyTorch: 1.12.1+cu113
torchvision: 0.13.1+cu113
CUDA runtime bundled with PyTorch: 11.3
cuDNN: 8.3.2
NumPy: 1.23.5
OpenCV-Python: 4.11.0.86
Pillow: 9.5.0

Repository
----------
Repository: WongKinYiu/yolov7
Git commit: a207844b1ce82d204ab36d87d496728d3d2348e7

Architecture and training entry point
-------------------------------------
YOLOv7:
  configuration: cfg/training/yolov7.yaml
  training entry point: train.py

YOLOv7x:
  configuration: cfg/training/yolov7x.yaml
  training entry point: train.py

YOLOv7-E6E:
  configuration: cfg/training/yolov7-e6e.yaml
  training entry point: train_aux.py

Reproduction files
------------------
Full package lock: requirements-repro-lock.txt
Training protocol and commands: YOLOV7_REPRO_SETUP.md

Notes
-----
1. Dataset paths are intentionally not machine-specific in this package.
2. The model configuration file determines the architecture. Loading a
   differently named checkpoint alone does not change the architecture.
3. Large checkpoints require Git LFS, GitHub Releases, or external archival
   storage; see weights/README.md.
