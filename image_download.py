#!/usr/bin/env python3
import requests
from argparse import ArgumentParser
import os
import cv2


def search_images(query, offset, count, key):
    response = requests.get(
        SEARCH_URL,
        headers={"Ocp-Apim-Subscription-Key": subscription_key},
        params={"q": query, "offset": offset, "count": count},
        verify=False
    )
    response.raise_for_status()
    return response.json(), response.json()["totalEstimatedMatches"]


# subscription_key = ""
ap = ArgumentParser()
ap.add_argument("-q", "--query", required=True, help="search term for bing image api")
ap.add_argument("-o", "--out", required=True, help="path to output directory for results")
ap.add_argument("-m", "--max", required=True, help="maxiumum number of images")
ap.add_argument("-k", "--key", required=True, help="bing search api key")
args = vars(ap.parse_args())

# Load Arguments
search_term = args["query"]
output_dir = args["out"]
subscription_key = args["key"]

# Constant Options
GROUP_SIZE = 50
SEARCH_URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

# Initial Search
print("Searching for images related to '%s'" % search_term)
_, num_results = search_images(search_term, 0, GROUP_SIZE, subscription_key)

print("Found %s images" % num_results)

total_num = min(num_results, int(args["max"]))
n = 0
for i in range(0, total_num, GROUP_SIZE):
    print("Getting images %s-%s of %s" % (i, i + GROUP_SIZE, total_num))
    search_results, _ = search_images(search_term, i, GROUP_SIZE, subscription_key)
    print("Saving images %s-%s of %s" % (i, i + GROUP_SIZE, total_num))
    for val in search_results["value"]:
        try:
            # Download Image
            image_response = requests.get(val["contentUrl"], timeout=10, verify=False)

            # Build file path
            extension = val["contentUrl"][val["contentUrl"].rfind("."):]
            path = os.path.sep.join([output_dir, "%s%s" % (str(n).zfill(8), extension)])

            # Save Image to File
            file = open(path, "wb")
            file.write(image_response.content)
            file.close()

            # Test image is readable, if not delete it
            image = cv2.imread(path)
            if image is None:
                os.remove(path)
                continue
            n += 1
        except Exception as e:
            print(e)
