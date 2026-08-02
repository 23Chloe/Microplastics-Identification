# Annotation and dataset-split provenance

This record separates file-backed evidence from author-supplied procedural
information. It does not retroactively claim that the historical benchmark was
free of same-source image leakage.

## File-backed annotation evidence

- Twenty-seven retained LabelMe JSON records were found in the author archive.
- Every retained record reports LabelMe version `5.5.0`.
- Their `imagePath` fields use relative paths such as `../images/<file>.jpg`.
- The retained JSON subset is evidence of the annotation software version, but
  it is not a complete annotation audit trail for the full dataset.

## Author-supplied blind-review procedure

The initial model development and annotation were completed before independent
review. Two assessors then reviewed a 10% sample from every sampling site while
blinded to the model result. Review agreement across sites ranged from 87% to
99%. Discrepancies were adjudicated and consolidated into the false-negative
record. The observed false-positive disagreements were concentrated in the
fiber class.

The numerical audit summary and per-particle adjudication table have not yet
been located in the repository. Until those retained records are published,
the procedure above is an author-supplied statement rather than a
repository-reproducible audit.

## Historical split-order evidence and leakage risk

Surviving manuscript versions state that augmentation expanded the dataset to
6,785 images and that the expanded dataset was then divided into training,
validation, and test sets at a 7:2:1 ratio. The supplied dataset archive contains
6,722 tiled images and 6,722 labels, but it does not retain train/validation/test
membership or a mapping from every augmented derivative to its source image.

Consequently, the historical archive cannot currently demonstrate that
derivatives of one source image were confined to a single split. The reported
historical benchmark must therefore be treated as having an unresolved
same-source leakage risk. The portable pipeline now documents a prospective
safe workflow: assign source groups to splits first, and augment only within the
training split. This prospective safeguard does not validate the historical
benchmark retroactively.

## Records still required

1. A source-image-to-tile/augmentation lineage table.
2. The historical train, validation, and test membership manifests.
3. The retained blind-review sampling list and adjudication record.
4. A group-aware re-audit or rerun if the historical split cannot be proven
   source-disjoint.
