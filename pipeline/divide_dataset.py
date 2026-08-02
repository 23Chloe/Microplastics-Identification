import argparse
import os
import shutil
import random
from pathlib import Path

# Input directories.
parser = argparse.ArgumentParser(description="Split paired images and JSON annotations into train/val/test sets.")
parser.add_argument("--input-images", required=True, help="Directory containing source images.")
parser.add_argument("--input-json", required=True, help="Directory containing source JSON annotations.")
parser.add_argument("--output-root", required=True, help="Root directory for train/val/test outputs.")
parser.add_argument("--seed", type=int, default=0, help="Random seed used for a reproducible split.")
args = parser.parse_args()

input_image_folder = args.input_images
input_json_folder = args.input_json

# Output directories.
output_train_image_folder = os.path.join(args.output_root, 'train', 'images')
output_train_json_folder = os.path.join(args.output_root, 'train', 'labels')
output_val_image_folder = os.path.join(args.output_root, 'val', 'images')
output_val_json_folder = os.path.join(args.output_root, 'val', 'labels')
output_test_image_folder = os.path.join(args.output_root, 'test', 'images')
output_test_json_folder = os.path.join(args.output_root, 'test', 'labels')

# Create output directories.
os.makedirs(output_train_image_folder, exist_ok=True)
os.makedirs(output_train_json_folder, exist_ok=True)
os.makedirs(output_val_image_folder, exist_ok=True)
os.makedirs(output_val_json_folder, exist_ok=True)
os.makedirs(output_test_image_folder, exist_ok=True)
os.makedirs(output_test_json_folder, exist_ok=True)

# Collect all annotation files.
json_files = sorted(f for f in os.listdir(input_json_folder) if f.lower().endswith('.json'))

# Dataset split ratios.
train_files = []
val_files = []
test_files = []

# Shuffle the files to randomize the split.
random.Random(args.seed).shuffle(json_files)

# Calculate split sizes.
total_files = len(json_files)
train_size = int(total_files * 0.7)
val_size = int(total_files * 0.2)
test_size = total_files - train_size - val_size

# Split the file list.
train_files = json_files[:train_size]
val_files = json_files[train_size:train_size + val_size]
test_files = json_files[train_size + val_size:]

# Copy paired image and annotation files to a destination split.
def resolve_image(src_image_folder, annotation_name):
    stem = Path(annotation_name).stem
    matches = [
        Path(src_image_folder) / f"{stem}{extension}"
        for extension in (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")
    ]
    existing = [path for path in matches if path.is_file()]
    if len(existing) != 1:
        raise FileNotFoundError(
            f"Expected exactly one image for {annotation_name}; found {len(existing)}: {existing}"
        )
    return existing[0]


def copy_files(file_list, src_image_folder, src_json_folder, dest_image_folder, dest_json_folder):
    for file in file_list:
        json_path = os.path.join(src_json_folder, file)
        image_path = resolve_image(src_image_folder, file)
        
        # Copy the image and its annotation file.
        shutil.copy2(image_path, dest_image_folder)
        shutil.copy2(json_path, dest_json_folder)

# Populate the training, validation, and test splits.
copy_files(train_files, input_image_folder, input_json_folder, output_train_image_folder, output_train_json_folder)
copy_files(val_files, input_image_folder, input_json_folder, output_val_image_folder, output_val_json_folder)
copy_files(test_files, input_image_folder, input_json_folder, output_test_image_folder, output_test_json_folder)

print("Dataset split completed.")
print(f"Training set: {len(train_files)} files")
print(f"Validation set: {len(val_files)} files")
print(f"Test set: {len(test_files)} files")
