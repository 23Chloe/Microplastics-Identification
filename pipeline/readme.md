**The process of dataset processing:**

1\. Obtain the global image (super-depth-of-field microscope) -- path:

*Microplastic-Image-Recognition\\dataset\\global images\_96*

2\. Slide window cropping (20% overlap rate) -- document:

*Microplastic-Image-Recognition\\pipeline\\Slide window cropping.py*

3\. Verify the suspicious particles on the image with FTIR, and label those verified as "MPs", obtaining the labeled file

4\. Statistically analyze the category information of the labeled file

5\. Augmentation the "film" category separately and then augmentation all categories together-- document:

*Microplastic-Image-Recognition\\pipeline\\data augmentation.py*

6. Split the dataset -- document:

*Microplastic-Image-Recognition\\pipeline\\divide\_dataset.py*

7. Convert the format of the labeled file according to the input requirements of different models (optional) -- document:

*Microplastic-Image-Recognition\\pipeline\\json\_txt.py*







**The training process of the model:**

1\. Modify the my\_data.yaml file of the model to configure the dataset.

2\. Adjust the hyperparameters and load the pre-trained weight file.

3\. Start the training and obtain the training results.

4\. Optimize the hyperparameters, train multiple times, compare the results, and select the best hyperparameters.

5\. Compare the evaluation results of different models (F1/Recall/Precision/mAP@0.5/mAP@0.5-0.95).







**The evaluation process of the best model on the generalization test dataset:**

1\. Obtain the true results of the generalization test dataset (FTIR).

2\. Run the best model to identify microplastics in the dataset (model).

3\. Compare the model's results with the true results and calculate the accuracy and recall rate of the best model (Precision, Recall).

4\. Calculate the average processing time required for each filter membrane. 

*Microplastic-Image-Recognition\\pipeline\\Calculate time.py*



<b>Quickly apply the model test dataset：</b>*Microplastic-Image-Recognition\\pipeline\\APP5.0.py*

## Portable command-line usage

All filesystem locations are supplied at runtime; no machine-specific absolute
paths are embedded in the published scripts. Run `python "<script>.py" --help`
to see the arguments for each utility. For example:

```bash
python "Slide window cropping.py" --input-folder dataset/global_images --output-folder dataset/tiles
python divide_dataset.py --input-images dataset/images --input-json dataset/jsons --output-root dataset/splits
python APP5.0.py --model-path weights/best.pt --input-folder dataset/test/images --output-folder outputs
```

