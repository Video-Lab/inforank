class Video:
	def __init__(self, width, height, title, music, data_boxes):
		self.width = width
		self.height = height
		self.raw_title = title # For filename, etc.
		self.music = music
		self.data_boxes = data_boxes

		self.dimensions = [width, height]
		self.title = self.generateTitle() # For video upload / 'pretty title'

	def generateTitle(self):
		pass