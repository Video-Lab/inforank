from misc import *

class Video:
	def __init__(self, width, height, title, music, data_boxes):
		self.width = int(width)
		self.height = int(height)
		self.raw_title = title # For filename, etc.
		self.music = music
		self.data_boxes = data_boxes # Boxes used in video

		self.image = None # Eventual video image
		self.image_pixels = None # Pixels of image
		self.frames = [] # Array used to store frames for video
		self.dimensions = [width, height]
		self.title = self.generateTitle() # For video upload / 'pretty title'

	def generateTitle(self):
		return f"Data Comparison: {self.raw_title} | {CHANNEL_NAME}" # Constant from misc file

	def previewDataBoxes(self):
		print("== PREVIEWING DATA BOXES ==\n")
		for data_box in self.data_boxes:

			print(f"Previewing {data_box.data_string}")
			ok = False

			while not ok:
				data_box.image.show()

				# Checks if already icon, asks to pull new icon for ease of access (most likely change)
				if data_box.data_image_type == "icon":
					new_icon = input("Pull new icon? [y/n]: ").strip().lower()[0]
					if new_icon == "y":

						# If there are icons to pull from, change and restart preview
						if len(data_box.icon_urls) > 0:
							data_box.popDataIcon()
							continue

						else:
							print("No more icons to try. Change the icon query or image type in the next step.")

				# Checks if good, handling bad inputs
				good = input("Data box is good? [y/n]: ").strip().lower()[0]
				while good != "y" and good != "n":
					good = input("Please enter a valid value: ").strip().lower()[0]
				
				# If user likes data box, exits preview
				if good == "y":
					ok = True

				else:
					# Used to store new values, defaults to existing value
					new_values = {
						'prefix': data_box.prefix,
						'data_value': data_box.data_value,
						'unit': data_box.unit,
						'unit_place': data_box.unit_place,
						'suffix': data_box.suffix,
						'data_title': data_box.data_title,
						'image_type': '',
						'color': data_box.color,
						'bg_light_color': data_box.bg_light_color,
						'bg_color': data_box.bg_color
					}

					#Information included in the change prompt
					new_value_settings = {
						'prefix': '',
						'data_value': '',
						'unit': '',
						'unit_place': 'before/after',
						'suffix': '',
						'data_title': '',
						'image_type': 'file/icon',
						'color': 'BG color for data value, hex',
						'bg_light_color': 'color for title bar, hex',
						'bg_color': 'color for image section, hex'
					}

					# Values to change
					to_change = input("""Enter the changes you would like to make, separating multiple changes with a comma 
[prefix,data_value,unit,unit_place,suffix,data_title,image_type,color,bg_color,bg_light_color]: """)
					to_change = to_change.strip().lower().split(",")

					#Ask for new values based on input above
					for changed in to_change:
						new_values[changed] = input(f"Enter new {changed} [{new_value_settings[changed]}]: ")
					
					#Set data box values based on inputs
					data_box.prefix = new_values['prefix']
					data_box.data_value = new_values['data_value']
					data_box.unit = new_values['unit']
					data_box.unit_place = new_values['unit_place']
					data_box.suffix = new_values['suffix']
					data_box.data_title = new_values['data_title']
					data_box.color = new_values['color']
					data_box.bg_light_color = new_values['bg_light_color']
					data_box.bg_color = new_values['bg_color']
					
					if new_values['image_type'] != "":

						#If file, change type to file and ask for path
						if new_values['image_type'] == "file":
							data_box.setDataImageType("file")
							file_path = input("Enter path to image: ")
							data_box.data_image = file_path

						#If icon, change type to icon and ask for queries
						elif new_values['image_type'] == "icon":
							data_box.setDataImageType("icon")
							query = input("Enter icon querie(s), comma-separated: ")
							data_box.data_image = query

					data_box.generateImage()

	def outputDataBoxes(self, out_dir):
		for i in range(len(self.data_boxes)):
			path = os.path.abspath(os.path.join(out_dir, f"{self.raw_title}_databox_{i}.png"))
			if os.path.exists(path):
				os.remove(path)
			self.data_boxes[i].outputImage(path)

	def outputDataBoxFromIndex(self, index, out_dir):
		path = os.path.abspath(os.path.join(out_dir, f"{self.raw_title}_databox_{index}.png"))
		if os.path.exists(path):
			os.remove(path)
		self.data_boxes[index].outputImage(path)

	def generateVideoImageBase(self):
		# Generates base of image used to create video frames
		size = ( int( ( len(self.data_boxes) * (DATA_BOX_PERCENTAGE*self.width) ) + ( (len(self.data_boxes)+1) * (GAP_PERCENTAGE*self.width) ) ) , int(self.height) )
		img = Image.new("RGBA",size,getColorComplement(self.data_boxes[0].bg_color, shift=-25))
		return img
	
	def fillVideoImage(self, img):
		# Place data box images on the video image
		gap = int(GAP_PERCENTAGE*self.width)
		x = gap

		for i in range(len(self.data_boxes)):
			img.paste(self.data_boxes[i].image, (x,0))
			x += self.data_boxes[i].data_box_width + gap
		
		return img
			

	def generateVideoImage(self):
		self.image = self.generateVideoImageBase()
		self.image = self.fillVideoImage(self.image)
		return self.image

	def outputVideoImage(self, out_path):
		self.image.save(os.path.abspath(out_path))

	def generateVideoFrames(self):
		# Generates the frames used to create the video
		self.image_pixels = np.array(self.image.getdata()) # Gets pixel values of image

		#Resize to rows-columns-colors shape
		self.image_pixels = self.image_pixels.reshape( (self.image.size[1], self.image.size[0], 4) )
		shape = self.image_pixels.shape

		#Markers for sliding window
		x1 = 0
		x2 = self.width

		# While right marker not at end
		while x2 < shape[1]:

			#Slice of image to fit video dimensions, remove alpha component
			self.frames.append(self.image_pixels[0:shape[0],x1:x2,:3])

			# If the right marker is closer to the end than the ppf value, add remaining pixel value
			if shape[1]-x2 < PPF:
				x1 += shape[1]-x2
				x2 += shape[1]-x2

			# Otherwise, shift normally
			else:
				x1 += PPF
				x2 += PPF
		
		return self.frames

	def setFade(self, direction):
		# Creates frames for a fade, either in or out
		debugMessage(f"Setting fade for direction {direction}")

		# Get number of frames from FPS and fade time set in settings
		num_fade_frames = int(FPS*FADE_TIME)


		# Base frame either beginning or end based on dir
		if direction == "in":
			base_frame = self.frames[0]

		elif direction == "out":
			base_frame = self.frames[len(self.frames)-1]

		# Empty frame array based on shape of base frame
		fade_frames = np.empty((num_fade_frames, *base_frame.shape))

		# Loop through number of frames, set up percentage completion
		for i in range(num_fade_frames):
			percentage = i/num_fade_frames

			debugMessage(f"{direction}-fade {percentage*100}% complete")
			
			# Loop through each pixel
			for row in range(len(base_frame)):
				for column in range(len(base_frame[row])):
					
					# If in, move from fade color to pixel color based on %, set frame pixel to that value
					if direction == "in":
						fade_frames[i][row][column] = [ math.floor( percentBetweenNumbers(FADE_COLOR[v],base_frame[row][column][v],percentage) ) for v in range(len(base_frame[row][column])) ]

					# If out, move from PIXEL COLOR to fade color instead.
					elif direction == "out":
						fade_frames[i][row][column] = [ math.floor( percentBetweenNumbers(base_frame[row][column][v],FADE_COLOR[v],percentage) ) for v in range(len(base_frame[row][column])) ]

		# If in, add frames to fade frames
		if direction == "in":
			self.frames = np.concatenate((fade_frames, self.frames), axis=0)

		# For out, reversed
		elif direction == "out":
			self.frames = np.concatenate((self.frames, fade_frames), axis=0)

		return self.frames
