"""Convert the three-class LabelMe annotations to COCO detection JSON."""

import argparse
import json
from pathlib import Path

from PIL import Image


CLASS_TO_ID = {"fragment": 1, "fiber": 2, "film": 3}


def convert_labelme_to_coco(json_dir: Path, images_dir: Path, output_json: Path) -> None:
    coco = {
        "images": [],
        "annotations": [],
        "categories": [
            {"id": class_id, "name": name, "supercategory": "microplastic"}
            for name, class_id in CLASS_TO_ID.items()
        ],
    }
    annotation_id = 1

    for image_id, json_path in enumerate(sorted(json_dir.glob("*.json")), start=1):
        data = json.loads(json_path.read_text(encoding="utf-8"))
        image_name = Path(data.get("imagePath") or json_path.with_suffix(".jpg").name).name
        image_path = images_dir / image_name
        if not image_path.exists():
            print(f"Warning: referenced image not found: {image_path}")
            continue

        with Image.open(image_path) as image:
            width, height = image.size
        coco["images"].append(
            {"id": image_id, "file_name": image_name, "height": height, "width": width}
        )

        for shape in data.get("shapes", []):
            label = shape.get("label")
            if label not in CLASS_TO_ID:
                print(f"Warning: unsupported class {label!r} in {json_path.name}")
                continue
            points = shape.get("points", [])
            if len(points) < 2:
                print(f"Warning: invalid shape in {json_path.name}")
                continue
            xs = [point[0] for point in points]
            ys = [point[1] for point in points]
            left, top, right, bottom = min(xs), min(ys), max(xs), max(ys)
            box_width, box_height = right - left, bottom - top
            coco["annotations"].append(
                {
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": CLASS_TO_ID[label],
                    "bbox": [left, top, box_width, box_height],
                    "area": box_width * box_height,
                    "iscrowd": 0,
                }
            )
            annotation_id += 1

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(coco, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-dir", type=Path, required=True)
    parser.add_argument("--images-dir", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    arguments = parser.parse_args()
    convert_labelme_to_coco(arguments.json_dir, arguments.images_dir, arguments.output_json)
