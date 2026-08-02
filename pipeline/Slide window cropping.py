import argparse
import cv2
import os
import numpy as np

def axis_starts(length, patch_size, stride, edge_mode):
    """Return deterministic crop starts for one image axis."""
    if length < patch_size:
        return [0] if edge_mode == "cover" else []
    starts = list(range(0, length - patch_size + 1, stride))
    final_start = length - patch_size
    if edge_mode == "cover" and starts[-1] != final_start:
        starts.append(final_start)
    return starts


def split_image_only(image_path, output_dir, patch_size=1280, overlap=0.2, edge_mode="discard"):
    """Split one image into fixed-size patches with a configurable overlap."""
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: unable to read image: {image_path}")
        return

    height, width = image.shape[:2]
    stride = int(patch_size * (1 - overlap))
    if patch_size <= 0:
        raise ValueError("patch_size must be positive")
    if not 0 <= overlap < 1:
        raise ValueError("overlap must be in the range [0, 1)")
    if stride <= 0:
        raise ValueError("overlap produces a zero-pixel stride")
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    os.makedirs(output_dir, exist_ok=True)

    patch_id = 0
    y_starts = axis_starts(height, patch_size, stride, edge_mode)
    x_starts = axis_starts(width, patch_size, stride, edge_mode)
    for y in y_starts:
        for x in x_starts:
            patch = image[y:y + patch_size, x:x + patch_size]
            if patch.shape[:2] != (patch_size, patch_size):
                padded = np.full((patch_size, patch_size, 3), 128, dtype=np.uint8)
                padded[:patch.shape[0], :patch.shape[1]] = patch
                patch = padded
            patch_filename = os.path.join(output_dir, f'{base_name}_patch_{patch_id}_{x}_{y}.jpg')
            cv2.imwrite(patch_filename, patch)
            patch_id += 1

    print(f"{base_name}: created {patch_id} patches in {output_dir}")

def batch_split_images(input_folder, output_folder, patch_size=1280, overlap=0.2, edge_mode="discard"):
    """Process all supported images in a directory."""
    os.makedirs(output_folder, exist_ok=True)

    supported_ext = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(supported_ext)]

    if not image_files:
        print("Warning: no image files found; verify the input directory.")
        return

    for image_name in image_files:
        image_path = os.path.join(input_folder, image_name)
        split_image_only(image_path, output_folder, patch_size, overlap, edge_mode)

    print("All images have been processed.")


# =========================== User inputs ===========================

# Input image directory.
parser = argparse.ArgumentParser(description="Crop images into overlapping square tiles.")
parser.add_argument("--input-folder", required=True, help="Directory containing source images.")
parser.add_argument("--output-folder", required=True, help="Directory for cropped image tiles.")
parser.add_argument("--patch-size", type=int, default=1280, help="Square tile size in pixels.")
parser.add_argument("--overlap", type=float, default=0.2, help="Overlap fraction in the range [0, 1).")
parser.add_argument(
    "--edge-mode",
    choices=("discard", "cover"),
    default="discard",
    help="Use 'discard' for the archived full-tile behavior or 'cover' to include image edges.",
)
args = parser.parse_args()

input_folder = args.input_folder

# Output directory for image patches.
output_folder = args.output_folder

# Patch size (1280 pixels is recommended for this workflow).
patch_size = args.patch_size

# Overlap ratio (0.2 means 20% overlap).
overlap = args.overlap

# Run batch cropping.
batch_split_images(input_folder, output_folder, patch_size, overlap, args.edge_mode)




