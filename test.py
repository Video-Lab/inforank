from importlib import import_module
from sys import modules

# Testing info
TESTS = [  ["generateVideoImage", {'path': './tests/testfile.txt', 'out_dir': './tests/imgs/videoimage.png'}]]
OLD_TESTS = [["parseFileTest", {'path': './tests/testfile.txt'}],
["generateImageTest", {'path': './tests/testfile.txt', 'test_path': './tests/imgs/databox_base_w_value_sample.png'}],
["generateAndTestDataBoxes", {'path': './tests/testfile.txt', 'out_dir': './tests/imgs/'}]]

def parseFile(path):
	import fileparser
	video = fileparser.parseFile(path)
	return video

def generateImageBaseTest(path, test_path):
	import fileparser
	from databox import DataBox
	video = fileparser.parseFile(path)
	img = video.data_boxes[0].generateImageBase()
	img.save(test_path)

def generateImageTest(path, test_path):
	import fileparser
	from databox import DataBox
	video = fileparser.parseFile(path)
	video.data_boxes[0].image.save(test_path)

def generateDataBoxes(path, out_dir):
	import fileparser
	from databox import DataBox
	import os
	video = fileparser.parseFile(path)
	generateDataBoxesFromVideo(video, out_dir)

def generateDataBoxesFromVideo(video, out_dir):
	from databox import DataBox
	import os
	for i in range(len(video.data_boxes)):
		out_path = os.path.join(out_dir, f"databox_{i}.png")
		video.data_boxes[i].image.save(out_path)

def generateAndTestDataBoxes(path, out_dir):
	from databox import DataBox
	import os
	video = parseFile(path)
	generateDataBoxesFromVideo(video, out_dir)
	video.previewDataBoxes()

def generateVideoImage(path, out_dir):
	video = parseFile(path)
	video.generateVideoImage()
	video.outputVideoImage(out_dir)
	
if __name__ == "__main__":
	for test in TESTS:
		getattr(modules[__name__], test[0])(**test[1])
