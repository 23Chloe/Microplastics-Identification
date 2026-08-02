import argparse
import os
import json
from PIL import Image

def convert_labelme_to_coco(json_dir, images_dir, output_json):
    coco_format = {
        "images": [],
        "annotations": [],
        "categories": [
            {"id": 1, "name": "fragment", "supercategory": "microplastic"},
            {"id": 2, "name": "fiber", "supercategory": "microplastic"}
        ]
    }

    annotation_id = 1
    image_id = 1

    for json_file in os.listdir(json_dir):
        if not json_file.endswith(".json"):
            continue

        with open(os.path.join(json_dir, json_file), "r") as f:
            data = json.load(f)

        # 使用 json_file 的名称（去掉 .json 后缀）来找到对应的图像
        image_file = json_file.replace(".json", ".jpg")  # 或根据实际情况调整扩展名
        image_path = os.path.join(images_dir, image_file)

        # 检查文件是否存在
        if not os.path.exists(image_path):
            print(f"Warning: Image file {image_path} not found.")
            continue

        img = Image.open(image_path)
        width, height = img.size

        coco_format["images"].append({
            "id": image_id,
            "file_name": image_file,
            "height": height,
            "width": width
        })

        for shape in data['shapes']:
            category = shape['label']
            class_id = 1 if category == 'fragment' else 2  # 将film标记为1（fragment）

            # 获取矩形的坐标
            points = shape['points']
            x_min = min(point[0] for point in points)
            y_min = min(point[1] for point in points)
            x_max = max(point[0] for point in points)
            y_max = max(point[1] for point in points)
            w = x_max - x_min
            h = y_max - y_min

            coco_format["annotations"].append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": class_id,
                "bbox": [x_min, y_min, w, h],
                "area": w * h,
                "iscrowd": 0
            })
            annotation_id += 1

        image_id += 1

    with open(output_json, "w") as f:
        json.dump(coco_format, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert LabelMe annotations to COCO JSON.")
    parser.add_argument("--json-dir", required=True, help="Directory containing LabelMe JSON files.")
    parser.add_argument("--images-dir", required=True, help="Directory containing the referenced images.")
    parser.add_argument("--output-json", required=True, help="Destination COCO annotation JSON file.")
    args = parser.parse_args()
    convert_labelme_to_coco(args.json_dir, args.images_dir, args.output_json)
