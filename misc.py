import numpy as np
import os
# Constants for general info, user-specfic global data, etc.
DEFAULTS = {'prefix': '', 'width': 1920, 'title': '', 'unit': '', 'unit_place': 'after', 'prefix': '', 'suffix': '', 'color': (21, 64, 16),
'bg_light_color': (217, 217, 217), 'bg_color': (46, 46, 46), 'music': '', 'data_image_type': 'file', 'data_image': './assets/none.png'}
FPS = 60 # Frames per second
CHANNEL_NAME = "InfoRank"
NUM_BOXES = 4 # "Number of boxes that can fit on the screen"
GAP_PERCENTAGE = 0.05 # % of video width taken up by a gap
DATA_BOX_PERCENTAGE = (1/NUM_BOXES)-((GAP_PERCENTAGE*(NUM_BOXES-1))/NUM_BOXES) #  % of width taken up by single data box
DATA_VALUE_PERCENTAGE = 0.50
DATA_TITLE_PERCENTAGE = 0.08
DATA_IMAGE_PERCENTAGE = 0.54
DATA_VALUE_PADDING_PERCENTAGE = 0.15*DATA_BOX_PERCENTAGE # % of WIDTH
FONT_REGULAR = "./assets/Mukta-ExtraLight.ttf"
FONT_BOLD = "./assets/Mukta-Bold.ttf"
# TEXT_PERCENTAGE = 0.95 # % of width of any line taken up by text
TEXT_COLOR_THRESHOLD = 150 # When to start drawing black text instead of white text. 
DATA_VALUE_FONT_SECONDARY = 40
DATA_VALUE_FONT_MAIN = 120
TEXT_PADDING = 40 # Pixel padding between lines
DATA_TITLE_FONT = 55


def hexToRGB(color):
	if color[0] == "#":
		color = color[1:] # Remove hash

	return tuple([int(color[0:2],16), int(color[2:4],16), int(color[4:6],16)])

def RGBToHex(color):
	return "#" + hex(color[0])[2:] + hex(color[1])[2:] + hex(color[2])[2:] # Remove 0x at start

# def hexToDec(hex_val):
# 	hex_val = hex_val.lower()
# 	hex_values = "abcdef"
# 	hex_map = {hex_val[i]: i+10 for i in range(len(hex_val))}
# 	for i in range(10):
# 		hex_map[str(i)] = i 
# 	return sum([16**(len(hex_val)-i) * hex_map[str(char)] for char in hex_val])

# def decToHex(dec):
# 	hex_val = hex_val.lower()
# 	hex_values = "abcdef"
# 	hex_map = {hex_val[i]: i+10 for i in range(len(hex_val))}
# 	for i in range(10):
# 		hex_map[str(i)] = i 
	

def getColorComplement(color, shift=45):
	if type(color) == str:
		color = hexToRGB(color)
		return RGBToHex([min(255,c+shift) for c in color]) # Add to RGB compoenents, cap at 255
	else:
		return tuple([min(255,c+shift) for c in color]) # Same but no conversion to rgb tuple

def getPairsInList(pair_set, target_list):
	return {k:v for k,v in pair_set.items() if k in target_list}


def getGoodTextColor(color): # Gives a good color for drawing text based on given color.
	return_hex = False
	return_color = (250, 250, 250)
	if type(color) == str:
		return_hex=True
		color = hexToRGB(color)

	if sum(color)/3 > TEXT_COLOR_THRESHOLD:
		return_color = (13, 13, 13)

	if return_hex:
		return RGBToHex(return_color)
	return return_color
