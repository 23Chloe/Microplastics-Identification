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

## Restoration required before training

1. Restore the exact `datasets/` package version matching this source snapshot.
2. Verify the dataset converter and class mapping against the archived labels.
3. Verify the exact run arguments and checkpoint role.
4. Only then run `main.py` with repository-relative data and output paths.
