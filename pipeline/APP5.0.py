import argparse
import os
import cv2
import torch
import numpy as np
import pandas as pd
import time
from collections import defaultdict

# 适合不同像素大小的图像，根据1280*1280的大小进行裁剪和填充，再识别，统计识别结果，拼接识别结果图
#成功应用于泛化数据集的检测和识别效果分析-20251031
# === 1. 参数设置 ===
parser = argparse.ArgumentParser(description="Run tiled YOLOv5 inference on filter-membrane images.")
parser.add_argument("--model-path", required=True, help="Path to the trained YOLOv5 .pt weight file.")
parser.add_argument("--input-folder", required=True, help="Directory containing input images.")
parser.add_argument("--output-folder", required=True, help="Directory used for detection results.")
parser.add_argument("--tile-size", type=int, default=1280, help="Square tile size in pixels.")
args = parser.parse_args()

model_path = args.model_path
input_folder = args.input_folder
output_base_folder = args.output_folder
tile_size = args.tile_size
os.makedirs(output_base_folder, exist_ok=True)

# === 2. 加载模型 ===
print("🔄 加载模型中...")
start_load_time = time.time()
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, trust_repo=True)
model.conf = 0.25  # 置信度阈值
load_time = time.time() - start_load_time
print(f"✅ 模型加载完成，耗时: {load_time:.2f} 秒")

# 定义类别颜色映射
class_colors = {
    'fragment': (0, 255, 0),    # 绿色
    'fiber': (255, 0, 0),       # 蓝色
    'lament': (0, 0, 255),      # 红色
    # 添加其他类别...
}

