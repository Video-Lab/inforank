from video import Video
import os
import argparse

def generateVideos(directory, preview):
    paths = []
    for f in os.listdir(directory):
        if os.path.isfile(os.path.join(directory,f)):
            paths.append(os.path.join(directory, f))
    print(paths)
    
    for p in paths:
        Video.fromFile(p).generateVideo(preview)



if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Create multiple videos from multiple files given a directory.")
    p.add_argument('-d', '--dir', type=str, required=True, help="Directory where files are located.")
    p.add_argument("-np", "--no-preview", required=False, action="store_true", help="Don't preview data boxes before generation.")
    ags = p.parse_args()
    generateVideos(os.path.abspath(ags.dir), not ags.no_preview)