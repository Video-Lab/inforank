from misc import *
from PIL import Image, ImageDraw, ImageFont

class DataBox:

	@classmethod
	def calculateDataBoxWidth(cls, width):
		return DATA_BOX_PERCENTAGE*int(width)

	def __init__(self, data_box_width, data_box_height, data_value, unit, unit_place, prefix, suffix, data_title, color, bg_light_color, bg_color, data_image_type, data_image):
		self.data_value = data_value # The data to be displayed
		self.data_box_width = data_box_width
		self.data_box_height = data_box_height
		self.unit = unit # Units for the data
		self.unit_place = unit_place # Before or After
		self.prefix = prefix # Taxt above value
		self.suffix = suffix # Text below value
		self.data_title = data_title # Label
		self.color = color # Color of value background
		self.bg_light_color = bg_light_color # Title bg color
		self.bg_color = bg_color # Image bg color
		self.data_image_type = data_image_type # File or icon
		self.data_image = data_image # Path or search terms

		self.dimensions = [data_box_width, data_box_height]
		self.light_color = getColorComplement(self.color) # Get lighter color from misc function
		self.image = self.generateImage()


	def generateImageBase(self): # Base of the image with base colors, no text or images
		pass

	def getDataValueCoordinates(self): # Coordinates for safe data value box
		pass

	def getDataTitleCoordinates(self): # Coordinates for data title, you get the idea
		pass

	def getDataImageCoordiantes(self):
		pass

	def generateTextFont(self, text, x1, y1, x2, y2): # Generates a safe font and font size to be used within given coordinates with a given text
		pass

	def writeText(self, text, font, x1, y1, x2, y2): # Writes the text with the given font and coordinates, making sure to horizontally center.
		pass

	def getImage(self): # Gets the image from the file or icon API, error checking included
		pass

	def writeDataValue(self): # Writes data value text (specific call to writeText)
		pass

	def writeDataTitle(self): # ...
		pass

	def writeDataImage(self):
		pass

	def generateImage(self): # Generates the image as a whole
		pass

	def outputImage(self, out_path): # Writes image to file at out_path
		pass