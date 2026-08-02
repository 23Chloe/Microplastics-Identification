import os
import random

# 配置文件路径
VOCdevkit_path = 'VOCdevkit'
trainval_txt_path = os.path.join(VOCdevkit_path, 'VOC2007/ImageSets/Main/trainval.txt')
val_txt_path = os.path.join(VOCdevkit_path, 'VOC2007/ImageSets/Main/2007_val.txt')
train_txt_path = os.path.join(VOCdevkit_path, 'VOC2007/ImageSets/Main/2007_train.txt')

# 读取 trainval.txt 文件
with open(trainval_txt_path, 'r') as f:
    lines = f.readlines()

# 设定验证集比例
val_ratio = 0.2

# 打乱数据
random.shuffle(lines)

# 计算验证集的大小
num_val = int(len(lines) * val_ratio)

# 将数据划分为训练集和验证集
val_lines = lines[:num_val]
train_lines = lines[num_val:]

# 保存验证集到 2007_val.txt
with open(val_txt_path, 'w') as f:
    f.writelines(val_lines)

# 保存训练集到 2007_train.txt
with open(train_txt_path, 'w') as f:
    f.writelines(train_lines)

print(f"Generated {val_txt_path} with {len(val_lines)} images.")
print(f"Generated {train_txt_path} with {len(train_lines)} images.")
