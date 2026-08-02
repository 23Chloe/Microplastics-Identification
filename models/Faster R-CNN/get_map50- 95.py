import os
import xml.etree.ElementTree as ET
import time
import json
import numpy as np
from PIL import Image
from tqdm import tqdm
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

from utils.utils import get_classes
from utils.utils_map import get_coco_map, get_map
from frcnn import FRCNN

if __name__ == "__main__":
    map_mode = 0  # 设置模式，0 代表完整流程，4 代表计算 COCO mAP
    classes_path = 'model_data/classes.txt'
    MINOVERLAP = 0.5
    confidence = 0.02
    nms_iou = 0.5
    score_threhold = 0.5
    map_vis = False
    VOCdevkit_path = 'VOCdevkit'
    map_out_path = 'map_out'

    image_ids = open(os.path.join(VOCdevkit_path, "VOC2007/ImageSets/Main/test.txt")).read().strip().split()

    if not os.path.exists(map_out_path):
        os.makedirs(map_out_path)
    if not os.path.exists(os.path.join(map_out_path, 'ground-truth')):
        os.makedirs(os.path.join(map_out_path, 'ground-truth'))
    if not os.path.exists(os.path.join(map_out_path, 'detection-results')):
        os.makedirs(os.path.join(map_out_path, 'detection-results'))
    if not os.path.exists(os.path.join(map_out_path, 'images-optional')):
        os.makedirs(os.path.join(map_out_path, 'images-optional'))

    class_names, _ = get_classes(classes_path)

    if map_mode == 0 or map_mode == 1:
        print("Load model.")
        frcnn = FRCNN(confidence=confidence, nms_iou=nms_iou)
        print("Load model done.")

    if map_mode == 0 or map_mode == 4:
        print("Calculating COCO mAP@0.5:0.95...")
        gt_json_path = os.path.join(map_out_path, "ground-truth.json")
        pred_json_path = os.path.join(map_out_path, "detection-results.json")
        
        coco_gt = COCO(gt_json_path)
        coco_dt = coco_gt.loadRes(pred_json_path)
        coco_eval = COCOeval(coco_gt, coco_dt, "bbox")
        coco_eval.params.iouThrs = np.linspace(0.5, 0.95, 10)
        coco_eval.evaluate()
        coco_eval.accumulate()
        coco_eval.summarize()
        
        map_50_95 = coco_eval.stats[0]  # mAP@0.5:0.95
        map_50 = coco_eval.stats[1]  # mAP@0.5
        
        print(f"mAP@0.5: {map_50:.4f}")
        print(f"mAP@0.5:0.95: {map_50_95:.4f}")