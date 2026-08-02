# DETR-Transformer release manifest

## Included

- Recovered model definitions and transformer utilities
- Official `datasets/` package and Apache-2.0 license restored from
  `facebookresearch/detr` commit `29901c51d7fe8712168b8d0d64351170bc0f83e0`
- `main.py`, `engine.py`, prediction scripts, Dockerfile, and requirements
- Entrypoint-default configuration record
- Archived checkpoint inventory with SHA-256 hashes

## Intentionally excluded

- `.pth` checkpoint binaries
- Generated outputs, caches, and machine-specific paths
- Dataset images and annotations

## Remaining evidence limitation

- A complete run-specific optimizer, batch, learning-rate schedule, epoch, and
  seed record independently tied to the reported benchmark result

The YAML under `runs/detr-r50/` records bundled entrypoint defaults, not a claim
that those defaults were the exact reported run settings.
