from importlib import import_module
from sys import modules


# Testing info
TESTS = [["parseFileTest", {'path': './tests/testfile.txt'}]]

def parseFileTest(path):
	import fileparser
	video = fileparser.parseFile(path)
	print(video.title)
	print(video.width)
	print(video.height)
	print(video.data_boxes[0].data_box_width)
	print(video.data_boxes[0].data_value)
	print(video.data_boxes[0].data_title)

if __name__ == "__main__":
	for test in TESTS:
		getattr(modules[__name__], test[0])(**test[1])
