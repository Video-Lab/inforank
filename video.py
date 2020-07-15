from misc import *

class Video:
	def __init__(self, width, height, title, music, data_boxes, out_path):
		self.width = int(width)
		self.height = int(height)
		self.raw_title = self.generateRawTitle(title) # For filename, etc.
		self.music = music
		self.data_boxes = data_boxes # Boxes used in video
		self.out_path = self.setupDirectoryStructure() # Path to output assets and video to

		self.image = None # Eventual video image
		self.image_pixels = None # Pixels of image
		self.frames = [] # Array used to store frames for video
		self.clip = None # Video clip to be used
		self.dimensions = [width, height]
		self.title = self.generateTitle(title) # For video upload / 'pretty title'

	def generateRawTitle(self, title):
		debugMessage("Generating raw title")
		new_title = title
		for forbidden in "\\/:*?\"<>|":
			new_title.replace(forbidden, "_")

		return new_title.lower().replace(" ", "_")

	def generateTitle(self, title):
		debugMessage("Generating main title")
		return f"Data Comparison: {title} | {CHANNEL_NAME}" # Constant from misc file

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
		debugMessage("Writing data boxes to files")
		for i in range(len(self.data_boxes)):
			debugMessage("Writing data box to " + os.path.join(out_dir, f"{self.raw_title}_data_box_{i}.png"))
			path = os.path.abspath(os.path.join(out_dir, f"{self.raw_title}_data_box_{i}.png"))
			if os.path.exists(path):
				os.remove(path)
			self.data_boxes[i].outputImage(path)

	def outputDataBoxFromIndex(self, index, out_dir):
		debugMessage("Outputting data box to " + out_dir + " at index " + index)
		path = os.path.abspath(os.path.join(out_dir, f"{self.raw_title}_databox_{index}.png"))
		if os.path.exists(path):
			os.remove(path)
		self.data_boxes[index].outputImage(path)

	def generateVideoImageBase(self):
		debugMessage("Generating video image base")
		# Generates base of image used to create video frames
		size = ( int( ( len(self.data_boxes) * (DATA_BOX_PERCENTAGE*self.width) ) + ( (len(self.data_boxes)+1) * (GAP_PERCENTAGE*self.width) ) ) , int(self.height) )
		img = Image.new("RGBA",size,getColorComplement(self.data_boxes[0].bg_color, shift=-25))
		return img
	
	def fillVideoImage(self, img):
		debugMessage("Filling video image")
		# Place data box images on the video image
		gap = int(GAP_PERCENTAGE*self.width)
		x = gap

		for i in range(len(self.data_boxes)):
			img.paste(self.data_boxes[i].image, (x,0))
			x += self.data_boxes[i].data_box_width + gap
		
		return img

	def generateVideoImage(self):
		debugMessage("Generating video image base")
		self.image = self.generateVideoImageBase()
		self.image = self.fillVideoImage(self.image)
		return self.image

	def outputVideoImage(self, out_path):
		debugMessage("Outputting video image to " + out_path)
		self.image.save(os.path.abspath(out_path))

	def generateVideoFrames(self):
		debugMessage("Generating video frames")
		# Generates the frames used to create the video
		self.image_pixels = np.array(self.image.getdata()) # Gets pixel values of image

		#Resize to rows-columns-colors shape
		self.image_pixels = self.image_pixels.reshape( (self.image.size[1], self.image.size[0], 4) )
		shape = self.image_pixels.shape

		#Markers for sliding window
		x1 = 0
		x2 = self.width
		number = 1

		# While right marker not at end
		while x2 < shape[1]:
			debugMessage("Generating frame " + number)
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
		debugMessage(f"Setting {direction}-fade")
		if direction == "in":
			self.clip.fx(vfx.fadein, duration=FADE_TIME, initial_color=FADE_COLOR)
		
		elif direction == "out":
			self.clip.fx(vfx.fadeout, duration=FADE_TIME, initial_color=FADE_COLOR)
		
		return self.clip

	def generateVideoClipFromFrames(self):
		debugMessage("Creating video clip")
		self.clip = ImageSequenceClip(self.frames, fps=FPS)
		if music != "":
			audio_clip = AudioFileClip(os.path.abspath(self.music))
			audio_clip = concatenate_audioclips([audio for i in range(math.ceil(float(self.clip.duration)/float(audio.duration)))])
			audio_clip = audio_clip.set_duration(self.clip.duration)
			self.clip = self.clip.set_audio()
			
		return self.clip

	def outputVideo(self):
		debugMessage("Outputting video")

		if self.clip:
			self.clip.write_videofile(os.path.join(self.out_path, "video.mp4"), **WRITE_SETTINGS)

	def setupDirectoryStructure(self, out_path):
		if not os.path.exists(os.path.join(out_path, "inforank/")):
					os.mkdir(os.path.join(out_path, "inforank"))
		
		os.mkdir(os.path.join(out_path, "inforank", self.raw_title))
		self.out_path = os.path.join(out_path, "inforank", self.raw_title)
		return self.out_path

	def generateVideo(self):
		self.previewDataBoxes()
		debugMessage("Generating full video")
		self.generateVideoImage()
		self.generateVideoFrames()
		self.generateVideoClipFromFrames()
		self.setFade("in")
		self.setFade("out")
		self.outputDataBoxes(os.path.join(self.out_path, "data_boxes"))
		self.outputVideoImage(os.path.join(self.out_path, "video_image.png"))
		self.outputVideo()