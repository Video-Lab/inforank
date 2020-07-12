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
		self.addDataUnit()
		self.generateImage()

	def addDataUnit(self):
		if self.unit_place == "before":
			self.data_value = self.unit + self.data_value
		else:
			self.data_value += self.unit

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

	def getDataTitleCoordinates(self): # Coordinates for data title, ...
		value_coords = self.getOuterDataValueCoordinates()
		return [(0,value_coords[1][1]),(self.data_box_width,value_coords[1][1]+(DATA_TITLE_PERCENTAGE*self.data_box_height))]

	def getDataImageCoordiantes(self):
		title_coords = self.getDataTitleCoordinates()
		return [(0,title_coords[1][1]),(self.data_box_width,title_coords[1][1]+(DATA_IMAGE_PERCENTAGE*self.data_box_height))]


	def generateTextFont(self, text, size, bold, box=None): # Generates a safe font and font size to be used within given coordinates with a given text
		if not box:
			box = [(0,0), (self.data_box_width, self.data_box_height)]
		# relative_coords = [(0,0), (coords[1][0]-coords[0][0],coords[1][1]-coords[1][0])]
		if bold:
			font_path = FONT_BOLD
		else:
			font_path = FONT_REGULAR

		# font = ImageFont.truetype(font=font_path,size=int((((TEXT_PERCENTAGE*relative_coords[1][0])/max(1,len(text))))*0.75)) # Size estimate, convert px to pt

		font = ImageFont.truetype(font=font_path, size=size)
		
		w,h = box[1][0]-box[0][0],box[1][1]-box[0][1]
		w *= TEXT_PERCENTAGE
		for i in range(font.size, 0, -1):
			text_size = font.getsize(text)
			if text_size[0] > w or text_size[1] > h:
				font = ImageFont.truetype(font=font_path, size=font.size-1)
			else:
				break
		return font

	def writeText(self, img, text, font, color, coords): # Writes the text with the given font and coordinates, making sure to horizontally center.

		draw = ImageDraw.Draw(img, mode='RGB')
		text_size = font.getsize(text)
		w,h = [coords[1][0]-coords[0][0], coords[1][1]-coords[0][1]] # width and height
		left_pad = (w-text_size[0])/2
		corner = [coords[0][0]+left_pad-font.getoffset(text)[0], coords[0][1]-font.getoffset(text)[1]]
		draw.text(corner, text, font=font, fill=color)
		# draw.rectangle([tuple(corner), (corner[0]+text_size[0], corner[1]+text_size[1])], outline='black') # Border around text
		return img

	def getImage(self): # Gets the image from the file or icon API, error checking included
		pass

	def writeDataValue(self, img): # Writes data value text (specific call to writeText)
		inner_coords = self.getInnerDataValueCoordinates()
		w,h = [inner_coords[1][0]-inner_coords[0][0], inner_coords[1][1]-inner_coords[0][1]] # width and height

		# #Getting fonts
		text_color = getGoodTextColor(self.color)
		prefix_font = self.generateTextFont(self.prefix,size=DATA_VALUE_FONT_SECONDARY,  bold=False, box=inner_coords) # Making sure to fit in box (height doesn't matter)
		main_font = self.generateTextFont(self.data_value,size=DATA_VALUE_FONT_MAIN,  bold=True, box=inner_coords) # ...
		suffix_font = self.generateTextFont(self.suffix, size=DATA_VALUE_FONT_SECONDARY, bold=False, box=inner_coords)

		# Fit text to boxes (reduce size if needed)

		# # Calculating coords for text boxes
		prefix_size = np.subtract(prefix_font.getsize(self.prefix), prefix_font.getoffset(self.prefix))
		main_size = np.subtract(main_font.getsize(self.data_value), main_font.getoffset(self.data_value))
		suffix_size = np.subtract(suffix_font.getsize(self.suffix), suffix_font.getoffset(self.suffix))

		top_padding = (h - (prefix_size[1] + main_size[1] + suffix_size[1] + (2*TEXT_PADDING) ) )/2 # Inner data value height - text w/ padding height / 2

		prefix_coords = [ (inner_coords[0][0], inner_coords[0][1]+top_padding) , (inner_coords[1][0], inner_coords[0][1]+top_padding+prefix_size[1]) ]

		main_coords = [ (prefix_coords[0][0], prefix_coords[1][1]+TEXT_PADDING) , (prefix_coords[1][0], prefix_coords[1][1]+TEXT_PADDING+main_size[1]) ]

		suffix_coords = [ (main_coords[0][0], main_coords[1][1]+TEXT_PADDING) , (main_coords[1][0], main_coords[1][1]+TEXT_PADDING+suffix_size[1]) ]

		# #Drawing text
		img = self.writeText(img, self.prefix, prefix_font, text_color, prefix_coords)
		img = self.writeText(img, self.data_value, main_font, text_color, main_coords)
		img = self.writeText(img, self.suffix, suffix_font, text_color, suffix_coords)

		# Draw borders around text areas (debug only)

		# draw = ImageDraw.Draw(img, mode='RGB')
		
		# draw.rectangle(prefix_coords, outline='white')
		# draw.rectangle(main_coords, outline='white')
		# draw.rectangle(suffix_coords, outline='white')

		return img



	def writeDataTitle(self, img): # ...
		text_color = getGoodTextColor(self.bg_light_color)
		title_coords = self.getDataTitleCoordinates()
		title_font = self.generateTextFont(self.data_title,size=DATA_TITLE_FONT,bold=True,box=title_coords)
		title_size = np.subtract(title_font.getsize(self.data_title), title_font.getoffset(self.data_title))
		top_pad = ((title_coords[1][1] - title_coords[0][1]) - title_size[1]) / 2
	
		title_coords_new = [(title_coords[0][0], title_coords[0][1]+top_pad) , (title_coords[1][0], title_coords[1][1])]
		img = self.writeText(img, self.data_title,title_font,text_color,title_coords_new)

		return img

	def writeDataImage(self, img):
		pass

	def generateImage(self): # Generates the image as a whole
		self.image = self.generateImageBase()
		self.image = self.writeDataValue(self.image)
		self.image = self.writeDataTitle(self.image)

	def outputImage(self, out_path): # Writes image to file at out_path
		pass