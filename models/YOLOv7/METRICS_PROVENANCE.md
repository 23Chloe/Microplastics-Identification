# YOLOv7 metric and checkpoint provenance

The archived `results.txt` files contain one validation record per epoch. The
values reported for the YOLOv7 family in manuscript Table 1 match the final
record at epoch `399/399`; they are not presented as a separate evaluation of
the released `best.pt` files.

| Model | Table 1 / final epoch | Final P | Final R | Final F1 | Final mAP@0.5 | Final mAP@0.5-0.95 | Best-fitness epoch |
|---|---:|---:|---:|---:|---:|---:|---:|
| YOLOv7 | 399/399 | 0.7883 | 0.7906 | 0.7894 | 0.8284 | 0.4887 | 399/399 |
| YOLOv7x | 399/399 | 0.8343 | 0.8286 | 0.8314 | 0.8631 | 0.5385 | 398/399 |
| YOLOv7-E6E | 399/399 | 0.8827 | 0.8394 | 0.8605 | 0.8792 | 0.5709 | 399/399 |

The training code selects `best.pt` using
`0.1 * mAP@0.5 + 0.9 * mAP@0.5-0.95`. For YOLOv7 and YOLOv7-E6E, the final
record is also the best-fitness record. For YOLOv7x, the best-fitness record is
epoch `398/399` (P 0.8349, R 0.8289, F1 0.8319, mAP@0.5 0.8631, and
mAP@0.5-0.95 0.5386), whereas Table 1 uses epoch `399/399`. The difference is
small but is retained explicitly to avoid conflating final-epoch reporting with
checkpoint selection.

No retained record demonstrates that every released `best.pt` file was
re-evaluated on an independent source-disjoint test set. Such a claim requires
a preserved split manifest and a fresh evaluation log.
