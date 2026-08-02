# Faster R-CNN source archive notes

This directory contains the Faster R-CNN scripts recovered from the author
archive. Checkpoints, TensorBoard events, generated images, and VOC data are
intentionally excluded from ordinary Git history.

The recovered scripts import local `nets/`, `utils/`, and `model_data/`
components that were not present in the supplied source archive. These files
therefore document the archived
training and evaluation settings but are not yet a standalone runnable package.
The missing components must be restored and matched to the archived scripts
before claiming complete code reproducibility.
