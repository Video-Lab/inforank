from fileparser import *
import argparse

def generateVideo(file, preview):
    video = parseFile(file)
    video.generateVideo(preview)

if __name__ == "__main__":

    p = argparse.ArgumentParser(description="Generate a data comparison video based on a given data file.")
    p.add_argument("-f", "--file", type=str, required=True, help="Path to file containing video information.")
    p.add_argument("-np", "--no-preview", required=False, action="store_true", help="Don't preview data boxes before generation.")
    ags = p.parse_args()
    generateVideo(ags.file, preview=not ags.no_preview)