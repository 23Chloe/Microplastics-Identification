import argparse
import os
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description="Inspect VOC XML annotations against an image directory.")
parser.add_argument("--xml-folder", required=True, help="Directory containing VOC XML annotations.")
parser.add_argument("--image-folder", required=True, help="Directory containing the corresponding images.")
args = parser.parse_args()
xml_folder = args.xml_folder
image_folder = args.image_folder

# 遍历 XML 文件夹
for xml_file in os.listdir(xml_folder):
    if xml_file.endswith(".xml"):
        xml_path = os.path.join(xml_folder, xml_file)

        # 解析 XML 文件
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 找到 <filename> 标签并更新内容
        for elem in root.iter("filename"):
            # 获取对应的图像文件名
            base_filename = os.path.splitext(xml_file)[0]
            image_extension = ".jpg"  # 根据实际情况修改扩展名
            new_filename = base_filename + image_extension
            elem.text = new_filename  # 更新 <filename> 标签

        # 更新 <folder> 标签内容
        for elem in root.iter("folder"):
            elem.text = "JPEGImages"  # 修改为实际的文件夹名称

        # 更新 <path> 标签内容
        for elem in root.iter("path"):
            image_path = os.path.join(image_folder, new_filename)
            elem.text = os.path.abspath(image_path)  # 获取图像文件的绝对路径

        # 保存更新后的 XML 文件
        tree.write(xml_path, encoding="utf-8")

print("XML 文件中的 <filename>、<folder> 和 <path> 标签已更新完成。")
