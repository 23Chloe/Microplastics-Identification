import argparse
import os
import json

# Directory containing annotation files.
parser = argparse.ArgumentParser(description="Count object classes in LabelMe JSON annotations.")
parser.add_argument("--input-json-folder", required=True, help="Directory containing LabelMe JSON files.")
input_json_folder = parser.parse_args().input_json_folder

# Per-class count dictionary.
category_count = {}

# Collect all annotation files.
json_files = [f for f in os.listdir(input_json_folder) if f.endswith('.json')]

# Count annotations for each class.
for json_file in json_files:
    json_path = os.path.join(input_json_folder, json_file)
    
    # Read one annotation file.
    with open(json_path, 'r') as f:
        annotations = json.load(f)
    
    # Count the class of each annotation.
    for obj in annotations['shapes']:
        category = obj['label']  # Read the class label.
        
        # Update the class count.
        if category in category_count:
            category_count[category] += 1
        else:
            category_count[category] = 1

# Print the count for each class.
print("Annotation count by class:")
for category, count in category_count.items():
    print(f"{category}: {count}")
