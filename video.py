class Video:
	def __init__(self, width, height, title, music, data_boxes):
		self.width = width
		self.height = height
		self.raw_title = title
		self.music = music
		self.data_boxes = data_boxes

		self.dimensions = [width, height]
		self.title = self.generateTitle()

	def generateTitle(self):
		pass