from importlib import import_module


# Testing info
TESTS = [["parseFileTest", {'path': './tests/testfile.txt'}]]

def parseFileTest(path):
	video = parseFile(path)
	print(dir(video))
	
if __name__ == "__main__":
	import fileparser

	for test in TESTS:
		print(getattr(fileparser, test[0])(**test[1]))
