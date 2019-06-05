%dirs
%cd tensorflow-models/research/object_detection

import os
from object_detection_lib import detect_objects
from utils import visualization_utils as vis_util
from object_detection.utils import label_map_util

from matplotlib import pyplot as plt

%matplotlib inline

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine
# %%
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
# %% markdown

output_dict, image_np = detect_objects('ssd_mobilenet_v1_ppn_shared_box_predictor_300x300_coco14_sync_2018_07_03')

# Visualization of the results of a detection.
vis_util.visualize_boxes_and_labels_on_image_array(
	image_np,
	output_dict['detection_boxes'],
	output_dict['detection_classes'],
	output_dict['detection_scores'],
	category_index,
	instance_masks=output_dict.get('detection_masks'),
	use_normalized_coordinates=True,
	line_thickness=8)
plt.figure(figsize=IMAGE_SIZE)
plt.imshow(image_np)

print(output_dict)
