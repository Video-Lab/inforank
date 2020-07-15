from misc import *

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
		self.icon_urls = [] # URLs for multiple icons (If needed)
		self.data_string = "" # Identifier showing prefix, main value, suffix, and title of data box
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
		self.generateDataString()
		self.generateImage()

	def setDataImageType(self, new_type):
		self.data_image_type = new_type
		return self.data_image_type

	def printInformation(self):
		# Prints information about the data box
		print(f"=== {self.data_string} ===\n")
		print(f"Prefix: {self.prefix}\n")
		print(f"Suffix: {self.suffix}\n")
		print(f"Unit & Unit place: {self.unit} - {self.unit_place}\n")
		print(f"Value: {self.data_value}\n")
		print(f"Title: {self.data_title}\n")
		print(f"Image & image type: {self.data_image_type} - {self.data_image}\n")
		print(f"Main color: {self.color}\n")
		print(f"Light color: {self.light_color}\n")
		print(f"Title background color: {self.bg_light_color}\n")
		print(f"Image background color: {self.bg_color}\n")
		print("=== ===\n\n")

	def addDataUnit(self):
		#Add unit
		if self.unit_place == "before":
			main = self.unit + self.data_value
		else:
			main = self.data_value + self.unit
		return main

	def generateImageBase(self): # Base of the image with base colors, no text or images
		img = Image.new('RGB', self.dimensions) #Create blank image with right dimensions
		draw = ImageDraw.Draw(img, mode='RGB') # Drawing ctx
		draw.rectangle(self.getOuterDataValueCoordinates(), fill=self.light_color) # Drawing for light color border around value
		draw.rectangle(self.getInnerDataValueCoordinates(), fill=self.color) # Inner data value box
		draw.rectangle(self.getDataTitleCoordinates(), fill=self.bg_light_color) # Title strip
		draw.rectangle(self.getDataImageCoordinates(), fill=self.bg_color) # Image box
		return img

	def getOuterDataValueCoordinates(self): # Coordinates for safe data value box
		return [(0,0) ,(int(self.data_box_width),int(DATA_VALUE_PERCENTAGE*self.data_box_height))]

	def getInnerDataValueCoordinates(self):
		return [(int(self.pad),int(self.pad)),(int(self.data_box_width-self.pad),int(DATA_VALUE_PERCENTAGE*self.data_box_height-self.pad))]

	def getDataTitleCoordinates(self): # Coordinates for data title, ...
		value_coords = self.getOuterDataValueCoordinates()
		return [(0,value_coords[1][1]),(int(self.data_box_width),int(value_coords[1][1]+(DATA_TITLE_PERCENTAGE*self.data_box_height)))]

	def getDataImageCoordinates(self):
		title_coords = self.getDataTitleCoordinates()
		return [(0,title_coords[1][1]),(self.data_box_width,int(title_coords[1][1]+(DATA_IMAGE_PERCENTAGE*self.data_box_height)))]

	def getSafeDataImageCoordinates(self): # Get area for image to be placed in box
		image_coords = self.getDataImageCoordinates()
		x_pad = int( (DATA_IMAGE_PADDING_PERCENTAGE*(image_coords[1][0]-image_coords[0][0]))/2 )
		y_pad = int( (DATA_IMAGE_PADDING_PERCENTAGE*(image_coords[1][1]-image_coords[0][1]))/2 )
		return [(x_pad,image_coords[0][1]+y_pad),(self.data_box_width-x_pad,int(image_coords[1][1]-y_pad))]

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

	def writeText(self, img, text, font, color, coords):
		# Writes the text with the given font and coordinates, making sure to horizontally center.

		#Set up draw ctx, font
		draw = ImageDraw.Draw(img, mode='RGB')
		text_size = font.getsize(text)

		#Calculate boxes, coordinates, horizontal centering
		w,h = [coords[1][0]-coords[0][0], coords[1][1]-coords[0][1]] # width and height
		left_pad = (w-text_size[0])/2
		corner = [coords[0][0]+left_pad-font.getoffset(text)[0], coords[0][1]-font.getoffset(text)[1]]

		draw.text(corner, text, font=font, fill=color)

		# Border around text (debug only)
		# draw.rectangle([tuple(corner), (corner[0]+text_size[0], corner[1]+text_size[1])], outline='black')
		return img

	def writeDataValue(self, img): # Writes data value text (specific call to writeText)
		inner_coords = self.getInnerDataValueCoordinates()
		w,h = [inner_coords[1][0]-inner_coords[0][0], inner_coords[1][1]-inner_coords[0][1]] # width and height

		# #Getting fonts
		text_color = getGoodTextColor(self.color)
		prefix_font = self.generateTextFont(self.prefix,size=DATA_VALUE_FONT_SECONDARY,  bold=False, box=inner_coords) # Making sure to fit in box (height doesn't matter)
		main_font = self.generateTextFont(self.data_value,size=DATA_VALUE_FONT_MAIN,  bold=True, box=inner_coords) # ...
		suffix_font = self.generateTextFont(self.suffix, size=DATA_VALUE_FONT_SECONDARY, bold=False, box=inner_coords)

		# Fit text to boxes (reduce size if needed)

		# Calculating coords for text boxes
		prefix_size = np.subtract(prefix_font.getsize(self.prefix), prefix_font.getoffset(self.prefix))
		main_size = np.subtract(main_font.getsize(self.data_value), main_font.getoffset(self.data_value))
		suffix_size = np.subtract(suffix_font.getsize(self.suffix), suffix_font.getoffset(self.suffix))

		top_padding = (h - (prefix_size[1] + main_size[1] + suffix_size[1] + (2*TEXT_PADDING) ) )/2 # Inner data value height - text w/ padding height / 2

		prefix_coords = [ (inner_coords[0][0], inner_coords[0][1]+top_padding) , (inner_coords[1][0], inner_coords[0][1]+top_padding+prefix_size[1]) ]

		main_coords = [ (prefix_coords[0][0], prefix_coords[1][1]+TEXT_PADDING) , (prefix_coords[1][0], prefix_coords[1][1]+TEXT_PADDING+main_size[1]) ]

		suffix_coords = [ (main_coords[0][0], main_coords[1][1]+TEXT_PADDING) , (main_coords[1][0], main_coords[1][1]+TEXT_PADDING+suffix_size[1]) ]

		main = self.addDataUnit()
		#Drawing text
		img = self.writeText(img, self.prefix, prefix_font, text_color, prefix_coords)
		img = self.writeText(img, main, main_font, text_color, main_coords)
		img = self.writeText(img, self.suffix, suffix_font, text_color, suffix_coords)

		# Draw borders around text areas (debug only)
		# draw = ImageDraw.Draw(img, mode='RGB')
		
		# draw.rectangle(prefix_coords, outline='white')
		# draw.rectangle(main_coords, outline='white')
		# draw.rectangle(suffix_coords, outline='white')

		return img

	def writeDataTitle(self, img): 
		
		# Gets title colors and size
		text_color = getGoodTextColor(self.bg_light_color)
		title_coords = self.getDataTitleCoordinates()
		title_font = self.generateTextFont(self.data_title,size=DATA_TITLE_FONT,bold=True,box=title_coords)

		# Adjusts box based on font offset & centers title
		title_size = np.subtract(title_font.getsize(self.data_title), title_font.getoffset(self.data_title))
		top_pad = ((title_coords[1][1] - title_coords[0][1]) - title_size[1]) / 2

		# Gets new title co-ordinates & writes text from internal functions
		title_coords_new = [(title_coords[0][0], title_coords[0][1]+top_pad) , (title_coords[1][0], title_coords[1][1])]
		img = self.writeText(img, self.data_title,title_font,text_color,title_coords_new)

		return img

	def getDataImage(self):
		# Checks if data type is loading from file
		if self.data_image_type == "file":
			# Open from given path and convert to RGBA for transparency
			img = Image.open(os.path.abspath(self.data_image)).convert("RGBA")
		else:
			# Call to function that gets icon
			img = self.getDataIcon()
		return img

	def getDataIcon(self):

		# Auth from environment variable
		headers = {'Authorization': 'Bearer ' + ICONFINDER_API_KEY}

		# Declaration to be used for later
		img = None

		# Split for multiple terms, remove spaces from each term
		queries = [query.strip() for query in self.data_image.split(",")]

		for query in queries:

			# Don't include vector icons, max 10, query from data image value
			url = "https://api.iconfinder.com/v4/icons/search?query=" + query + "&count=10&vector=0&premium=0"

			# Default value as fallback in case of API error
			img_url = os.path.abspath("./assets/none.png")

			resp = requests.get(url, headers=headers)

			# Checks if too many requests (HTTP Code 429)
			while resp.status_code == 429:
				# Tries request every second until timeout ends
				print("Too many requests to IconFinder API. Waiting 1 second...")
				time.sleep(1)
				resp = requests.get(url, headers=headers)

			# Other than OK code
			if resp.status_code != 200:
				# Loads image from fallback URL
				print("Error in connection with error code " + resp.status_code + ", defaulting to none.png")
				img = Image.open(img_url).convert("RGBA")
			
			else:
				#Convert to JSON, pull URL to image from largest size raster images, stores all image URLs for preview later
				resp = resp.json()
				for icon in resp['icons']:
					biggest = len(icon['raster_sizes'])-1

					#Checks if icon is under size
					if icon['raster_sizes'][biggest]['size_width'] < MIN_SIZE[0] or icon['raster_sizes'][biggest]['size_height'] < MIN_SIZE[1]:
						continue

					self.icon_urls.append(icon['raster_sizes'][biggest]['formats'][0]["preview_url"])

		# Get first icon URL
		img_url = self.icon_urls[0]
		img = self.getDataIconFromURL(img_url).convert("RGBA")

		return img

	def getDataIconFromURL(self, url):
		# Loads image from external URL
		return Image.open(BytesIO(requests.get(url).content))

	def writeDataImage(self, img, data_img):
		# Gets the image and image coordinates, other calculations and declarations
		data_img = self.getDataImage()
		image_coords = self.getSafeDataImageCoordinates()
		w,h = image_coords[1][0] - image_coords[0][0], image_coords[1][1]-image_coords[0][1]
		newsize = list(data_img.size)
		ratio = newsize[1] / newsize[0]
		bigger = None

		# Checks if either width or height is bigger than given width/height. If both, will resize based on height.
		if data_img.size[0] > w:
			bigger = "w"
		if data_img.size[1] > h:
			bigger = "h"
		

		#Resizes image based on oversized axis from previous conditional, adjusts opposite axis based on aspect ratio
		if bigger == "w":
			newsize[0] = int(IMAGE_PERCENTAGE[0]*w)
			newsize[1] = int(ratio*newsize[0])
		elif bigger == "h":
			newsize[1] = int(IMAGE_PERCENTAGE[1]*h)
			newsize[0] = int((1/ratio)*newsize[1])

		# Calculates padding to center image in safe box
		left_pad = int((w-newsize[0])/2)
		top_pad = int((h-newsize[1])/2)
		
		#Resize & overlay image
		data_img = data_img.resize(newsize)
		img.paste(data_img, [image_coords[0][0]+left_pad, image_coords[0][1]+top_pad], mask=data_img)

		return img

	def popDataIcon(self):
		#Uses next icon URL in list & re-generates image
		self.icon_urls.pop(0)
		img_url = self.icon_urls[0]
		img = self.getDataIconFromURL(img_url).convert("RGBA")

		self.image = self.generateImageBase()
		self.image = self.writeDataValue(self.image)
		self.image = self.writeDataTitle(self.image)
		self.image = self.writeDataImage(self.image, img)


	def generateImage(self):
		# Generates the image as a whole
		self.image = self.generateImageBase()
		self.image = self.writeDataValue(self.image)
		self.image = self.writeDataTitle(self.image)
		self.image = self.writeDataImage(self.image, self.getDataImage())
		return self.image

	def outputImage(self, out_path):
		# Writes image to file at out_path
		self.image.save(os.path.abspath(out_path))

	def generateDataString(self):
		# Generates string with prefix, value, suffix, and title
		if self.unit_place == "before":
			main = self.unit + self.data_value
		else:
			main = self.data_value + self.unit
		self.data_string = f"{self.prefix} {main} {self.suffix} - {self.data_title}"
		return self.data_string