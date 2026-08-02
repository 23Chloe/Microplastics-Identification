# Third-party source and license notices

This repository contains project-authored pipeline code alongside redistributed
third-party model implementations. Each third-party component remains governed
by its own license.

| Component | Upstream | Recorded source boundary | License file |
|---|---|---|---|
| YOLOv5 | `ultralytics/yolov5` | Recovered source identifies as v7.0; exact commit unresolved | `models/YOLOv5/LICENSE` (AGPL-3.0) |
| YOLOv7 | `WongKinYiu/yolov7` | Commit `a207844b1ce82d204ab36d87d496728d3d2348e7` | `models/YOLOv7/LICENSE.md` (GPL-3.0) |
| YOLOv8 | `ultralytics/ultralytics` | Version 8.2.35, commit `8ea945cc8e3ecbd466dde73f89ae018b3d7079f1` | `models/YOLOv8/LICENSE` (AGPL-3.0) |
| DETR | `facebookresearch/detr` | Commit `29901c51d7fe8712168b8d0d64351170bc0f83e0` plus documented author defaults | `models/DETR-Transformer/LICENSE` (Apache-2.0) |
| Faster R-CNN | `bubbliiiing/faster-rcnn-pytorch` | Commit `d81ba09f9c961e7ae07612e638a242f18e2c50fe` plus documented author settings | `models/Faster R-CNN/LICENSE` (MIT) |

No license is inferred for model checkpoints or datasets beyond rights held by
their respective authors and sources. Release assets must retain this notice
and the model-level license files.
