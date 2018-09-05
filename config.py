import os
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
MODEL_FOLDER = "./modelfolder"

VIDEO_TAG = "./videosource"
VIDEO_FOLDER = "./videofolder"

CNN_TAG = "./cnnmodel"


def get_model():
    return os.path.join(root.find(MODEL_FOLDER).text, root.find(MODEL_TAG).text)


def get_video_source():
    return os.path.join(root.find(VIDEO_FOLDER).text, root.find(VIDEO_TAG).text)


def get_cnn():
    return os.path.join(root.find(MODEL_FOLDER).text, root.find(CNN_TAG).text)


def set_video_source(filename):
    folder, file = folder_file(filename)
    root.find(VIDEO_FOLDER).text = folder
    root.find(VIDEO_TAG).text = file
    tree.write("config.xml")
    reload()


def set_model(filename):
    folder, file = folder_file(filename)
    root.find(MODEL_FOLDER).text = folder
    root.find(MODEL_TAG).text = file
    tree.write("config.xml")
    reload()


def set_cnn(filename):
    folder, file = folder_file(filename)
    root.find(MODEL_FOLDER).text = folder
    root.find(CNN_TAG).text = file
    tree.write("config.xml")
    reload()


def folder_file(path):
    file = path.split(os.path.sep)[-1]
    index = path.find(file) - 1
    folder = path[0:index] if index != -1 else ''
    return folder, file


if __name__ == '__main__':
    print(get_model())
    print(get_video_source())
    print(get_cnn())
