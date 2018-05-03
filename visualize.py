from keras.models import load_model
from PIL import Image

model = load_model("poke_small_vgg.model")

first_layer = model.layers[0].get_weights()


for i in range(first_layer[0].shape[3]):
    Image.fromarray(first_layer[0][:,:,:,i], 'RGB').save('layer1/%s.png' % i)
