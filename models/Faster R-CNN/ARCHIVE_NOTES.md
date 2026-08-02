# Faster R-CNN source archive notes

This directory contains the Faster R-CNN scripts recovered from the author
archive. Checkpoints, TensorBoard events, generated images, and VOC data are
intentionally excluded from ordinary Git history.

The author archive omitted local `nets/`, `utils/`, and `model_data/`
components. Shared retained scripts match the structure of
`bubbliiiing/faster-rcnn-pytorch` commit
`d81ba09f9c961e7ae07612e638a242f18e2c50fe`, with explicit author changes to
class paths, checkpoint paths, epoch settings, and Pillow text rendering. The
missing `nets/` and `utils/` modules and the upstream MIT license were restored
from that commit. `model_data/classes.txt` was reconstructed from the same
three-class mapping retained in the YOLO dataset configurations.

The package is now structurally complete after dependencies, data, and a
verified checkpoint are supplied. Non-English comments and runtime messages
were removed or translated without changing the recovered model configuration.
Ambiguous scratch filenames were replaced by descriptive command-line tools.
