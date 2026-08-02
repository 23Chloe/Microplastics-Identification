"""Create a deterministic, source-group-disjoint train/val/test split."""

from __future__ import annotations

import argparse
import csv
import random
import shutil
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")


@dataclass(frozen=True)
class Record:
    stem: str
    group_id: str
    image: Path
    annotation: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Split paired images and JSON annotations while keeping every tile "
            "or derivative from the same original image or membrane in one subset."
        )
    )
    parser.add_argument("--input-images", required=True, type=Path)
    parser.add_argument("--input-json", required=True, type=Path)
    parser.add_argument("--groups-csv", required=True, type=Path,
                        help="CSV with columns stem and group_id.")
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--train-ratio", type=float, default=0.7)
    parser.add_argument("--val-ratio", type=float, default=0.2)
    parser.add_argument("--test-ratio", type=float, default=0.1)
    return parser.parse_args()


def load_groups(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not {"stem", "group_id"}.issubset(reader.fieldnames):
            raise ValueError("groups CSV must contain stem and group_id columns")
        mapping: dict[str, str] = {}
        for row_number, row in enumerate(reader, start=2):
            stem = Path(row["stem"].strip()).stem
            group_id = row["group_id"].strip()
            if not stem or not group_id:
                raise ValueError(f"blank stem or group_id at CSV row {row_number}")
            if stem in mapping and mapping[stem] != group_id:
                raise ValueError(f"conflicting group assignments for {stem}")
            mapping[stem] = group_id
    return mapping


def resolve_image(folder: Path, stem: str) -> Path:
    matches = [folder / f"{stem}{extension}" for extension in IMAGE_EXTENSIONS]
    existing = [path for path in matches if path.is_file()]
    if len(existing) != 1:
        raise FileNotFoundError(
            f"Expected exactly one image for {stem}; found {len(existing)}: {existing}"
        )
    return existing[0]


def build_records(images: Path, annotations: Path, groups: dict[str, str]) -> list[Record]:
    annotation_paths = sorted(annotations.glob("*.json"))
    if not annotation_paths:
        raise ValueError(f"No JSON annotations found in {annotations}")
    records: list[Record] = []
    missing_groups: list[str] = []
    for annotation in annotation_paths:
        stem = annotation.stem
        if stem not in groups:
            missing_groups.append(stem)
            continue
        records.append(Record(stem, groups[stem], resolve_image(images, stem), annotation))
    if missing_groups:
        preview = ", ".join(missing_groups[:10])
        raise ValueError(f"Missing source-group assignments for {len(missing_groups)} stems: {preview}")
    return records


def split_groups(records: list[Record], seed: int, ratios: tuple[float, float, float]) -> dict[str, str]:
    if any(ratio <= 0 for ratio in ratios) or abs(sum(ratios) - 1.0) > 1e-9:
        raise ValueError("train/val/test ratios must be positive and sum to 1")
    grouped: dict[str, list[Record]] = defaultdict(list)
    for record in records:
        grouped[record.group_id].append(record)
    group_ids = sorted(grouped)
    if len(group_ids) < 3:
        raise ValueError("At least three independent source groups are required")
    random.Random(seed).shuffle(group_ids)

    targets = [len(records) * ratio for ratio in ratios]
    split_names = ("train", "val", "test")
    assignments: dict[str, str] = {}
    current_split = 0
    current_counts = [0, 0, 0]
    for index, group_id in enumerate(group_ids):
        remaining_groups = len(group_ids) - index
        remaining_splits = 2 - current_split
        if current_split < 2 and (
            remaining_groups <= remaining_splits
            or (
                current_counts[current_split] >= targets[current_split]
                and remaining_groups > remaining_splits
            )
        ):
            current_split += 1
        assignments[group_id] = split_names[current_split]
        current_counts[current_split] += len(grouped[group_id])

    if set(assignments.values()) != set(split_names):
        raise ValueError("The group allocation produced an empty subset; provide more source groups")
    return assignments


def ensure_empty_destination(root: Path) -> None:
    for split in ("train", "val", "test"):
        split_root = root / split
        if split_root.exists() and any(split_root.rglob("*")):
            raise FileExistsError(f"Destination is not empty: {split_root}")


def write_split(records: list[Record], assignments: dict[str, str], output_root: Path) -> None:
    ensure_empty_destination(output_root)
    manifest_rows: list[dict[str, str]] = []
    for record in records:
        split = assignments[record.group_id]
        image_destination = output_root / split / "images" / record.image.name
        annotation_destination = output_root / split / "labels" / record.annotation.name
        image_destination.parent.mkdir(parents=True, exist_ok=True)
        annotation_destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(record.image, image_destination)
        shutil.copy2(record.annotation, annotation_destination)
        manifest_rows.append(
            {
                "stem": record.stem,
                "group_id": record.group_id,
                "split": split,
                "image": image_destination.relative_to(output_root).as_posix(),
                "annotation": annotation_destination.relative_to(output_root).as_posix(),
            }
        )

    manifest_path = output_root / "split_manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=("stem", "group_id", "split", "image", "annotation")
        )
        writer.writeheader()
        writer.writerows(sorted(manifest_rows, key=lambda row: (row["split"], row["group_id"], row["stem"])))

    split_groups_seen: dict[str, set[str]] = defaultdict(set)
    for group_id, split in assignments.items():
        split_groups_seen[split].add(group_id)
    if any(split_groups_seen[left] & split_groups_seen[right]
           for left, right in (("train", "val"), ("train", "test"), ("val", "test"))):
        raise RuntimeError("Source-group leakage detected after assignment")

    for split in ("train", "val", "test"):
        count = sum(row["split"] == split for row in manifest_rows)
        print(f"{split}: {count} files from {len(split_groups_seen[split])} source groups")
    print(f"Split manifest: {manifest_path}")


def main() -> None:
    args = parse_args()
    groups = load_groups(args.groups_csv)
    records = build_records(args.input_images, args.input_json, groups)
    assignments = split_groups(
        records,
        args.seed,
        (args.train_ratio, args.val_ratio, args.test_ratio),
    )
    write_split(records, assignments, args.output_root)


if __name__ == "__main__":
    main()
