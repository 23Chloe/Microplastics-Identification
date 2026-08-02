# DETR reproducibility setup

## Bundled entrypoint defaults

The following values are directly visible in `main.py`:

| Setting | Default |
|---|---|
| Backbone | ResNet-50 |
| Optimizer | AdamW |
| Learning rate | 1e-4 |
| Backbone learning rate | 1e-5 |
| Weight decay | 1e-4 |
| Batch size | 8 |
| Epochs | 400 |
| Learning-rate drop epoch | 200 |
| Seed | 42 |
| Object queries | 100 |
| Encoder / decoder layers | 6 / 6 |

These are source defaults only. The supplied archive does not retain a complete
run-specific record proving that every default was used for the benchmark.

## Verification required before an exact benchmark rerun

The missing `datasets/` package was restored from the matching official DETR
source boundary at commit `29901c51d7fe8712168b8d0d64351170bc0f83e0`.

1. Verify the dataset converter and class mapping against the archived labels.
2. Verify the exact run arguments and checkpoint role.
3. Only then run `main.py` with repository-relative data and output paths.
