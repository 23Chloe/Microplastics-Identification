# DETR checkpoint inventory

Checkpoint binaries are excluded from ordinary Git history. The table records
the author-archive files without inferring their role or validity.

| Archived file | Bytes | SHA-256 | Status / published URL |
|---|---:|---|---|
| `detr-r50-e632da11.pth` | 166,618,694 | `e632da11ec76ae67bac2f8579fbed3724e08dead7d200ca13e019b197784eadc` | upstream-named checkpoint; URL pending |
| `detr-r50_3.pth` | 166,688,136 | `306c04aeffa786115586aebdd3f6e5fe649a70e55d70ef45b78cc3cdc18561f9` | author-archive checkpoint; role requires verification |
| `runs/best.pth` | 797,584 | `aad0362963471d9537ce87be304aace1134d3ffb67bbaaf4be38dba201984d48` | unusually small; integrity/role requires verification |
| `runs/latest.pth` | 797,148 | `9bc65d63c1eba1c848b397aa53a29d850e6e1cc3943e72ff77e458f0f39f993a` | unusually small; integrity/role requires verification |

Do not publish any file as the definitive benchmark checkpoint until its role
and loadability have been verified with the restored source package.
