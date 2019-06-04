import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
from PIL import Image

# This is needed since the notebook is stored in the object_detection folder.
from utils import ops as utils_ops

if StrictVersion(tf.__version__) < StrictVersion('1.12.0'):
  raise ImportError('Please upgrade your TensorFlow installation to v1.12.*.')

sys.path.append("..")
from utils import label_map_util
from object_detection.utils import timer as timer_util

# Load inference function
from run_inference_for_single_image import infere

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


def detect_objects(model_name):

	# What model to download.
	MODEL_NAME = model_name

	MODEL_DIR = 'models_data'
	MODEL_FILE = MODEL_NAME + '.tar.gz'
	DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

	# Path to frozen detection graph. This is the actual model that is used for the object detection.
	PATH_TO_FROZEN_GRAPH = os.path.join(MODEL_DIR,MODEL_NAME + '/frozen_inference_graph.pb')

	# List of the strings that is used to add correct label for each box.
	PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

	opener = urllib.request.URLopener()
	opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, os.path.join(MODEL_DIR,MODEL_FILE))
	tar_file = tarfile.open(os.path.join(MODEL_DIR,MODEL_FILE))
	for file in tar_file.getmembers():
	  file_name = os.path.basename(file.name)
	  if 'frozen_inference_graph.pb' in file_name:
	    tar_file.extract(file, os.path.join(MODEL_DIR,MODEL_NAME))

	detection_graph = tf.Graph()
	with detection_graph.as_default():
	  od_graph_def = tf.GraphDef()
	  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
	    serialized_graph = fid.read()
	    od_graph_def.ParseFromString(serialized_graph)
	    tf.import_graph_def(od_graph_def, name='')

	category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

	# For the sake of simplicity we will use only 2 images:
	# image1.jpg
	# image2.jpg
	# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
	PATH_TO_TEST_IMAGES_DIR = 'test_images_cameras'
	TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, '{}'.format(name)) for name in os.listdir(PATH_TO_TEST_IMAGES_DIR) ]

	print(TEST_IMAGE_PATHS)

	# Size, in inches, of the output images.
	IMAGE_SIZE = (12, 8)

	timer = timer_util.Timer()
	for image_path in TEST_IMAGE_PATHS:
		timer.tic()
		image = Image.open(image_path)
	  	# the array based representation of the image will be used later in order to prepare the
		# result image with boxes and labels on it.
		image_np = load_image_into_numpy_array(image)
		# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
		image_np_expanded = np.expand_dims(image_np, axis=0)
		# Actual detection.
		output_dict = infere(image_np_expanded, detection_graph)
		duration = timer.toc()
		output_dict['proc_duration'] = duration

		return output_dict,image_np
