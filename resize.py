#!/usr/bin/env python3

from argparse import ArgumentParser
import os
import cv2

ap=ArgumentParser()
ap.add_argument("-s", "--size", required=True, help="size in pixels for output images")
ap.add_argument("-d", "--directory", required=True, help="directory of images to resize")
ap.add_argument("-o", "--out", required=True, help="directory of images to resize")
args = vars(ap.parse_args())

directory=args["directory"]
if directory.endswith("/"):
    directory = directory[:-1]
output_dir=args["out"]
size=int(args["size"])


files=os.listdir(directory)

def is_image(filename):
    for ext in ['.png', '.jpeg', '.jpg']:
        if filename.lower().endswith(ext):
            return True
    return False

print("Resizing %s images" % len(files))
for file in files:
    if not is_image(file):
        continue
    try:
        image = cv2.imread(directory + "/" + file)
        resized_image = cv2.resize(image, (size, size))
        cv2.imwrite(output_dir + "/" + file, resized_image)
    except Exception as e:
        print("Error writing %s" % file)