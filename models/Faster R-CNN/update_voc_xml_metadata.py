"""Update VOC XML filename, folder, and path metadata."""

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path


def update_metadata(xml_folder: Path, image_folder: Path, absolute_paths: bool) -> None:
    for xml_path in sorted(xml_folder.glob("*.xml")):
        image_name = f"{xml_path.stem}.jpg"
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for element in root.iter("filename"):
            element.text = image_name
        for element in root.iter("folder"):
            element.text = image_folder.name
        for element in root.iter("path"):
            image_path = image_folder / image_name
            element.text = str(image_path.resolve() if absolute_paths else image_path.as_posix())
        tree.write(xml_path, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xml-folder", type=Path, required=True)
    parser.add_argument("--image-folder", type=Path, required=True)
    parser.add_argument(
        "--absolute-paths",
        action="store_true",
        help="Write machine-specific absolute image paths instead of portable relative paths.",
    )
    arguments = parser.parse_args()
    update_metadata(arguments.xml_folder, arguments.image_folder, arguments.absolute_paths)
    print("VOC XML metadata updated.")
