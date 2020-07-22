import argparse
from os import path as os_path

def generateInfoRankFile(dict_args):
	path = dict_args['path']
	if os_path.exists(path):
		raise ValueError("Path " + path + " already exists.")
	else:
		with open(path, 'w+') as f:
			for k,v in dict_args.items():
				if k not in ['num_rows', 'path']:
					f.write(f"{k}={v}\n") # Write all settings excluding extras from argparse
			f.write("||BEGIN_DATA||\n")

			data_rows = "data_value=|data_title=|data_image_type=|data_image=\n"*dict_args['num_rows']
			data_rows = data_rows[:len(data_rows)-1]
			f.write(data_rows)


if __name__ == "__main__":
	p = argparse.ArgumentParser("Generate an InfoRank Video file based on given arguments.")
	p.add_argument('-w', '--width', default=1920, type=int, help="Width of video.")
	p.add_argument('-ht', '--height', default=1080, type=int, help="Height of video.")
	p.add_argument('-t', '--title', default="", type=str, help="Raw title of video.")
	p.add_argument('-u', '--unit', default="", type=str, help="Unit to use in data values.")
	p.add_argument('-up', '--unit-place', default="after", type=str, help="Where to place the unit relative to the value.")
	p.add_argument('-px', '--prefix', default="", type=str, help="Text before the value.")
	p.add_argument('-sx', '--suffix', default="", type=str, help="Text after the value.")
	p.add_argument('-c', '--color', default="", type=str, help="Background color for value in data box.")
	p.add_argument('-bl', '--bg-light-color', default="", type=str, help="Background color for title strip.")
	p.add_argument('-bc', '--bg-color', default="", type=str, help="Background color for image box.")
	p.add_argument('-m', '--music', default="", type=str, help="Music for video.")
	p.add_argument('-gc', '--gap-color', default="", type=str, help="Color to use for gaps between boxes.")
	p.add_argument('-p', '--out-path', type=str, required=True, help="Path to write file")
	p.add_argument('-n', '--num-rows', default=50, type=int, help="Number of data rows to add.")

	args = vars(p.parse_args())
	generateInfoRankFile(args)