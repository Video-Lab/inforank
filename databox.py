from misc import *

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