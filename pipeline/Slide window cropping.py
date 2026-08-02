import argparse
import cv2
import os

def split_image_only(image_path, output_dir, patch_size=1280, overlap=0.2):
    """ 仅切割单张图像为指定大小的 patch，支持设置重叠比例 """
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ 无法读取图像: {image_path}")
        return

    height, width = image.shape[:2]
    stride = int(patch_size * (1 - overlap))
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    os.makedirs(output_dir, exist_ok=True)

    patch_id = 0
    for y in range(0, height - patch_size + 1, stride):
        for x in range(0, width - patch_size + 1, stride):
            patch = image[y:y + patch_size, x:x + patch_size]
            patch_filename = os.path.join(output_dir, f'{base_name}_patch_{patch_id}_{x}_{y}.jpg')
            cv2.imwrite(patch_filename, patch)
            patch_id += 1

    print(f"✅ {base_name}: 切割为 {patch_id} 张 patch，保存至 {output_dir}")

def batch_split_images(input_folder, output_folder, patch_size=1280, overlap=0.2):
    """ 批量处理文件夹中的所有图像 """
    os.makedirs(output_folder, exist_ok=True)

    supported_ext = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(supported_ext)]

    if not image_files:
        print("⚠️ 未找到图像文件，请确认文件夹路径是否正确。")
        return

    for image_name in image_files:
        image_path = os.path.join(input_folder, image_name)
        split_image_only(image_path, output_folder, patch_size, overlap)

    print("🎉 所有图像已处理完成！")


# =========================== 🟢 你的输入区域 ===========================

# 输入图像文件夹路径（替换为你的图像所在文件夹）
parser = argparse.ArgumentParser(description="Crop images into overlapping square tiles.")
parser.add_argument("--input-folder", required=True, help="Directory containing source images.")
parser.add_argument("--output-folder", required=True, help="Directory for cropped image tiles.")
parser.add_argument("--patch-size", type=int, default=1280, help="Square tile size in pixels.")
parser.add_argument("--overlap", type=float, default=0.2, help="Overlap fraction in the range [0, 1).")
args = parser.parse_args()

input_folder = args.input_folder

# 输出 patch 保存文件夹
output_folder = args.output_folder

# patch 尺寸（建议1280）
patch_size = args.patch_size

# 重叠比例（0.2 表示 20% 重叠）
overlap = args.overlap

# 执行批量切图
batch_split_images(input_folder, output_folder, patch_size, overlap)




