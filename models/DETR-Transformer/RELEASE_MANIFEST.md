# DETR-Transformer release manifest

## Included

- Recovered model definitions and transformer utilities
- `main.py`, `engine.py`, prediction scripts, Dockerfile, and requirements
- Entrypoint-default configuration record
- Archived checkpoint inventory with SHA-256 hashes

## Intentionally excluded

- `.pth` checkpoint binaries
- Generated outputs, caches, and machine-specific paths
- Dataset images and annotations

## Missing from the supplied archive

- The local `datasets/` package imported by `main.py` and `engine.py`
- A complete run-specific optimizer, batch, learning-rate schedule, epoch, and
  seed record independently tied to the reported benchmark result

The YAML under `runs/detr-r50/` records bundled entrypoint defaults, not a claim
that those defaults were the exact reported run settings.
