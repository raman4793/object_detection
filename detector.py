import os

import numpy as np
import tensorflow as tf

import config
import draw
from utils import label_map_util


# Globals

class Detector:

	def __init__(self):
		self.NUM_CLASSES = 2
		self.PATH_TO_LABELS = os.path.join('config', 'object_detection.pbtxt')
		self.label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
		self.categories = label_map_util.convert_label_map_to_categories(self.label_map, max_num_classes=self.NUM_CLASSES, use_display_name=True)
		self.category_index = label_map_util.create_category_index(self.categories)	
		# What model to download.
		self.MODEL_NAME = config.get_model()

		# Path to frozen detection graph. This is the actual model that is used for the object detection.
		self.PATH_TO_CKPT = self.MODEL_NAME + '/frozen_inference_graph.pb'	

		self.detection_graph = tf.Graph()
		with self.detection_graph.as_default():
			od_graph_def = tf.GraphDef()
			with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
				serialized_graph = fid.read()
				od_graph_def.ParseFromString(serialized_graph)
				tf.import_graph_def(od_graph_def, name='')
		self.detection_graph.as_default()
		self.sess = tf.Session(graph=self.detection_graph)

	def __load_graph__(self):
		self.detection_graph.as_default()
		od_graph_def = tf.GraphDef()
		fid = tf.gfile.GFile(self.PATH_TO_CKPT, 'rb')
		# with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
		serialized_graph = fid.read()
		od_graph_def.ParseFromString(serialized_graph)
		tf.import_graph_def(od_graph_def, name='')		


	def predict(self, image, callback):
		count = 0
		# ret, image = cap.read()
		# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
		image_np_expanded = np.expand_dims(image, axis=0)
		image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
		# Each box represents a part of the image where a particular object was detected.
		boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
		# Each score represent how level of confidence for each of the objects.
		# Score is shown on the result image, together with the class label.
		scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
		num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
		# Actual detection.
		(boxes, scores, classes, num_detections) = self.sess.run(
		    [boxes, scores, classes, num_detections],
		    feed_dict={image_tensor: image_np_expanded})
		# Visualization of the results of a detection.
		draw.visualize_boxes_and_labels_on_image_array(
		    image,
		    np.squeeze(boxes),
		    np.squeeze(classes).astype(np.int32),
		    np.squeeze(scores),
		    self.category_index,
		    use_normalized_coordinates=True,
		    line_thickness=8)

		callback(image)
		# cv2.imshow('object detection', cv2.resize(image, (800,600)))
		# cv2.imshow('object detection', image)	
		# cv2.waitKey()
		# time.sleep(2)				

	def __del__(self):
		# fid.close()
		tf.reset_default_graph()
		# self.sess.close()


# NUM_CLASSES = 2
# PATH_TO_LABELS = os.path.join('config', 'object_detection.pbtxt')
# label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
# categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
# category_index = label_map_util.create_category_index(categories)	
# # What model to download.
# MODEL_NAME = 'trained_models/new_12_model'

# # Path to frozen detection graph. This is the actual model that is used for the object detection.
# PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'	

# detection_graph = tf.Graph()
# sess = None

# def process(image, callback):
# 	print("Session ",sess)
# 	count = 0
# 	# ret, image = cap.read()
# 	# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
# 	image_np_expanded = np.expand_dims(image, axis=0)
# 	image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
# 	# Each box represents a part of the image where a particular object was detected.
# 	boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
# 	# Each score represent how level of confidence for each of the objects.
# 	# Score is shown on the result image, together with the class label.
# 	scores = detection_graph.get_tensor_by_name('detection_scores:0')
# 	classes = detection_graph.get_tensor_by_name('detection_classes:0')
# 	num_detections = detection_graph.get_tensor_by_name('num_detections:0')
# 	# Actual detection.
# 	(boxes, scores, classes, num_detections) = sess.run(
# 	    [boxes, scores, classes, num_detections],
# 	    feed_dict={image_tensor: image_np_expanded})
# 	# Visualization of the results of a detection.
# 	draw.visualize_boxes_and_labels_on_image_array(
# 	    image,
# 	    np.squeeze(boxes),
# 	    np.squeeze(classes).astype(np.int32),
# 	    np.squeeze(scores),
# 	    category_index,
# 	    use_normalized_coordinates=True,
# 	    line_thickness=8)

# 	callback(image)
# 	# cv2.imshow('object detection', cv2.resize(image, (800,600)))
# 	# cv2.imshow('object detection', image)	
# 	# cv2.waitKey()
# 	# time.sleep(2)



# def setup():
# 	load_graph()
# 	# detection_graph.as_default()
# 	sess = tf.Session(graph=detection_graph)


# def predict(path, callback):
# 	process(path, callback)

# def clean():
# 	tf.reset_default_graph()
# 	sess.close()	