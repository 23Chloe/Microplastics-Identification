"""Dependency-free checks for source-group-disjoint dataset splitting."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "pipeline" / "divide_dataset.py"
SPEC = importlib.util.spec_from_file_location("divide_dataset", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def make_records() -> list:
    records = []
    for group_number in range(10):
        for tile_number in range(2):
            stem = f"source_{group_number:02d}_tile_{tile_number:02d}"
            records.append(
                MODULE.Record(
                    stem=stem,
                    group_id=f"source_{group_number:02d}",
                    image=Path(f"{stem}.jpg"),
                    annotation=Path(f"{stem}.json"),
                )
            )
    return records


def test_split_is_deterministic_and_group_disjoint() -> None:
    records = make_records()
    first = MODULE.split_groups(records, seed=0, ratios=(0.7, 0.2, 0.1))
    second = MODULE.split_groups(records, seed=0, ratios=(0.7, 0.2, 0.1))
    assert first == second
    assert set(first.values()) == {"train", "val", "test"}
    for group_id in {record.group_id for record in records}:
        assert len({first[record.group_id] for record in records if record.group_id == group_id}) == 1


if __name__ == "__main__":
    test_split_is_deterministic_and_group_disjoint()
    print("Group split test passed.")
