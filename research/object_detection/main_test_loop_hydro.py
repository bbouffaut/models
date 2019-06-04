%dirs
%cd tensorflow-models/research/object_detection

from object_detection_lib import detect_objects
from utils import visualization_utils as vis_util
from matplotlib import pyplot as plt

%matplotlib inline

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
