from misc import *

class DataBox:
	def __init__(self, width, height, value, unit, unit_place, prefix, suffix, title, color, bg_light_color, bg_color, data_image_type, data_image):
		self.value = value # The data to be displayed
		self.width = width
		self.height = height
		self.unit = unit # Units for the data
		self.unit_place = unit_place # Before or After
		self.prefix = prefix # Taxt above value
		self.suffix = suffix # Text below value
		self.title = title # Label
		self.color = color # Color of value background
		self.bg_light_color = bg_light_color # Title bg color
		self.bg_color = bg_color # Image bg color
		self.data_image_type = data_image_type # File or icon
		self.data_image = data_image # Path or search terms

		self.dimensions = [width, height]
		self.light_color = getComplement(self.color) # Get lighter color from misc function