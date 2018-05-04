#!/usr/bin/env python3

import cv2
import os
import shutil
import random
import decimal

pokemon_names=[]

with open('original_151.txt') as names_file:
    line = names_file.readline()
    while line:
        pokemon_names.append(line.replace("\n", ""))
        line = names_file.readline()

bg_images = []
for file in ["backgrounds/%s.jpg" % ("%s" % i).zfill(2) for i in range(len(os.listdir("backgrounds/")))]:
    print(file)
    image = cv2.imread(file)
    if image is not None:
        bg_images.append(cv2.resize(image, (196, 196)))
    else:
        print("Error opening %s" % file)

if os.path.exists("dataset_augmented"):
    shutil.rmtree("dataset_augmented")
os.mkdir("dataset_augmented")

for pokemon_name in pokemon_names:
    n = 0
    if not os.path.exists('dataset_augmented/%s' % pokemon_name):
        os.mkdir('dataset_augmented/%s' % pokemon_name)

    for file in [f.format(pokemon_name) for f in ["dataset/{0}/{0}.png", "dataset/{0}/{0}_go.png"]]:
        image = cv2.imread(file, cv2.IMREAD_UNCHANGED)

        cv2.imwrite('dataset_augmented/%s/%s.png' % (pokemon_name, ("%s" % n).zfill(3)), image)
        n+=1
        if image is not None:
            for bg_img_idx in random.sample(range(0, len(bg_images) - 1), 4) + random.sample(range(0, len(bg_images) - 1), 4) + random.sample(range(0, len(bg_images) - 1), 4):
                pokemon_size = int(196 * decimal.Decimal(random.randrange(40, 95))/100)
                pokemon_x = random.randrange(0, 196 - pokemon_size)
                pokemon_y = random.randrange(0, 196 - pokemon_size)

                resized_pokemon = cv2.resize(image, (pokemon_size, pokemon_size))
                background_copy = cv2.resize(bg_images[bg_img_idx], (196, 196))

                # Corners of Pasted Image
                y1, y2 = pokemon_y, pokemon_y + pokemon_size
                x1, x2 = pokemon_x, pokemon_x + pokemon_size

                alpha_s = resized_pokemon[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s

                for channel in range(0, 3):
                    background_copy[y1:y2, x1:x2, channel] = (alpha_s * resized_pokemon[:, :, channel] +
                                                              alpha_l * background_copy[y1:y2, x1:x2, channel])


                cv2.imwrite('dataset_augmented/%s/%s.png' % (pokemon_name, ("%s" % n).zfill(3)), background_copy)
                n+=1
        else:
            print("Error opening %s" % file)