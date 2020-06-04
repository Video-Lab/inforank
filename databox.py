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
		img = Image.new('RGB', self.dimensions, [0,0,0]) #Create blank image with right dimensions
		draw = ImageDraw.Draw(img, mode='RGB') # Drawing ctx
		draw.rectangle(self.getOuterDataValueCoordinates(), fill=self.light_color) # Drawing for light color border around value
		draw.rectangle(self.getInnerDataValueCoordinates(), fill=self.color) # Inner data value box
		draw.rectangle(self.getDataTitleCoordinates(), fill=self.bg_light_color) # Title strip
		draw.rectangle(self.getDataImageCoordiantes(), fill=self.bg_color) # Image box
		return img

	def getOuterDataValueCoordinates(self): # Coordinates for safe data value box
		return [0,0,self.data_box_width,DATA_VALUE_PERCENTAGE*self.data_box_height]

	def getInnerDataValueCoordinates(self):
		data_value_inner_width = (1-DATA_VALUE_PADDING_PERCENTAGE)*self.data_box_width
		data_value_inner_height = (1-DATA_VALUE_PADDING_PERCENTAGE)*self.data_box_height

		return [self.data_box_width-data_value_inner_width,self.data_box_height-data_value_inner_height,data_value_inner_width,data_value_inner_height]

	def getDataTitleCoordinates(self): # Coordinates for data title, you get the idea
		value_coords = self.getOuterDataValueCoordinates()
		return [0,value_coords[3],self.data_box_width,value_coords[3]+(DATA_TITLE_PERCENTAGE*self.data_box_height)]

	def getDataImageCoordiantes(self):
		title_coords = self.getDataTitleCoordinates()
		return [0,title_coords[3],self.data_box_width,title_coords[3]+(DATA_IMAGE_PERCENTAGE*self.data_box_height)]


	def generateTextFont(self, text, x0, y0, x1, y1): # Generates a safe font and font size to be used within given coordinates with a given text
		pass

	def writeText(self, img, text, font, x0, y0, x1, y1): # Writes the text with the given font and coordinates, making sure to horizontally center.
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