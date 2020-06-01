class DataBox:
	def __init__(self, width, height, value, unit, unit_place, prefix, suffix, title, color, bg_light_color, bg_medium_color, bg_dark_color, data_image_type, data_image):
		self.value = value
		self.width = width
		self.height = height
		self.unit = unit
		self.unit_place = unit_place
		self.prefix = prefix
		self.suffix = suffix
		self.title = title
		self.color = color
		self.bg_light_color = bg_light_color
		self.bg_medium_color = bg_medium_color
		self.bg_dark_color = bg_dark_color
		self.data_image_type = data_image_type
		self.data_image = data_image

		self.dimensions = [width, height]