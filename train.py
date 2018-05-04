#!/usr/bin/env python3

# set the matplotlib backend so figures can be saved in the background
import matplotlib

matplotlib.use("Agg")

# import the necessary packages
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.preprocessing.image import img_to_array
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from models.smaller_vggnet import SmallerVGGNet
import matplotlib.pyplot as plt
from imutils import paths
import numpy as np
import argparse
import random
import pickle
import cv2
import os
from models.resnet import ResnetBuilder

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
                help="path to input dataset (i.e., directory of images)")
ap.add_argument("-m", "--model", required=True,
                help="path to output model")

ap.add_argument("-t", "--type", required=True,
                help="'resnet' or 'vggnet'")

ap.add_argument("-l", "--labelbin", required=True,
                help="path to output label binarizer")
ap.add_argument("-p", "--plot", type=str, default="plot.png",
                help="path to output accuracy/loss plot")
args = vars(ap.parse_args())


# initialize the number of epochs to train for, initial learning rate,
# batch size, and image dimensions
EPOCHS = 100
INITIAL_LEARNING_RATE = 1e-3
BATCH_SIZE = 32
IMAGE_DIMS = (96, 96, 3)

# initialize the data and labels
data = []
labels = []

# grab the image paths and randomly shuffle them
print("loading images...")
imagePaths = sorted(list(paths.list_images(args["dataset"])))
random.seed(42)
random.shuffle(imagePaths)

for imagePath in imagePaths:
    # load the image, pre-process it, and store it in the data list
    image = cv2.imread(imagePath)
    h, w, _ = image.shape
    if h != 96 or w != 96:
        image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
    image = img_to_array(image)
    data.append(image)

    # extract the class label from the image path and update the
    # labels list
    label = imagePath.split(os.path.sep)[-2]
    labels.append(label)

# Make Data into a nd_array with pixel intensities between 0 and 1
data = np.array(data, dtype="float") / 255.0

# Binarize Labels
labels = np.array(labels)
lb = LabelBinarizer()
labels = lb.fit_transform(labels)

# partition the data into training and testing splits using 80% of
# the data for training and the remaining 20% for testing
(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.2, random_state=42)

# construct the image generator for data augmentation
data_augmenter = ImageDataGenerator(rotation_range=25, width_shift_range=0.1,
                                    height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                                    horizontal_flip=True, fill_mode="nearest")

print("compiling model...")

model = None
model_type = args['type']
if model_type == 'vggnet':
    model = SmallerVGGNet.build(width=IMAGE_DIMS[1], height=IMAGE_DIMS[0],
                                depth=IMAGE_DIMS[2], classes=len(lb.classes_))
elif model_type == 'resnet':
    model = ResnetBuilder.build_resnet_34(input_shape=(IMAGE_DIMS[1], IMAGE_DIMS[2], IMAGE_DIMS[0]),
                                num_outputs=len(lb.classes_))
else:
    print('Unknown model type %s' % model_type)
    exit(1)

opt = Adam(lr=INITIAL_LEARNING_RATE, decay=INITIAL_LEARNING_RATE / EPOCHS)
model.compile(loss="categorical_crossentropy", optimizer=opt,
              metrics=["accuracy"])

# train the network
print("training network...")
H = model.fit_generator(
    data_augmenter.flow(trainX, trainY, batch_size=BATCH_SIZE),
    validation_data=(testX, testY),
    steps_per_epoch=len(trainX) // BATCH_SIZE,
    epochs=EPOCHS, verbose=1)

# save the model to disk
print("serializing network...")
model.save(args["model"])

# save the label binarizer to disk
print("serializing label binarizer...")
f = open(args["labelbin"], "wb")
f.write(pickle.dumps(lb))
f.close()

# plot the training loss and accuracy
plt.style.use("ggplot")
plt.figure()
N = EPOCHS
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="upper left")
plt.savefig(args["plot"])
