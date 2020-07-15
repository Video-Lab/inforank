import numpy as np
import os
import requests
import time
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import math
from moviepy import ImageSequenceClip, AudioFileClip
from moviepy.editor import *
from .settings import *
 
if not ICONFINDER_API_KEY:
	raise ValueError("IconFinder API key not found.")

def hexToRGB(color):
	if color[0] == "#":
		color = color[1:] # Remove hash

	return tuple([int(color[0:2],16), int(color[2:4],16), int(color[4:6],16)])

def RGBToHex(color):
	return "#" + hex(color[0])[2:] + hex(color[1])[2:] + hex(color[2])[2:] # Remove 0x at start

def getColorComplement(color, shift=45):
	if type(color) == str:
		color = hexToRGB(color)
		return RGBToHex([max(0, min(255,c+shift)) for c in color]) # Add to RGB compoenents, cap at 255
	else:
		return tuple([max(0, min(255,c+shift)) for c in color]) # Same but no conversion to rgb tuple

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

def percentBetweenNumbers(a,b,p):
	# Create linear graph from (0,a) to (0,b), use function to calculate value from percentage (0 -> 1)
	return ((b-a)*p)+a

def debugMessage(m):
	# Prints message if debug is true
	if DEBUG:
		print(m)