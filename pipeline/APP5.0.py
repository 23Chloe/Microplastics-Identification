import argparse
import os
import cv2
import torch
import numpy as np
import pandas as pd
import time
from collections import defaultdict

# Process images of different sizes by cropping and padding them to 1280 x 1280,
# running detection, summarizing predictions, and stitching the result tiles.
# Validated for generalized-dataset detection analysis on 2025-10-31.
# === 1. Parameters ===
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

# === 2. Load the model ===
print("Loading model...")
start_load_time = time.time()
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, trust_repo=True)
model.conf = 0.25  # Confidence threshold
load_time = time.time() - start_load_time
print(f"Model loaded in {load_time:.2f} s")

# Class-to-color mapping.
class_colors = {
    'fragment': (0, 255, 0),    # Green
    'fiber': (255, 0, 0),       # Blue
    'lament': (0, 0, 255),      # Red
    # Add other classes as needed.
}

def draw_detection(image, bbox, class_name, confidence, color):
    """Draw a detection box and label without filling the box interior."""
    xmin, ymin, xmax, ymax = bbox
    
    # Convert coordinates to integers.
    xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
    
    # Draw only the box border.
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
    
    # Prepare label text.
    label = f"{class_name} {confidence:.2f}"
    
    # Calculate label dimensions.
    (label_width, label_height), baseline = cv2.getTextSize(
        label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
    )
    
    # Draw the label background above the box.
    label_y = max(ymin - 5, label_height + 5)
    cv2.rectangle(image,
                 (xmin, label_y - label_height - 5),
                 (xmin + label_width, label_y),
                 color, -1)  # Fill the label background.
    
    # Draw label text.
    cv2.putText(image, label,
               (xmin, label_y - 5),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# === 3. Iterate over input images ===
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
    output_csv_path = os.path.join(output_img_folder, "detection_statistics.csv")
    output_time_csv_path = os.path.join(output_img_folder, "timing_statistics.csv")

    print(f"\nProcessing image: {file}")

    # === 4. Read the image ===
    img = cv2.imread(input_image_path)
    if img is None:
        print(f"Error: unable to read image: {input_image_path}")
        continue

    h, w = img.shape[:2]
    
    # === 5. Calculate the tile grid ===
    rows = (h + tile_size - 1) // tile_size  # Round up.
    cols = (w + tile_size - 1) // tile_size  # Round up.
    
    print(f"Image size: {w}x{h}; tile grid: {rows}x{cols}")

    # === 6. Crop and pad tiles ===
    sub_images, positions, padding_info = [], [], []
    
    for i in range(rows):
        for j in range(cols):
            # Calculate the current tile boundaries.
            y1 = i * tile_size
            x1 = j * tile_size
            y2 = min((i + 1) * tile_size, h)
            x2 = min((j + 1) * tile_size, w)
            
            # Extract the unpadded tile.
            original_tile = img[y1:y2, x1:x2]
            tile_h, tile_w = original_tile.shape[:2]
            
            # Pad edge tiles when needed.
            if tile_h < tile_size or tile_w < tile_size:
                # Create a neutral gray square background.
                padded_tile = np.full((tile_size, tile_size, 3), 128, dtype=np.uint8)
                # Place the original tile in the upper-left corner.
                padded_tile[:tile_h, :tile_w] = original_tile
                padding_flag = True
            else:
                padded_tile = original_tile
                padding_flag = False
            
            sub_images.append(padded_tile)
            positions.append((i, j, y1, x1, y2, x2))
            padding_info.append((padding_flag, tile_h, tile_w))

    # === 7. Detect and render ===
    results_list, result_images = [], []
    all_detections = []  # Store detections in full-image coordinates.
    tile_times = []  # Store processing time for each tile.

    for idx, (tile, pos_info, pad_info) in enumerate(zip(sub_images, positions, padding_info)):
        i, j, y1, x1, y2, x2 = pos_info
        padding_flag, tile_h, tile_w = pad_info
        
        print(f"Processing tile ({i},{j})...")
        tile_start_time = time.time()
        
        # Save the input tile.
        tile_path = os.path.join(output_img_folder, f"{filename}_tile_{i}_{j}.jpg")
        cv2.imwrite(tile_path, tile)

        # Run detection directly on the in-memory image.
        try:
            # Convert BGR to RGB for detection.
            tile_rgb = cv2.cvtColor(tile, cv2.COLOR_BGR2RGB)
            results = model(tile_rgb)
            detections = results.pandas().xyxy[0]
        except Exception as e:
            print(f"Detection failed: {e}")
            continue
            
        class_counts = defaultdict(int)
        
        # Process detections.
        tile_detections = []
        for _, row in detections.iterrows():
            cls_name = row['name']
            confidence = row['confidence']
            xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']
            
            # Exclude detections that fall entirely inside padded regions.
            if padding_flag:
                # Keep boxes that intersect the original tile area.
                if (xmin < tile_w and ymin < tile_h and 
                    xmax > 0 and ymax > 0):
                    # Clip each box to the original tile boundary.
                    xmin = max(0, xmin)
                    ymin = max(0, ymin)
                    xmax = min(tile_w, xmax)
                    ymax = min(tile_h, ymax)
                    
                    # Convert tile coordinates to full-image coordinates.
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
                # Convert coordinates without padding adjustment.
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
        
        # Render on a copy while preserving the original BGR colors.
        result_img = tile.copy()
        
        # Draw the box and label for each detection.
        for detection in tile_detections:
            class_name = detection['class']
            confidence = detection['confidence']
            tile_bbox = detection['tile_bbox']
            
            # Use the configured class color or green by default.
            color = class_colors.get(class_name, (0, 255, 0))
            
            # Draw the detection.
            draw_detection(result_img, tile_bbox, class_name, confidence, color)
        
        result_images.append(result_img)

        # Save the rendered tile.
        detected_path = os.path.join(output_img_folder, f"{filename}_detected_{i}_{j}.jpg")
        cv2.imwrite(detected_path, result_img)
        
        # Record tile processing time.
        tile_time = time.time() - tile_start_time
        tile_times.append(tile_time)

        # Record per-tile statistics.
        result_row = {
            "SubImage": f"{filename}_tile_{i}_{j}.jpg", 
            "Position": f"({i},{j})",
            "Processing time (s)": f"{tile_time:.2f}",
            "Detection count": sum(class_counts.values())
        }
        for cls in model.names.values():
            result_row[cls] = class_counts.get(cls, 0)
        result_row["Total"] = sum(class_counts.values())
        results_list.append(result_row)

    # === 8. Stitch rendered tiles ===
    if len(result_images) > 1:
        # Create the stitching canvas.
        stitched_h = rows * tile_size
        stitched_w = cols * tile_size
        stitched_canvas = np.zeros((stitched_h, stitched_w, 3), dtype=np.uint8)
        
        # Place each rendered tile at its grid position.
        for idx, (result_img, pos_info) in enumerate(zip(result_images, positions)):
            i, j, _, _, _, _ = pos_info
            y_start = i * tile_size
            x_start = j * tile_size
            
            # Normalize tile dimensions before stitching.
            result_img_resized = cv2.resize(result_img, (tile_size, tile_size))
            stitched_canvas[y_start:y_start+tile_size, x_start:x_start+tile_size] = result_img_resized
        
        stitched_path = os.path.join(output_img_folder, f"{filename}_stitched_detected.jpg")
        cv2.imwrite(stitched_path, stitched_canvas)
        print(f"Saved stitched detection image: {stitched_path}")

    # === 9. Render detections on the full image ===
    img_with_detections = img.copy()
    for detection in all_detections:
        bbox = detection['bbox']
        class_name = detection['class']
        confidence = detection['confidence']
        
        # Use the configured class color or green by default.
        color = class_colors.get(class_name, (0, 255, 0))
        
        # Draw the detection.
        draw_detection(img_with_detections, bbox, class_name, confidence, color)

    # Save the full-image detection result.
    final_detection_path = os.path.join(output_img_folder, f"{filename}_final_detected.jpg")
    cv2.imwrite(final_detection_path, img_with_detections)
    print(f"Saved full-image detection result: {final_detection_path}")

    # === 10. Save detection statistics ===
    df = pd.DataFrame(results_list)
    
    # Calculate total processing time for this image.
    image_total_time = time.time() - image_start_time
    total_processing_time += image_total_time
    
    # Add a summary row.
    summary_row = {"SubImage": "Summary", "Position": "All"}
    total_count = 0
    for cls in model.names.values():
        cls_total = df[cls].sum()
        summary_row[cls] = cls_total
        total_count += cls_total
    summary_row["Total"] = total_count
    summary_row["Processing time (s)"] = f"{image_total_time:.2f}"
    summary_row["Detection count"] = total_count
    
    # Append the summary row to the DataFrame.
    df = pd.concat([df, pd.DataFrame([summary_row])], ignore_index=True)
    df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')

    # === 11. Save timing statistics ===
    time_stats = {
        "Metric": [
            "Model loading time (s)",
            "Total image processing time (s)",
            "Tile count",
            "Mean tile processing time (s)",
            "Total detection count",
            "Processing rate (detections/s)"
        ],
        "Value": [
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

    print(f"Completed {filename}: {total_count} detections")
    mean_tile_time = np.mean(tile_times) if tile_times else 0.0
    print(f"Processing time: {image_total_time:.2f} s; mean per tile: {mean_tile_time:.2f} s")

# === 12. Overall statistics ===
print("\nOverall statistics:")
print(f"   Images processed: {total_images}")
print(f"   Total processing time: {total_processing_time:.2f} s")
print(
    f"   Mean processing time per image: {total_processing_time / total_images:.2f} s"
    if total_images > 0
    else "   Mean processing time per image: 0.00 s"
)

print("\nBatch processing completed.")
