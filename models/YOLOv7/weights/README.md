# Corrected model weights

The verified weights were recovered from the separate weight directory in the
final replacement package. They are excluded from ordinary Git history and
published in the `model-weights-v1` GitHub Release.

| Model | Architecture | Published download URL | SHA-256 | Parameter count |
|---|---|---|---|---:|
| YOLOv7 | `cfg/training/yolov7.yaml` | [yolov7_best.pt](https://github.com/23Chloe/Microplastics-Identification/releases/download/model-weights-v1/yolov7_best.pt) | `f1359901761d03dea3fcd70710959988b83c912d581c53bc6cd6cbade3f9e804` | 37,207,344 |
| YOLOv7x | `cfg/training/yolov7x.yaml` | [yolov7x_best.pt](https://github.com/23Chloe/Microplastics-Identification/releases/download/model-weights-v1/yolov7x_best.pt) | `2d31044a89d20d7f1ea654702736b7b26b2dd2783329d31152cee22c8bba59fb` | 70,828,568 |
| YOLOv7-E6E | `cfg/training/yolov7-e6e.yaml` | [yolov7-e6e_best.pt](https://github.com/23Chloe/Microplastics-Identification/releases/download/model-weights-v1/yolov7-e6e_best.pt) | `1339df3a0fcd5f59ba1c3040602f29313876c68c5f827c012fcc2d7b4b8c6b5d` | 164,927,712 |

The supplied files are:

- `yolov7_best.pt`
- `yolov7x_best.pt`
- `yolov7-e6e_best.pt`

Do not publish the old approximately 74.8 MB files under YOLOv7x or
YOLOv7-E6E names. Those files contain the base YOLOv7 architecture.

