from importlib import import_module


# Testing info
TESTS = [["parseFile", {'path': './tests/testfile.txt'}]]

if __name__ == "__main__":
	for test in TESTS:
		test[0](**test[1])
