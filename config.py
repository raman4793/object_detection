import xml.etree.ElementTree as ET

attribs = []

tree = ET.parse('config.xml')
root = tree.getroot()	
for ele in root:
	attribs.append(ele.attrib)
def reload():
	tree = ET.parse('config.xml')
	root = tree.getroot()	
	for ele in root:
		attribs.append(ele.attrib)

reload()
# MODEL_NAME = "trained_models/new_12_model"
# VIDEO_SOURCE = "p1.mp4"
# CNN_MODEL = "trained_models/safe_unsafe.model"
MODEL_TAG = "./modelname"

VIDEO_TAG = "./videosource"

CNN_TAG = "./cnnmodel"

def get_model():
	print(root.find(MODEL_TAG).text)

def get_video_source():
	print(root.find(VIDEO_TAG).text)

def get_cnn():
	print(root.find(CNN_TAG).text)

def set_video_source(filename):
	root.find(VIDEO_TAG).text = filename
	tree.write("config.xml")
	reload()

def set_model(filename):
	root.find(MODEL_TAG).text = filename
	tree.write("config.xml")
	reload()

def set_cnn(filename):
	root.find(CNN_TAG).text = filename
	tree.write("config.xml")
	reload()

if __name__ == '__main__':
	get_model()
	get_video_source()
	get_cnn()