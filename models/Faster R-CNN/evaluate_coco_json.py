"""Evaluate COCO-format prediction JSON from IoU 0.50 to 0.95."""

import argparse
from pathlib import Path

import numpy as np
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval


def evaluate(ground_truth_json: Path, predictions_json: Path) -> np.ndarray:
    ground_truth = COCO(str(ground_truth_json))
    predictions = ground_truth.loadRes(str(predictions_json))
    evaluator = COCOeval(ground_truth, predictions, "bbox")
    evaluator.params.iouThrs = np.linspace(0.5, 0.95, 10)
    evaluator.evaluate()
    evaluator.accumulate()
    evaluator.summarize()
    return evaluator.stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ground-truth-json", type=Path, required=True)
    parser.add_argument("--predictions-json", type=Path, required=True)
    arguments = parser.parse_args()
    stats = evaluate(arguments.ground_truth_json, arguments.predictions_json)
    print(f"mAP@0.50:0.95: {stats[0]:.4f}")
    print(f"mAP@0.50: {stats[1]:.4f}")
