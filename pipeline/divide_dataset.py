import argparse
import os
import shutil
import random

# 输入和输出文件夹路径
parser = argparse.ArgumentParser(description="Split paired images and JSON annotations into train/val/test sets.")
parser.add_argument("--input-images", required=True, help="Directory containing source images.")
parser.add_argument("--input-json", required=True, help="Directory containing source JSON annotations.")
parser.add_argument("--output-root", required=True, help="Root directory for train/val/test outputs.")
args = parser.parse_args()

input_image_folder = args.input_images
input_json_folder = args.input_json

# 输出文件夹路径
output_train_image_folder = os.path.join(args.output_root, 'train', 'images')
output_train_json_folder = os.path.join(args.output_root, 'train', 'labels')
output_val_image_folder = os.path.join(args.output_root, 'val', 'images')
output_val_json_folder = os.path.join(args.output_root, 'val', 'labels')
output_test_image_folder = os.path.join(args.output_root, 'test', 'images')
output_test_json_folder = os.path.join(args.output_root, 'test', 'labels')

# 创建输出文件夹
os.makedirs(output_train_image_folder, exist_ok=True)
os.makedirs(output_train_json_folder, exist_ok=True)
os.makedirs(output_val_image_folder, exist_ok=True)
os.makedirs(output_val_json_folder, exist_ok=True)
os.makedirs(output_test_image_folder, exist_ok=True)
os.makedirs(output_test_json_folder, exist_ok=True)

# 获取所有标注文件
json_files = [f for f in os.listdir(input_json_folder) if f.endswith('.json')]

# 按照比例划分数据集
train_files = []
val_files = []
test_files = []

# 打乱文件顺序，确保划分的随机性
random.shuffle(json_files)

# 计算划分的大小
total_files = len(json_files)
train_size = int(total_files * 0.7)
val_size = int(total_files * 0.2)
test_size = total_files - train_size - val_size

# 划分文件
train_files = json_files[:train_size]
val_files = json_files[train_size:train_size + val_size]
test_files = json_files[train_size + val_size:]

# 函数：复制文件到目标文件夹
def copy_files(file_list, src_image_folder, src_json_folder, dest_image_folder, dest_json_folder):
    for file in file_list:
        json_path = os.path.join(src_json_folder, file)
        image_path = os.path.join(src_image_folder, file.replace('.json', '.jpg').replace('.json', '.png'))
        
        # 复制图像和标注文件到目标文件夹
        shutil.copy(image_path, dest_image_folder)
        shutil.copy(json_path, dest_json_folder)

# 复制训练、验证、测试数据
copy_files(train_files, input_image_folder, input_json_folder, output_train_image_folder, output_train_json_folder)
copy_files(val_files, input_image_folder, input_json_folder, output_val_image_folder, output_val_json_folder)
copy_files(test_files, input_image_folder, input_json_folder, output_test_image_folder, output_test_json_folder)

print(f"数据集划分完成！")
print(f"训练集: {len(train_files)} 个文件")
print(f"验证集: {len(val_files)} 个文件")
print(f"测试集: {len(test_files)} 个文件")
