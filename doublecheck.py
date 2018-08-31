# USAGE
# python test_network.py --model santa_not_santa.model --image images/examples/santa_01.png

# import the necessary packages
import os
os.environ['KERAS_BACKEND'] = 'theano'
import numpy as np
import argparse
import imutils
import cv2
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import math

class DoubleChecker:

	def __init__(self):
		self.MODEL_NAME = "safe_unsafe.model"
		self.model = load_model(self.MODEL_NAME)

	def double_check(self, image, cropbox, use_normalized_coordinates=True):
		# cv2.imshow("test", image)
		# cv2.waitKey()		
		# print(cropbox)
		cropbox = self.normalize_cropbox(image, cropbox, use_normalized_coordinates)
		cropped_image = self.crop(image, cropbox)
		# cv2.imshow("test", cropped_image)
		# cv2.waitKey()		
		# print(cropbox)
		# pre-process the image for classification

		try:
			cropped_image = cv2.resize(cropped_image, (28, 28))
			# cv2.imshow("test", cropped_image)
			# cv2.waitKey()			
			cropped_image = cropped_image.astype("float") / 255.0
			cropped_image = img_to_array(cropped_image)
			cropped_image = np.expand_dims(cropped_image, axis=0)

			safe, unsafe = self.model.predict(cropped_image)[0]
			label = "unsafe" if safe > unsafe else "safe"
			proba = safe if safe > unsafe else unsafe			
		except:
			label = "safe"
			proba = 0.25
		# print((label, proba))
		# label = "{}: {:.2f}%".format(label, proba * 100)		
		return (label, proba)

	# def normalize_cropbox(self, image, cropbox):
	# 	draw = ImageDraw.Draw(image)
	# 	im_width, im_height = image.size
	# 	ymin, xmin, ymax, xmax = cropbox
	# 	if use_normalized_coordinates:
	# 		(left, right, top, bottom) = (xmin * im_width, xmax * im_width,
	# 	                              ymin * im_height, ymax * im_height)
	# 	else:
	# 		(left, right, top, bottom) = (xmin, xmax, ymin, ymax)		

	# 	return (ymin, xmin, ymax, xmax)

	def normalize_cropbox(self, image, cropbox, use_normalized_coordinates=True):
		# draw = ImageDraw.Draw(image)
		im_width, im_height = 1920, 1080
		ymin, xmin, ymax, xmax = cropbox
		(left, right, top, bottom) = (xmin * im_width, xmax * im_width,
		                              ymin * im_height, ymax * im_height)	


		return (top, bottom, left, right)

	def crop(self, numpy_image, crop_box):
		# print(crop_box)
		(top, bottom, left, right) = crop_box
		top = math.floor(top)
		bottom = math.floor(bottom)
		left = math.floor(left)
		right = math.floor(right)
		# print("Cropbox ", (top, bottom, left, right))
		# x1 = int(crop_box[0])-25
		# y1 = int(crop_box[1])-25
		# x2 = int(crop_box[2])+25
		# y2 = int(crop_box[3])+25
		return numpy_image[top:bottom, left:right]

# # construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-m", "--model", required=True,
# 	help="path to trained model model")
# ap.add_argument("-i", "--image", required=True,
# 	help="path to input image")
# args = vars(ap.parse_args())

# # load the image
# image = cv2.imread(args["image"])
# orig = image.copy()

# # pre-process the image for classification
# image = cv2.resize(image, (28, 28))
# image = image.astype("float") / 255.0
# image = img_to_array(image)
# image = np.expand_dims(image, axis=0)

# # load the trained convolutional neural network
# print("[INFO] loading network...")
# model = load_model(args["model"])

# # classify the input image
# (notSanta, santa) = model.predict(image)[0]

# # build the label
# label = "Safe" if santa > notSanta else "Not Safe"
# proba = santa if santa > notSanta else notSanta
# label = "{}: {:.2f}%".format(label, proba * 100)

# # draw the label on the image
# output = imutils.resize(orig, width=400)
# cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
# 	0.7, (0, 255, 0), 2)

# # show the output image
# cv2.imshow("Output", output)
# cv2.waitKey(0)