def draw_detection(image, bbox, class_name, confidence, color):
    """绘制检测框和标签，保持框内完全透明"""
    xmin, ymin, xmax, ymax = bbox
    
    # 确保坐标是整数
    xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
    
    # 只绘制边界框（空心矩形）
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
    
    # 准备标签文本
    label = f"{class_name} {confidence:.2f}"
    
    # 计算标签文本大小
    (label_width, label_height), baseline = cv2.getTextSize(
        label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
    )
    
    # 绘制标签背景（在框上方）
    label_y = max(ymin - 5, label_height + 5)
    cv2.rectangle(image,
                 (xmin, label_y - label_height - 5),
                 (xmin + label_width, label_y),
                 color, -1)  # 填充标签背景
    
    # 绘制标签文本
    cv2.putText(image, label,
               (xmin, label_y - 5),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# === 3. 遍历图像 ===
total_images = 0
total_processing_time = 0

for file in os.listdir(input_folder):
    if not file.lower().endswith(('.jpg', '.png', '.jpeg', '.bmp', '.tif')):
        continue

    total_images += 1
    image_start_time = time.time()
    
    input_image_path = os.path.join(input_folder, file)
    filename = os.path.splitext(file)[0]
    output_img_folder = os.path.join(output_base_folder, filename)
    os.makedirs(output_img_folder, exist_ok=True)
    output_csv_path = os.path.join(output_img_folder, "统计结果.csv")
    output_time_csv_path = os.path.join(output_img_folder, "时间统计.csv")

    print(f"\n🔄 处理图像: {file}")

    # === 4. 读取图像 ===
    img = cv2.imread(input_image_path)
    if img is None:
        print(f"❌ 无法读取图像：{input_image_path}")
        continue

    h, w = img.shape[:2]
    
    # === 5. 计算切割的行列数 ===
    rows = (h + tile_size - 1) // tile_size  # 向上取整
    cols = (w + tile_size - 1) // tile_size  # 向上取整
    
    print(f"📏 图像尺寸: {w}x{h}, 切割为 {rows}x{cols} 个瓦片")

    # === 6. 切割和填充 ===
    sub_images, positions, padding_info = [], [], []
    
    for i in range(rows):
        for j in range(cols):
            # 计算当前瓦片的起始和结束坐标
            y1 = i * tile_size
            x1 = j * tile_size
            y2 = min((i + 1) * tile_size, h)
            x2 = min((j + 1) * tile_size, w)
            
            # 提取原始瓦片
            original_tile = img[y1:y2, x1:x2]
            tile_h, tile_w = original_tile.shape[:2]
            
            # 如果需要填充
            if tile_h < tile_size or tile_w < tile_size:
                # 创建1280x1280的灰色背景（比黑色更好）
                padded_tile = np.full((tile_size, tile_size, 3), 128, dtype=np.uint8)
                # 将原始瓦片放在左上角
                padded_tile[:tile_h, :tile_w] = original_tile
                padding_flag = True
            else:
                padded_tile = original_tile
                padding_flag = False
            
            sub_images.append(padded_tile)
            positions.append((i, j, y1, x1, y2, x2))
            padding_info.append((padding_flag, tile_h, tile_w))

    # === 7. 识别和渲染 ===
    results_list, result_images = [], []
    all_detections = []  # 存储所有检测结果用于后续拼接
    tile_times = []  # 存储每个瓦片的处理时间

    for idx, (tile, pos_info, pad_info) in enumerate(zip(sub_images, positions, padding_info)):
        i, j, y1, x1, y2, x2 = pos_info
        padding_flag, tile_h, tile_w = pad_info
        
        print(f"🔍 处理瓦片 ({i},{j})...")
        tile_start_time = time.time()
        
        # 保存切割的瓦片
        tile_path = os.path.join(output_img_folder, f"{filename}_tile_{i}_{j}.jpg")
        cv2.imwrite(tile_path, tile)

        # 进行目标检测 - 使用内存中的图像而不是文件路径
        try:
            # 使用RGB格式进行检测
            tile_rgb = cv2.cvtColor(tile, cv2.COLOR_BGR2RGB)
            results = model(tile_rgb)
            detections = results.pandas().xyxy[0]
        except Exception as e:
            print(f"❌ 检测失败: {e}")
            continue
            
        class_counts = defaultdict(int)
        
        # 处理检测结果
        tile_detections = []
        for _, row in detections.iterrows():
            cls_name = row['name']
            confidence = row['confidence']
            xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']
            
            # 如果进行了填充，需要过滤掉填充区域的检测结果
            if padding_flag:
                # 只保留在原始瓦片区域内的检测框
                if (xmin < tile_w and ymin < tile_h and 
                    xmax > 0 and ymax > 0):
                    # 裁剪检测框到原始瓦片范围内
                    xmin = max(0, xmin)
                    ymin = max(0, ymin)
                    xmax = min(tile_w, xmax)
                    ymax = min(tile_h, ymax)
                    
                    # 转换坐标回原始图像坐标系
                    orig_xmin = xmin + x1
                    orig_ymin = ymin + y1
                    orig_xmax = xmax + x1
                    orig_ymax = ymax + y1
                    
                    class_counts[cls_name] += 1
                    tile_detections.append({
                        'class': cls_name,
                        'confidence': confidence,
                        'bbox': [orig_xmin, orig_ymin, orig_xmax, orig_ymax],
                        'tile_bbox': [xmin, ymin, xmax, ymax]
                    })
            else:
                # 直接转换坐标
                orig_xmin = xmin + x1
                orig_ymin = ymin + y1
                orig_xmax = xmax + x1
                orig_ymax = ymax + y1
                
                class_counts[cls_name] += 1
                tile_detections.append({
                    'class': cls_name,
                    'confidence': confidence,
                    'bbox': [orig_xmin, orig_ymin, orig_xmax, orig_ymax],
                    'tile_bbox': [xmin, ymin, xmax, ymax]
                })
        
        all_detections.extend(tile_detections)
        
        # === 新的渲染逻辑：保持原始图像颜色 ===
        # 创建结果图像的副本（保持原始BGR颜色）
        result_img = tile.copy()
        
        # 为每个检测绘制边界框和标签
        for detection in tile_detections:
            class_name = detection['class']
            confidence = detection['confidence']
            tile_bbox = detection['tile_bbox']
            
            # 获取类别颜色
            color = class_colors.get(class_name, (0, 255, 0))  # 默认绿色
            
            # 绘制检测框
            draw_detection(result_img, tile_bbox, class_name, confidence, color)
        
        result_images.append(result_img)

        # 保存检测后的瓦片
        detected_path = os.path.join(output_img_folder, f"{filename}_detected_{i}_{j}.jpg")
        cv2.imwrite(detected_path, result_img)
        
        # 记录瓦片处理时间
        tile_time = time.time() - tile_start_time
        tile_times.append(tile_time)

        # 统计信息
        result_row = {
            "SubImage": f"{filename}_tile_{i}_{j}.jpg", 
            "Position": f"({i},{j})",
            "处理时间(秒)": f"{tile_time:.2f}",
            "检测目标数": sum(class_counts.values())
        }
        for cls in model.names.values():
            result_row[cls] = class_counts.get(cls, 0)
        result_row["Total"] = sum(class_counts.values())
        results_list.append(result_row)

    # === 8. 拼接结果图 ===
    if len(result_images) > 1:
        # 创建拼接画布
        stitched_h = rows * tile_size
        stitched_w = cols * tile_size
        stitched_canvas = np.zeros((stitched_h, stitched_w, 3), dtype=np.uint8)
        
        # 将各个瓦片放置到对应位置
        for idx, (result_img, pos_info) in enumerate(zip(result_images, positions)):
            i, j, _, _, _, _ = pos_info
            y_start = i * tile_size
            x_start = j * tile_size
            
            # 确保瓦片尺寸正确
            result_img_resized = cv2.resize(result_img, (tile_size, tile_size))
            stitched_canvas[y_start:y_start+tile_size, x_start:x_start+tile_size] = result_img_resized
        
        stitched_path = os.path.join(output_img_folder, f"{filename}_stitched_detected.jpg")
        cv2.imwrite(stitched_path, stitched_canvas)
        print(f"✅ 已生成拼接结果图: {stitched_path}")

    # === 9. 生成完整图像的检测结果 ===
    # 在原始图像上绘制所有检测框
    img_with_detections = img.copy()
    for detection in all_detections:
        bbox = detection['bbox']
        class_name = detection['class']
        confidence = detection['confidence']
        
        # 获取类别颜色
        color = class_colors.get(class_name, (0, 255, 0))  # 默认绿色
        
        # 绘制检测框
        draw_detection(img_with_detections, bbox, class_name, confidence, color)

    # 保存完整检测结果
    final_detection_path = os.path.join(output_img_folder, f"{filename}_final_detected.jpg")
    cv2.imwrite(final_detection_path, img_with_detections)
    print(f"✅ 已生成完整检测结果图: {final_detection_path}")

    # === 10. 保存统计结果 ===
    df = pd.DataFrame(results_list)
    
    # 计算图像总处理时间
    image_total_time = time.time() - image_start_time
    total_processing_time += image_total_time
    
    # 添加汇总行
    summary_row = {"SubImage": "汇总", "Position": "全部"}
    total_count = 0
    for cls in model.names.values():
        cls_total = df[cls].sum()
        summary_row[cls] = cls_total
        total_count += cls_total
    summary_row["Total"] = total_count
    summary_row["处理时间(秒)"] = f"{image_total_time:.2f}"
    summary_row["检测目标数"] = total_count
    
    # 将汇总行添加到DataFrame
    df = pd.concat([df, pd.DataFrame([summary_row])], ignore_index=True)
    df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')

    # === 11. 保存时间统计 ===
    time_stats = {
        "项目": [
            "模型加载时间(秒)",
            "图像总处理时间(秒)",
            "瓦片数量",
            "平均瓦片处理时间(秒)",
            "总检测目标数",
            "处理速度(目标/秒)"
        ],
        "数值": [
            f"{load_time:.2f}",
            f"{image_total_time:.2f}",
            f"{len(sub_images)}",
            f"{np.mean(tile_times):.2f}" if tile_times else "0.00",
            f"{total_count}",
            f"{total_count/image_total_time:.2f}" if image_total_time > 0 else "0.00"
        ]
    }
    
    time_df = pd.DataFrame(time_stats)
    time_df.to_csv(output_time_csv_path, index=False, encoding='utf-8-sig')

    print(f"✅ 处理完成：{filename}，共检测到 {total_count} 个目标")
    print(f"⏱️ 处理时间: {image_total_time:.2f} 秒, 平均每个瓦片: {np.mean(tile_times):.2f} 秒")

# === 12. 总体统计 ===
print(f"\n📊 总体统计:")
print(f"   处理图像总数: {total_images}")
print(f"   总处理时间: {total_processing_time:.2f} 秒")
print(f"   平均每张图像处理时间: {total_processing_time/total_images:.2f} 秒" if total_images > 0 else "0.00 秒")

print("\n🎉 批量处理全部完成！")
