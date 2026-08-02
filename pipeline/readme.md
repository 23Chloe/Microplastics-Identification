**The process of dataset processing:**

1\. Obtain the global image (super-depth-of-field microscope) -- path:

*Microplastic-Image-Recognition\\dataset\\global images\_96*

2\. Slide window cropping (20% overlap rate) -- document:

*Microplastic-Image-Recognition\\pipeline\\Slide window cropping.py*

3\. Verify the suspicious particles on the image with FTIR, and label those verified as "MPs", obtaining the labeled file

4\. Statistically analyze the category information of the labeled file

5\. Assign every tile from the same original microscope image or filter
membrane to one source group, then split those groups into training,
validation, and test sets before augmentation. A `stem,group_id` CSV is
required so overlapping tiles cannot cross dataset boundaries -- document:

*Microplastic-Image-Recognition\\pipeline\\divide\_dataset.py*

6\. Apply augmentation to the training set only. The film class can receive a
higher augmentation multiplier -- document:

*Microplastic-Image-Recognition\\pipeline\\data augmentation.py*

7. Convert the annotation format according to the input requirements of each model (optional) -- document:

*Microplastic-Image-Recognition\\pipeline\\json\_txt.py*







**The training process of the model:**

1\. Modify the my\_data.yaml file of the model to configure the dataset.

2\. Adjust the hyperparameters and load the pre-trained weight file.

3\. Start the training and obtain the training results.

4\. Optimize the hyperparameters, train multiple times, compare the results, and select the best hyperparameters.

5\. Compare the evaluation results of different models (F1/Recall/Precision/mAP@0.5/mAP@0.5-0.95).







**The application evaluation process on the separately collected ID/OOD membranes:**

1\. Obtain the true results of the generalization test dataset (FTIR).

2\. Run the selected model to identify microplastics in the dataset (model).

3\. Compare the model's results with the true results and calculate the accuracy and recall rate of the best model (Precision, Recall).

4\. Calculate the average processing time required for each filter membrane. 

*Microplastic-Image-Recognition\\pipeline\\Calculate time.py*



<b>Quickly apply the model test dataset:</b> *Microplastic-Image-Recognition\\pipeline\\APP5.0.py*

## Portable command-line usage

All filesystem locations are supplied at runtime; no machine-specific absolute
paths are embedded in the published scripts. Run `python "<script>.py" --help`
to see the arguments for each utility. For example:

```bash
python "Slide window cropping.py" --input-folder dataset/global_images --output-folder dataset/tiles --edge-mode discard
python divide_dataset.py --input-images dataset/images --input-json dataset/jsons --groups-csv pipeline/group_manifest.csv --output-root dataset/splits --seed 0
python APP5.0.py --model-path models/YOLOv5/weights/best.pt --input-folder dataset/test/images --output-folder outputs
```

The splitter writes `split_manifest.csv` and refuses to proceed without an
explicit source-group assignment for every annotation. Augmentation must be
run only on `dataset/splits/train`; validation and test files must remain
unaugmented.

The historical experiment archive states that augmentation preceded the 7:2:1
split and does not retain source-group membership. Therefore, the safer
prospective workflow documented above must not be used retroactively to call
the historical internal test subset independent or leakage-free. Until a
source-disjoint audit or rerun is available, the internal metrics are reported
as archived benchmark metrics and are not presented as proof of generalizability.

`--edge-mode discard` preserves the archived full-tile cropping behavior.
`--edge-mode cover` also includes border regions and pads images smaller than
one tile. Record the selected mode because it changes the generated dataset.

