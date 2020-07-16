from misc import *
from databox import DataBox

class Video:

	@classmethod
	def errorCheckFile(cls, path):
		with open(path, 'r') as f:
			begin_settings_index, end_settings_index, begin_data_index, end_data_index = cls.getFileIndexes(path)
			lf = list(f)
			for i in range(begin_settings_index,end_settings_index+1):
				if lf[i] != "\n": # Make sure not new line
					if "=" not in lf[i] or len(lf[i].split("=")) != 2:
						raise ValueError("Error in file at " + path + " at line " + str(i+1))

			for i in range(begin_data_index,end_data_index+1):
				if lf[i] != "\n": # Make sure not new line
					row = lf[i].split("|")
					if len(row) != 4:
						raise ValueError("Error in file at " + path + " at line " + str(i+1))
					else:
						for val in row:
							if "=" not in val or len(val.split("=")) != 2:
								raise ValueError("Error in file at " + path + " at line " + str(i+1))
		return

	@classmethod
	def getFileIndexes(cls, path):
		with open(path, 'r') as f:
			lf = list(f)
			end_data_index = len(lf)-1
			begin_settings_index = 0
			begin_data_index = 0
			end_settings_index = 0
			for i in range(len(lf)):
				if "||BEGIN_DATA||" in lf[i]:
					begin_data_index = i+1
					end_settings_index = i-1
		return [begin_settings_index, end_settings_index, begin_data_index, end_data_index]

	@classmethod
	def fromFile(cls, path):
		debugMessage("Parsing data file at " + path)
		cls.errorCheckFile(path)
		begin_settings_index, end_settings_index, begin_data_index, end_data_index = cls.getFileIndexes(path)

		with open(path, 'r') as f:
			lf = list(f)
			lf = [line.replace("\n", "") for line in lf] # remove new line chars & new lines in general
			settings_rows = lf[begin_settings_index:end_settings_index+1]
			data_rows = lf[begin_data_index:end_data_index+1]

			settings = {setting[0]: setting[1] for setting in [setting_string.split('=') for setting_string in settings_rows if setting_string != ""]} # Parse into dict of key-value pairs, 1 line = 1 pair, remove new lines
			data = [{data_setting.split('=')[0]: data_setting.split('=')[1] for data_setting in row.split('|')} for row in data_rows if row != ""] # Same for data, but 1 line = 1 dict,                      ^^^^^^^^^^^^^^^^

			for d in data: # Replace blank values with defaults from misc.py for settings, data
				for k,v in d.items():
					if d[k] == '':
						d[k] = DEFAULTS[k]

			for k in settings.keys():
				if settings[k] == '':
					settings[k] = DEFAULTS[k]

			settings['data_box_height'] = settings['height']
			settings['data_box_width'] = DataBox.calculateDataBoxWidth(settings['width'])

			data_settings = getPairsInList(settings, ['data_box_width', 'data_box_height', 'data_value', 'unit', 'unit_place', 'prefix', 'suffix', 'data_title', 'color', 'bg_light_color', 'bg_color'])
			video_settings = getPairsInList(settings, ['width', 'height', 'title', 'music', 'out_path', 'gap_color'])

			data_boxes = [DataBox(**data_settings, **data[i], position=len(data)-i) for i in range(len(data))] # Convert data row strings to DataBox classes
			video = cls(**video_settings, data_boxes=data_boxes) # Unpack settings, convert to video class

			return video

	def __init__(self, width, height, title, music, data_boxes, out_path, gap_color):
		self.width = int(width)
		self.height = int(height)
		self.raw_title = self.generateRawTitle(title) # For filename, etc.
		self.music = music
		self.data_boxes = data_boxes # Boxes used in video
		self.out_path = self.setupDirectoryStructure(out_path) # Path to output assets and video to
		self.gap_color = getColorTuple(gap_color)
		self.image = None # Eventual video image
		self.image_pixels = None # Pixels of image
		self.frames = [] # Array used to store frames for video
		self.clip = None # Video clip to be used
		self.dimensions = [width, height]
		self.title = self.generateTitle(title) # For video upload / 'pretty title'
		# self.rankDataBoxes()

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
						'color': 'BG color for data value, hex/RGB',
						'bg_light_color': 'color for title bar, hex/RGB',
						'bg_color': 'color for image section, hex/RGB'
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
		if not os.path.exists(out_dir):
			os.mkdir(out_dir)

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
		img = Image.new("RGBA",size,getColorComplement(self.gap_color, shift=-25))
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
			debugMessage("Generating frame " + str(number))
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
			number += 1
		
		return self.frames

	def setFade(self, direction):
		debugMessage(f"Setting {direction}-fade")
		if direction == "in":
			base_frame = self.frames[0]
			self.clip = concatenate_videoclips([ ImageSequenceClip([base_frame for i in range(math.floor(FPS*FADE_TIME))], fps=FPS), self.clip ])
			self.clip = self.clip.fx(vfx.fadein, duration=FADE_TIME, initial_color=FADE_COLOR)
			self.setMusic()
		
		elif direction == "out":
			base_frame = self.frames[len(self.frames)-1]
			self.clip = concatenate_videoclips([ self.clip, ImageSequenceClip([base_frame for i in range(math.floor(FPS*FADE_TIME))], fps=FPS) ])
			self.clip = self.clip.fx(vfx.fadeout, duration=FADE_TIME, final_color=FADE_COLOR)
			self.setMusic()
		
		return self.clip


	def generateVideoClipFromFrames(self):
		debugMessage("Creating video clip")
		self.clip = concatenate_videoclips([ ImageSequenceClip([self.frames[0] for i in range(math.floor(FPS*BEGINNING_WAIT_TIME))], fps=FPS), ImageSequenceClip(self.frames, fps=FPS), ImageSequenceClip([self.frames[len(self.frames)-1] for i in range(math.floor(FPS*END_WAIT_TIME))], fps=FPS) ])
		self.setMusic()
		return self.clip

	def setMusic(self):
		if self.music != "":
			audio_clip = AudioFileClip(os.path.abspath(self.music))
			audio_clip = concatenate_audioclips([audio_clip for i in range(math.ceil(float(self.clip.duration)/float(audio_clip.duration)))])
			audio_clip = audio_clip.set_duration(self.clip.duration)
			audio_clip = audio_clip.fx(afx.audio_fadein, FADE_TIME).fx(afx.audio_fadeout, FADE_TIME)
			self.clip = self.clip.set_audio(audio_clip)

	def outputVideo(self):
		debugMessage("Outputting video")

		if self.clip:
			self.clip.write_videofile(os.path.join(self.out_path, "video.mp4"), **WRITE_SETTINGS)

	def setupDirectoryStructure(self, out_path):

		if not os.path.exists(os.path.join(out_path, "inforank/")):
					os.mkdir(os.path.join(out_path, "inforank"))

		if not os.path.exists(os.path.join(out_path, "inforank", self.raw_title)):
			os.mkdir(os.path.join(out_path, "inforank", self.raw_title))

		self.out_path = os.path.join(out_path, "inforank", self.raw_title)
		return self.out_path

	def generateVideo(self, preview=True):
		if preview:
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
		self.outputVideoInformation()

	def outputVideoInformation(self):
		info = self.title + "\n\n"
		for i in range(len(self.data_boxes)):
			info += f"=== {self.data_boxes[i].data_string} ===\n"
			info += f"{self.data_boxes[i].prefix}\n{self.data_boxes[i].data_value}\n{self.data_boxes[i].suffix}\n{self.data_boxes[i].data_title}\n{self.data_boxes[i].icon_urls[0]}\n\n"
			for j in range(1, len(self.data_boxes[i].icon_urls)):
				info += f"{self.data_boxes[i].icon_urls[j]}\n"
			info += "\n=== ===\n\n"
		with open(os.path.join(self.out_path, "info.txt"), "w+") as f:
			f.write(info)