# Constants for general info, user-specfic global data, etc.
DEFAULTS = {'prefix': '', 'width': 1920, 'title': '', 'unit': '', 'unit_place': 'after', 'prefix': '', 'suffix': '', 'color': [21, 64, 16],
'bg_light_color': [217, 217, 217], 'bg_color': [46, 46, 46], 'music': '', 'data_image_type': 'file', 'data_image': './assets/none.png'}
CHANNEL_NAME = "InfoRank"
NUM_BOXES = 4 "Number of boxes that can fit on the screen"


def hexToRGB(color):
	pass

def RGBToHex(color):
	pass

def hexToDec(hex):
	pass

def getColorComplement(color, shift=20):
	pass

def getPairsInList(pair_set, target_list):
	return {k:v for k,v in pair_set.items() if k in target_list}