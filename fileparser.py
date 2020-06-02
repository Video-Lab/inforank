from misc import *
from video import Video
from databox import DataBox

def parseFile(path):
	
	errorCheckFile(path)
	begin_settings_index, end_settings_index, begin_data_index, end_data_index = getFileIndexes(path)

	with open(path, 'r') as f:
		settings_rows = ef[begin_settings_index:end_settings_index+1]
		data_rows = ef[begin_data_index:end_data_index+1]

		settings = {setting[0]: setting[1] for setting in [setting_string[1].split('=') for setting_string in settings_rows]} # Parse into dict of key-value pairs, 1 line = 1 pair
		data = [{data_setting[0]: data_setting[1] for data_setting in row[1].split('|')} for row in data_rows] # Same for data, but 1 line = 1 dict


		for d in settings, data: # Replace blank values with defaults from misc.py for settings, data
			for k in d.keys():
				if d[k] == ''
				d[k] = DEFAULTS[k]

		settings['data_box_height'] = settings['height']
		settings['data_box_width'] = DataBox.calculateDataBoxWidth(width) # TODO

		data_settings = getPairsInList(settings, ['data_box_width', 'data_box_height', 'value', 'unit', 'unit_place', 'prefix', 'suffix', 'title', 'color', 'bg_light_color', 'bg_color'])
		video_settings = getPairsInList(settings, ['width', 'height', 'title', 'music'])

		data_boxes = [DataBox(**data_settings, **row) for row in data] # Convert data row strings to DataBox classes
		video = Video(**video_settings, data_boxes=data_boxes) # Unpack settings, convert to video class

		return video



def getFileIndexes(path):
	with open(path, 'r') as f:
		ef = enumerate(f)
		end_data_index = len(ef)-1
		begin_settings_index = 0
		for i, line in ef:
			if "||BEGIN_DATA||" in line:
				begin_data_index = i+1
				end_settings_index = i-1
	return [begin_settings_index, end_settings_index, begin_data_index, end_data_index]


def errorCheckFile(path):
	with open(path, 'r') as f:
		begin_settings_index, end_settings_index, begin_data_index, end_data_index = getFileIndexes(path)
		ef = enumerate(f)
		for i,line in ef[begin_settings_index:end_settings_index+1]:
			if "=" not in line or len(line.split("=")) > 2:
				raise ValueError("Error in file at " + path + " at line " + i)

		for i,line in ef[begin_data_index:end_data_index+1]:
			row = line.split("|")
			if len(row) > 4:
				raise ValueError("Error in file at " + path + " at line " + i)
			else:
				for val in row:
					if "=" not in line or len(line.split("=")) > 2:
						raise ValueError("Error in file at " + path + " at line " + i)
	return