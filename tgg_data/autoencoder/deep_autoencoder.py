import os
from keras.datasets import mnist
import numpy as np
from keras.layers import Input, Dense
from keras.models import Model
from keras import regularizers
from keras.layers import Dropout


def load( fdc_rgb ):
    x = []
    image_files = os.listdir( fdc_rgb )
    for fp in image_files:
        x.append(np.load(fdc_rgb+fp))
    return x


train_dir  = "/home/yun-hsuan/GitRepo/tgg_data/plot_rgb512/"
#test_dir   = "/home/yun-hsuan/GitRepo/tgg_data/plot_rgb512/"

_batch_size = 128
_epoch      = 400

x_train = load(train_dir)
x_test  = x_train[:]

x_train = np.array(x_train, dtype='float32') / 255.
x_test = np.array(x_test, dtype='float32')/ 255.

row = len(x_train[0])
col = len(x_train[0][0])

img_len = row * col

print img_len

encoding_dim = 256 # compression of factor 24.5

input_img = Input(shape=(img_len,))

encoded = Dense(1024, activation='relu')(input_img)
encoded = Dense(1024, activation='relu')(encoded)
encoded = Dense(512, activation='relu')(encoded)
encoded = Dense(512, activation='relu')(encoded)
encoded = Dense(encoding_dim, activation='relu')(encoded)

decoded = Dense(512, activation='relu')(encoded)
decoded = Dense(512, activation='relu')(decoded)
decoded = Dense(1024, activation='relu')(decoded)
decoded = Dense(1024, activation='relu')(decoded)
decoded = Dense(img_len, activation='sigmoid')(decoded)


autoencoder = Model(input=input_img, output=decoded)

# Create the encoder Model
encoder = Model(input=input_img, output=encoded)
encoded_input = Input(shape=(encoding_dim,))

# Create the decoder Model
decoded1 = autoencoder.layers[-5](encoded_input)
decoded1 = autoencoder.layers[-4](decoded1)
decoded1 = autoencoder.layers[-3](decoded1)
decoded1 = autoencoder.layers[-2](decoded1)
decoded1 = autoencoder.layers[-1](decoded1)
decoder  = Model(input=encoded_input, output=decoded1)

autoencoder.load_weights('ae_model.h5')
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

decoder.summary()
autoencoder.summary()
encoder.summary()

#x_train = x_train.astype('float32') / 255.
#x_test = x_test.astype('float32') / 255.
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
print x_train.shape
print x_test.shape
#exit(0)

autoencoder.fit(x_train, x_train,
        nb_epoch=_epoch,
        batch_size=_batch_size,
        shuffle=True)
        #,validation_data=(x_test, x_test))

# encode and decode some digits
# note that we take them from the *test* set
encoded_imgs = encoder.predict(x_train[1000:1256])
np.save("para", encoded_imgs)
decoded_imgs = decoder.predict(encoded_imgs)

# serialize model to YAML
ae_model_yaml = autoencoder.to_yaml()
with open("ae_model1.yaml", "w") as yaml_file:
    yaml_file.write(ae_model_yaml)
        # serialize weights to HDF5
autoencoder.save_weights("ae_model1.h5")
print("Saved ae_model to disk")

# use Matplotlib (don't ask)
import matplotlib.pyplot as plt

n = 10       # how many digits we will display
plt.figure(figsize=(20, 4))
for i in range(n):
    # display original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i].reshape(row, col))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # display reconstruction
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_imgs[i].reshape(row, col))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()
