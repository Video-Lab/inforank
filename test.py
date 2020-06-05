from importlib import import_module
from sys import modules


# Testing info
TESTS = [["generateImageTest", {'path': './tests/testfile.txt', 'test_path': './tests/imgs/databox_base_w_value_sample.png'}]]
OLD_TESTS = [["parseFileTest", {'path': './tests/testfile.txt'}]]

def parseFileTest(path):
	import fileparser
	video = fileparser.parseFile(path)
	print(video.title)
	print(video.width)
	print(video.height)
	print(video.data_boxes[0].data_box_width)
	print(video.data_boxes[0].data_value)
	print(video.data_boxes[0].data_title)


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
	video.data_boxes[0].generateImage()
	video.data_boxes[0].image.save(test_path)


if __name__ == "__main__":
	for test in TESTS:
		getattr(modules[__name__], test[0])(**test[1])
