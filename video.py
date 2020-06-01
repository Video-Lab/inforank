from misc import *

class Video:
	def __init__(self, width, height, title, music, data_boxes):
		self.width = width
		self.height = height
		self.raw_title = title # For filename, etc.
		self.music = music
		self.data_boxes = data_boxes # Boxes used in video

		self.dimensions = [width, height]
		self.title = self.generateTitle() # For video upload / 'pretty title'

	def generateTitle(self):
		return f"Data Comparison: {self.raw_title} | {CHANNEL_NAME}" # Constant from misc file