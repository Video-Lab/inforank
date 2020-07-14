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