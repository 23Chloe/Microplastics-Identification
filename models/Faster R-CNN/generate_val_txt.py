import os
import random


VOCdevkit_path = 'VOCdevkit'
trainval_txt_path = os.path.join(VOCdevkit_path, 'VOC2007/ImageSets/Main/trainval.txt')
val_txt_path = os.path.join(VOCdevkit_path, 'VOC2007/ImageSets/Main/2007_val.txt')
train_txt_path = os.path.join(VOCdevkit_path, 'VOC2007/ImageSets/Main/2007_train.txt')


with open(trainval_txt_path, 'r') as f:
    lines = f.readlines()


val_ratio = 0.2


random.shuffle(lines)


num_val = int(len(lines) * val_ratio)


val_lines = lines[:num_val]
train_lines = lines[num_val:]


with open(val_txt_path, 'w') as f:
    f.writelines(val_lines)


with open(train_txt_path, 'w') as f:
    f.writelines(train_lines)

print(f"Generated {val_txt_path} with {len(val_lines)} images.")
print(f"Generated {train_txt_path} with {len(train_lines)} images.")
