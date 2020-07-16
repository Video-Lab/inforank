# Constants for general info, user-specfic global data, etc.
DEFAULTS = {'prefix': '', 'width': 1920, 'title': '', 'unit': '', 'unit_place': 'after', 'prefix': '', 'suffix': '', 'color': (21, 64, 16),
'bg_light_color': (217, 217, 217), 'bg_color': (46, 46, 46), 'gap_color': (46, 46, 46), 'music': '', 'data_image_type': 'file', 'data_image': './assets/none.png', 'out_path': './'}
FPS = 60 # Frames per second
CHANNEL_NAME = "InfoRank"
NUM_BOXES = 4 # "Number of boxes that can fit on the screen"
GAP_PERCENTAGE = 0.01 # % of video width taken up by a gap
DATA_BOX_PERCENTAGE = (1/NUM_BOXES)-((GAP_PERCENTAGE*(NUM_BOXES-1))/NUM_BOXES) #  % of width taken up by single data box
DATA_VALUE_PERCENTAGE = 0.50
DATA_TITLE_PERCENTAGE = 0.08
DATA_IMAGE_PERCENTAGE = 0.42
DATA_VALUE_PADDING_PERCENTAGE = 0.15*DATA_BOX_PERCENTAGE # % of WIDTH
DATA_IMAGE_PADDING_PERCENTAGE = 0.1 # Padding around data image box for actual image
FONT_REGULAR = "./assets/Mukta-ExtraLight.ttf"
FONT_BOLD = "./assets/Mukta-Bold.ttf"
TEXT_PERCENTAGE = 0.9 # % of width of any line taken up by text
TEXT_COLOR_THRESHOLD = 150 # When to start drawing black text instead of white text. 
DATA_VALUE_FONT_SECONDARY = 40
DATA_VALUE_FONT_MAIN = 120
TEXT_PADDING = 40 # Pixel padding between lines
DATA_TITLE_FONT = 55
IMAGE_PERCENTAGE = (0.9, 0.9) # % of data image box taken up by actual image on x and y axis
MIN_SIZE = (256, 256) # Minimum data image size
PPF = 1 # Number of pixels to shift per frame
FADE_TIME = 1 # Number of seconds to fade in
FADE_COLOR = (0,0,0) # Base color for fades
DEBUG = True # Print debug messages
WRITE_SETTINGS = {'codec': "libx264", 'bitrate': '5000k', 'ffmpeg_params': ['-crf', '18'], 'fps': FPS} # Video file settings for output.