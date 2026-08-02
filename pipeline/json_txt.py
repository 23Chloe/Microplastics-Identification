import argparse
import os
import json
from PIL import Image
from collections import defaultdict

# === Path configuration ===
parser = argparse.ArgumentParser(description="Convert LabelMe JSON annotations to YOLO text labels.")
parser.add_argument("--json-folder", required=True, help="Directory containing LabelMe JSON files.")
parser.add_argument("--image-folder", required=True, help="Directory containing the referenced images.")
parser.add_argument("--label-output", required=True, help="Directory for YOLO text labels.")
args = parser.parse_args()

json_folder = args.json_folder
image_folder = args.image_folder
label_output = args.label_output

os.makedirs(label_output, exist_ok=True)

# Class mapping
label_map = {
    "fragment": 0,
    "fiber": 1,
    "film": 2
}

# Keep the film class separate.
merge_film_to_fragment = False

# Class counter
class_counts = defaultdict(int)

def convert_shape_to_yolo(shape, img_w, img_h):
    points = shape['points']
    xmin = min(p[0] for p in points)
    xmax = max(p[0] for p in points)
    ymin = min(p[1] for p in points)
    ymax = max(p[1] for p in points)

    x_center = (xmin + xmax) / 2.0 / img_w
    y_center = (ymin + ymax) / 2.0 / img_h
    width = (xmax - xmin) / img_w
    height = (ymax - ymin) / img_h

    # Clamp normalized coordinates to the [0, 1] range.
    x_center = min(max(x_center, 0), 1)
    y_center = min(max(y_center, 0), 1)
    width = min(max(width, 0), 1)
    height = min(max(height, 0), 1)

    return x_center, y_center, width, height

converted_count = 0

for file in os.listdir(json_folder):
    if not file.endswith('.json'):
        continue
    json_path = os.path.join(json_folder, file)
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    image_path = os.path.join(image_folder, data['imagePath'])
    if not os.path.exists(image_path):
        print(f"Warning: image file does not exist: {image_path}")
        continue

    img = Image.open(image_path)
    img_w, img_h = img.size

    txt_lines = []

    for shape in data['shapes']:
        label_name = shape['label']
        
        # Preserve the original class instead of merging film labels.
        if label_name not in label_map:
            print(f"Warning: unknown class '{label_name}'; skipping it.")
            continue
        
        class_id = label_map[label_name]
        x_center, y_center, width, height = convert_shape_to_yolo(shape, img_w, img_h)
        txt_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
        class_counts[label_name] += 1

    # Write the converted label file.
    base_name = os.path.splitext(file)[0]
    txt_path = os.path.join(label_output, base_name + ".txt")
    with open(txt_path, 'w') as f:
        f.write('\n'.join(txt_lines))

    converted_count += 1

# Report conversion results.
print(f"\nSuccessfully converted JSON files: {converted_count}")
print(f"Label output directory: {label_output}")
print("\nAnnotation count by class:")
for cls, count in class_counts.items():
    print(f" - {cls:<10}: {count} annotations")
