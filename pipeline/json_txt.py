import argparse
import os
import json
from PIL import Image
from collections import defaultdict

# === 路径配置 ===
parser = argparse.ArgumentParser(description="Convert LabelMe JSON annotations to YOLO text labels.")
parser.add_argument("--json-folder", required=True, help="Directory containing LabelMe JSON files.")
parser.add_argument("--image-folder", required=True, help="Directory containing the referenced images.")
parser.add_argument("--label-output", required=True, help="Directory for YOLO text labels.")
args = parser.parse_args()

json_folder = args.json_folder
image_folder = args.image_folder
label_output = args.label_output

os.makedirs(label_output, exist_ok=True)

# 类别映射
label_map = {
    "fragment": 0,
    "fiber": 1,
    "film": 2
}

# 不合并 film 类别
merge_film_to_fragment = False

# 类别计数器
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

    # 裁剪到 0~1 范围内
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
        print(f"⚠️ 图像文件不存在: {image_path}")
        continue

    img = Image.open(image_path)
    img_w, img_h = img.size

    txt_lines = []

    for shape in data['shapes']:
        label_name = shape['label']
        
        # 不合并 film 类别，直接使用原始类别
        if label_name not in label_map:
            print(f"⚠️ 未知类别: {label_name}，跳过")
            continue
        
        class_id = label_map[label_name]
        x_center, y_center, width, height = convert_shape_to_yolo(shape, img_w, img_h)
        txt_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
        class_counts[label_name] += 1

    # 写入标签文件
    base_name = os.path.splitext(file)[0]
    txt_path = os.path.join(label_output, base_name + ".txt")
    with open(txt_path, 'w') as f:
        f.write('\n'.join(txt_lines))

    converted_count += 1

# 输出信息
print(f"\n✅ 成功转换 JSON 文件数量：{converted_count}")
print(f"📌 标签输出路径：{label_output}")
print("\n📊 各类别数量统计：")
for cls, count in class_counts.items():
    print(f" - {cls:<10} : {count} 个标注")
