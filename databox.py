from misc import *
from PIL import Image, ImageDraw, ImageFont

class DataBox:

	@classmethod
	def calculateDataBoxWidth(cls, width):
		return DATA_BOX_PERCENTAGE*int(width)

	def __init__(self, data_box_width, data_box_height, data_value, unit, unit_place, prefix, suffix, data_title, color, bg_light_color, bg_color, data_image_type, data_image):
		self.data_value = data_value # The data to be displayed
		self.data_box_width = int(data_box_width)
		self.data_box_height = int(data_box_height)
		self.unit = unit # Units for the data
		self.unit_place = unit_place # Before or After
		self.prefix = prefix # Taxt above value
		self.suffix = suffix # Text below value
		self.data_title = data_title # Label
		self.pad=DATA_VALUE_PADDING_PERCENTAGE*self.data_box_width
		if type(color) == str:
			self.color = hexToRGB(color)
		else:
			self.color = color # Color of value background

		if type(bg_light_color) == str:
			self.bg_light_color = hexToRGB(bg_light_color)
		else:
			self.bg_light_color = bg_light_color # Title bg color

		if type(bg_color) == str:
			self.bg_color = hexToRGB(bg_color)
		else:
			self.bg_color = bg_color # Image bg color
	
		self.data_image_type = data_image_type # File or icon
		self.data_image = data_image # Path or search terms

		self.dimensions = [self.data_box_width, self.data_box_height]
		self.light_color = getColorComplement(self.color) # Get lighter color from misc function
		self.image = self.generateImage()


	def generateImageBase(self): # Base of the image with base colors, no text or images
		img = Image.new('RGB', self.dimensions) #Create blank image with right dimensions
		draw = ImageDraw.Draw(img, mode='RGB') # Drawing ctx
		draw.rectangle(self.getOuterDataValueCoordinates(), fill=self.light_color) # Drawing for light color border around value
		draw.rectangle(self.getInnerDataValueCoordinates(), fill=self.color) # Inner data value box
		draw.rectangle(self.getDataTitleCoordinates(), fill=self.bg_light_color) # Title strip
		draw.rectangle(self.getDataImageCoordiantes(), fill=self.bg_color) # Image box
		return img

	def getOuterDataValueCoordinates(self): # Coordinates for safe data value box
		return [(0,0) ,(self.data_box_width,DATA_VALUE_PERCENTAGE*self.data_box_height)]

	def getInnerDataValueCoordinates(self):
		return [(self.pad,self.pad),(self.data_box_width-self.pad,DATA_VALUE_PERCENTAGE*self.data_box_height-self.pad)]

	def getDataTitleCoordinates(self): # Coordinates for data title, you get the idea
		value_coords = self.getOuterDataValueCoordinates()
		return [(0,value_coords[1][1]),(self.data_box_width,value_coords[1][1]+(DATA_TITLE_PERCENTAGE*self.data_box_height))]

	def getDataImageCoordiantes(self):
		title_coords = self.getDataTitleCoordinates()
		return [(0,title_coords[1][1]),(self.data_box_width,title_coords[1][1]+(DATA_IMAGE_PERCENTAGE*self.data_box_height))]


	def generateTextFont(self, text, coords, bold, color): # Generates a safe font and font size to be used within given coordinates with a given text
		relative_coords = [(0,0), (coords[1][0]-coords[0][0],coords[1][1]-coords[1][0])]
		if bold:
			font_path = FONT_BOLD
		else:
			font_path = FONT_REGULAR

		font = ImageFont.truetype(font=font_path,size=floor(((TEXT_PERCENTAGE*relative_coords[1][0])/len(text))*0.75),fill=color) # Size estimate, convert px to pt

		return font

	def writeText(self, img, text, font, coords): # Writes the text with the given font and coordinates, making sure to horizontally center.
		pass

	def getImage(self): # Gets the image from the file or icon API, error checking included
		pass

	def writeDataValue(self, img): # Writes data value text (specific call to writeText)
		pass

	def writeDataTitle(self, img): # ...
		pass

	def writeDataImage(self, img):
		pass

	def generateImage(self): # Generates the image as a whole
		pass

	def outputImage(self, out_path): # Writes image to file at out_path
		pass