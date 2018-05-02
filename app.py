from flask import request, Flask
import cv2
from flask import Flask
import os
from keras.models import load_model
import pickle
from keras.preprocessing.image import img_to_array
import numpy as np

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

image_dir=dir('images/')

lb = pickle.loads(open("pokemon.pickle", "rb").read())

app = Flask(__name__)
@app.route('/pokedex', methods=['POST'])
def classify_pokemon():
    file = request.files['file']

    ext=file.filename.split('.')[-1]
    filename=str(len(os.listdir('images'))) + "." + ext
    file.save(os.path.join('images', filename))

    # load the image
    image = cv2.imread("images/%s" % filename)

    # pre-process the image for classification
    image = cv2.resize(image, (96, 96))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    print("[INFO] loading model...")
    model = load_model("poke_small_vgg.model")

    print("[INFO] classifying image...")
    proba = model.predict(image)[0]
    idx = np.argmax(proba)
    label = lb.classes_[idx]

    print("[INFO] %s %s" % (label, proba[idx]))


    return '{"label": "%s", "probability": %s}' % (label, proba[idx])

app.run()