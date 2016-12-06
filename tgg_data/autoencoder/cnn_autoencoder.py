import os
from keras.datasets import mnist
from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D
from keras.models import Model
import numpy as np


def load( fdc_rgb ):
    x = []
    image_files = os.listdir( fdc_rgb )
    for fp in image_files:
        x.append(np.load(fdc_rgb+fp))
    return x


train_dir  = "/home/yun-hsuan/GitRepo/tgg_data/plot_rgb512/"
#test_dir   = "/home/yun-hsuan/GitRepo/tgg_data/test_rgb512/"

_batch_size = 256
_epoch      = 200

x_train = load(train_dir)
x_test  = x_train[:]

row = len(x_train[0])
col = len(x_train[0][0])

x_train = np.array(x_train, dtype='float32') / 255.
x_test = np.array(x_test, dtype='float32') / 255.

input_img = Input(shape=(row, col, 1))

x = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(input_img)

x = MaxPooling2D((2, 2), border_mode='same')(x)

x = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(x)

x = MaxPooling2D((2, 2), border_mode='same')(x)

x = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(x)

encoded = MaxPooling2D((2, 2), border_mode='same')(x)

# at this point the representation is (8, 4, 4) i.e. 128-dimensional

x = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(encoded)

x = UpSampling2D((2, 2))(x)

x = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(x)

x = UpSampling2D((2, 2))(x)

x = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(x)

x = UpSampling2D((2, 2))(x)

decoded = Convolution2D(1, 3, 3, activation='sigmoid', border_mode='same')(x)

autoencoder = Model(input_img, decoded)

autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

autoencoder.summary()
#exit(0)

x_train = np.reshape(x_train, (len(x_train), row, col, 1))
x_test  = np.reshape(x_test,  (len(x_test), row, col, 1))
print x_train.shape
print x_test.shape
#exit(0)

from keras.callbacks import TensorBoard

autoencoder.fit(x_train, x_train,
        nb_epoch=_epoch,
        batch_size=_batch_size,
        shuffle=True,
        #validation_data=(x_test, x_test),
        callbacks=[TensorBoard(log_dir='/tmp/autoencoder')])

# serialize model to YAML
ae_model_yaml = autoencoder.to_yaml()
with open("ae_model.yaml", "w") as yaml_file:
    yaml_file.write(ae_model_yaml)
        # serialize weights to HDF5
autoencoder.save_weights("ae_model.h5")
print("Saved ae_model to disk")

#encoded_imgs = encoded.predict(x_test)
decoded_imgs = autoencoder.predict(x_test[:128])

# use Matplotlib (don't ask)
import matplotlib.pyplot as plt

n = 6       # how many digits we will display
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
