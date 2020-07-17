# InfoRank
InfoRank is tool that generates data ranking videos based on user-inputted information.

![Preview of a finished video.](https://raw.githubusercontent.com/Video-Lab/inforank/master/preview.png)

## Data files
InfoRank runs on data entered into a specially-formatted text file, with information about the video and its contents. A typical data file looks as follows:

    width=1920
    height=1080
    title=
    unit=
    unit_place=after
    prefix=
    suffix=
    color=
    bg_light_color=
    bg_color=
    music=
    
    ||BEGIN_DATA||
    
    data_value=|data_title=|data_image_type=|data_image=
    data_value=|data_title=|data_image_type=|data_image=
    data_value=|data_title=|data_image_type=|data_image=

New lines are not parsed, so you can space the file however you want.

**Video Settings**

The first part of the file focuses on general video settings, including dimensions & formatting for the boxes on the video.

 - `prefix` refers to the text that appears before the main value on each box, while `suffix` sets the text that appears after the main value. If `RANK_DATA_BOXES` is entered into either the prefix or the suffix, the position of that box will be used as a value, starting from the highest number and moving towards 1.
 - The `unit` is a phrase or character that can be placed either before or after the main value, specified by the `unit_place` setting.
 - As for colors, the `color` property refers to the color of the main data section, `bg_light_color` refers to the title background color, and `bg_color` refers to the background color of the image section. The data border and text colors are automatically calculated based on the colors above.
 - The `music` setting stores the path to an audio file that can be used as background music for the video. If you don't want music, leave this setting blank.

**Data Settings**

Each box on the video is represented by a single line after the `||BEGIN_DATA||` marker, which indicates the start of the data settings. The settings for a single data box looks as follows:

    data_value=|data_title=|data_image_type=|data_image=
   
Each setting is separated by a `|` character. It is important not to modify the names of the settings themselves, but you can modify their order.

The use of each setting is described below:

 - `data_value` stores the main value of each data box. For example, in the preview image, this would be the large number indicating the rank of the fruit. This can be any type of text, including words and phrases.
 - `data_title` stores the title which appears under the data and over the image. Just like the data value, this can be any type of text.
 - `data_image_type` stores the type of image used in the box. This can either be `file` or `icon`. Note that this value will influence the value used in the next setting.
 - `data_image` is the actual text used to retrieve the image. If the image type is `icon`, you can enter a list of comma-separated search terms that will be used to find the icon. On the other hand, if the image type if `file`, then you can enter a path to a custom image to be used.

**Default Settings**
If you leave a certain video setting blank, it will resort to a default value that can be found in the `settings.py` file (more on that later).

## Create blank data file
The `generatefile.py` script can be used to create a data file with a set of parameters.

To learn more about the script parameters, type this in your console:

    python generatefile.py -h

Which will list the parameters and their descriptions.

Here is an example of the script in use:

    python generatefile.py --width 1280 --height 720 --title "Salary Comparison" --prefix Salary --num-rows 10 --path ./test.txt
   
This command will generate a file called `test.txt` with 10 data box rows, and the settings specified in the command filled in. If a parameter is not included (besides the required path to file), it will show up as blank on the file.

Running the script without any parameters will generate a data file with the width and height set to 1920 and 1080, and 40 blank data box rows.

## Application settings
The `settings.py` file contains general settings about the application that work regardless of the data file. Each constant has a description of what it does. This can be used to alter aspects of the video, including spacing between boxes, video framerate, and default values.

## Important: Using Icons
This application uses the IconFinder API to find and implement icons into the video. To use icons, you have to create your own API application with IconFinder, and then create an environment variable in your command line with the API secret.

**Getting your API secret**

You can get started at [https://www.iconfinder.com/api-solution](https://www.iconfinder.com/api-solution),  where you can create an account and an application.

**Creating an environment variable**

Once you have your API key, you can create an environment variable called `ICONFINDER_API_KEY` which will allow you to use icons with the application. The following commands will allow you to set an environment variable:

**Linux, macOS**

    export ICONFINDER_API_KEY="key-goes-here"

**Windows (PowerShell)**

    $env:ICONFINDER_API_KEY="key-goes-here"

**Windows (CMD)**

    set ICONFINDER_API_KEY=key-goes-here

(note the absence of quotation marks in the Command Prompt command).

## Create video

**Create single video**
To create a single video, run the `inforank.py` script, passing the path to your data file as a parameter. Here is an example of a call to the script:

    python inforank.py --file "./data_file.txt"

This will create a single video and output it to `./inforank/<title>/video.mp4` (Unless you change the filetype or other write settings in the `settings.py` file).

**Create videos in batch**

To create multiple videos, run the `dir2inforank.py` script & pass it the path to a directory containing multiple data files. This will create videos based on all the data files in the directory. Below is an example of the script in action:

    python dir2inforank.py --dir './data_files/'

This will output videos in the same manner as single videos, with multiple directories under the `./inforank` directory.

## Previewing data boxes
By default, the tool will allow you to preview data boxes before they are rendered into the video. An image is brought up in an image viewer, and the command line will prompt you to make changes to the data box if needed.

If the data box uses an icon, a prompt will be brought up to change the icon based on the search term you provided. This is brought up before you are given the opportunity to change the data box settings. Once you approve the icon, you can move on to changing the settings of the data box.

You will be given a prompt to enter a comma-separated list of the properties you want to change. From there, a new preview will be brought up, and you will be allowed to continually change the data box until you approve it.

Although it is not recommended, you can bypass the preview stage by passing the `-np` or `--no-preview` flag to both the `inforank.py` and `dir2inforank.py` files.

## Finding your videos
Once your video is exported, you can find it under a directory in the `./inforank` directory. The directory name is based on the video title, with spaces replaced by underscores. The following list explains the contents of this directory:

 - The `video.mp4` file is the actual video file. The file extension can be altered from the `settings.py` file.
 - The `video_image.png` is the full image used to generate the video. This is a high-definition file that contains the full width of the video without any cut-offs or scrolling.
 - The `info.txt` file contains general information about the video and the data boxes used, including a "pretty" title that can be used when uploading YouTube videos, and the information used for each data box. This includes the URL or path to images used and extra URLs returned from queries to the IconFinder API if icons are used.
 - The `data_boxes` directory contains individual images of each data box. The files are named based on the title of the video and a number indicating their position, starting from 0 and moving up to the total number of data boxes.