from fileparser import *
import argparse

def generateVideo(file):
    video = parseFile(file)
    video.generateVideo()

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate a data comparison video based on a given data file.")
    p.add_argument("-f", "--file", type=str, required=True, help="Path to file containing video information.")
    ags = p.parse_args()
    generateVideo(ags.file)