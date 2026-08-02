import argparse
import os
import json

# 标注文件所在的文件夹路径
parser = argparse.ArgumentParser(description="Count object classes in LabelMe JSON annotations.")
parser.add_argument("--input-json-folder", required=True, help="Directory containing LabelMe JSON files.")
input_json_folder = parser.parse_args().input_json_folder

# 统计各类别的字典
category_count = {}

# 获取所有标注文件
json_files = [f for f in os.listdir(input_json_folder) if f.endswith('.json')]

# 统计各类别数量
for json_file in json_files:
    json_path = os.path.join(input_json_folder, json_file)
    
    # 读取标注文件
    with open(json_path, 'r') as f:
        annotations = json.load(f)
    
    # 统计每个标注的类别
    for obj in annotations['shapes']:
        category = obj['label']  # 获取类别标签
        
        # 更新类别计数
        if category in category_count:
            category_count[category] += 1
        else:
            category_count[category] = 1

# 输出每个类别的数量
print("各类别的数量统计：")
for category, count in category_count.items():
    print(f"{category}: {count}")
