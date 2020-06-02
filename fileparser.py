from misc import *
from video import Video
from databox import DataBox

def parseFile(path):

	errorCheckFile(path)
	begin_settings_index, end_settings_index, begin_data_index, end_data_index = getFileIndexes(path)

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


		print(settings.keys())

		for k in settings.keys():
			if settings[k] == '':
				settings[k] = DEFAULTS[k]



		settings['data_box_height'] = settings['height']
		settings['data_box_width'] = DataBox.calculateDataBoxWidth(settings['width']) # TODO

		data_settings = getPairsInList(settings, ['data_box_width', 'data_box_height', 'data_value', 'unit', 'unit_place', 'prefix', 'suffix', 'data_title', 'color', 'bg_light_color', 'bg_color'])
		video_settings = getPairsInList(settings, ['width', 'height', 'title', 'music'])

		data_boxes = [DataBox(**data_settings, **row) for row in data] # Convert data row strings to DataBox classes
		video = Video(**video_settings, data_boxes=data_boxes) # Unpack settings, convert to video class

		return video



def getFileIndexes(path):
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


def errorCheckFile(path):
	with open(path, 'r') as f:
		begin_settings_index, end_settings_index, begin_data_index, end_data_index = getFileIndexes(path)
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