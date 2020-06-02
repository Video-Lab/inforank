from misc import *
from video import Video
from databox import DataBox

def parseFile(path):
	with open(path, 'r') as f:
		ef = enumerate(f)
		end_data_index = len(ef)-1
		begin_settings_index = 0
		for i, line in ef:
			if "||BEGIN_DATA||" in line:
				begin_data_index = i+1
				end_settings_index = i-1

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

		data_boxes = [DataBox(**data_settings, **row) for row in data]
		video = Video(**video_settings, data_boxes=data_boxes)
		
		return video