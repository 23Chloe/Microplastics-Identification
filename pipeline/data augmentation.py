import argparse
import os
import cv2
import numpy as np
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import imgaug.augmenters as iaa

# Input paths.
parser = argparse.ArgumentParser(description="Augment images and matching YOLO labels.")
parser.add_argument("--input-images", required=True, help="Directory containing source images.")
parser.add_argument("--input-labels", required=True, help="Directory containing source YOLO labels.")
parser.add_argument("--output-images", required=True, help="Directory for augmented images.")
parser.add_argument("--output-labels", required=True, help="Directory for augmented YOLO labels.")
args = parser.parse_args()

input_image_folder = args.input_images
input_label_folder = args.input_labels

# Output paths.
output_image_folder = args.output_images
output_label_folder = args.output_labels

# Create output directories.
os.makedirs(output_image_folder, exist_ok=True)
os.makedirs(output_label_folder, exist_ok=True)

# Augmentation policy.
augmenter = iaa.Sequential([
    iaa.Fliplr(0.5),                        # Horizontal flip
    iaa.Affine(scale=(0.8, 1.2), rotate=(-15, 15)),  # Scaling and rotation
    iaa.Multiply((0.8, 1.2)),               # Brightness adjustment
    iaa.Crop(percent=(0, 0.2))              # Cropping
])

for filename in os.listdir(input_image_folder):
    if not filename.lower().endswith(('.jpg', '.png')):
        continue

    img_path = os.path.join(input_image_folder, filename)
    label_filename = os.path.splitext(filename)[0] + ".txt"
    label_path = os.path.join(input_label_folder, label_filename)

    if not os.path.exists(label_path):
        continue

    # Read the image.
    image = cv2.imread(img_path)
    height, width = image.shape[:2]

    # Read the labels.
    with open(label_path, 'r') as f:
        lines = f.readlines()

    bboxes = []
    labels = []
    has_film = False

    for line in lines:
        parts = line.strip().split()
        cls, cx, cy, w, h = int(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
        x1 = (cx - w/2) * width
        y1 = (cy - h/2) * height
        x2 = (cx + w/2) * width
        y2 = (cy + h/2) * height
        bboxes.append(BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2))
        labels.append(cls)
        if cls == 2:
            has_film = True

    if not bboxes:
        continue

    bbox_container = BoundingBoxesOnImage(bboxes, shape=image.shape)

    # Select the augmentation multiplier.
    aug_num = 6 if has_film else 4

    for i in range(aug_num):
        image_aug, bbs_aug = augmenter(image=image, bounding_boxes=bbox_container)
        bbs_aug = bbs_aug.remove_out_of_image().clip_out_of_image()

        # Save the augmented image.
        out_img_name = f"aug_{i}_{filename}"
        out_img_path = os.path.join(output_image_folder, out_img_name)
        cv2.imwrite(out_img_path, image_aug)

        # Save the augmented labels.
        out_label_name = f"aug_{i}_{label_filename}"
        out_label_path = os.path.join(output_label_folder, out_label_name)

        with open(out_label_path, "w") as f:
            for idx, bb in enumerate(bbs_aug.bounding_boxes):
                cls = labels[idx]
                cx = (bb.x1 + bb.x2) / 2 / width
                cy = (bb.y1 + bb.y2) / 2 / height
                bw = (bb.x2 - bb.x1) / width
                bh = (bb.y2 - bb.y1) / height
                f.write(f"{cls} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}\n")
