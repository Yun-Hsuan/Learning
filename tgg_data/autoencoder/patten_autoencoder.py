import os
from keras.datasets import mnist
import numpy as np
from keras.layers import Input, Dense
from keras.models import Model



def load( fdc_rgb ):
    x = []
    image_files = os.listdir( fdc_rgb )
    for fp in image_files:
        x.append(np.load(fdc_rgb+fp))
    return x


train_dir  = "/home/yun-hsuan/GitRepo/tgg_data/plot_rgb512/"
test_dir   = "/home/yun-hsuan/GitRepo/tgg_data/plot_rgb512/"

x_train = load(train_dir)
x_test  = load(test_dir)

x_train = np.array(x_train, dtype='float32') / 255.
x_test = np.array(x_test, dtype='float32')/ 255.

row = len(x_train[0])
col = len(x_train[0][0])

img_len = row * col

encoding_dim = 32 # compression of factor 24.5

input_img = Input(shape=(img_len,))

encoded = Dense(encoding_dim, activation='relu')(input_img)

decoded = Dense(img_len, activation='sigmoid')(encoded)

autoencoder = Model(input=input_img, output=decoded)

encoder = Model(input=input_img, output=encoded)

# create a placeholder for an encoded (32-dimensional) input
encoded_input = Input(shape=(encoding_dim,))

# retrieve the last layer of the autoencoder model
decoder_layer = autoencoder.layers[-1]

# create the decoder model
decoder = Model(input=encoded_input, output=decoder_layer(encoded_input))

autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

#(x_train, _), (x_test, _) = mnist.load_data()

#x_train = x_train.astype('float32') / 255.
#x_test = x_test.astype('float32') / 255.
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
print x_train.shape
print x_test.shape
#exit(0)


autoencoder.fit(x_train, x_train,
        nb_epoch=300,
        batch_size=34,
        shuffle=True,
        validation_data=(x_test, x_test))

# encode and decode some digits
# note that we take them from the *test* set
encoded_imgs = encoder.predict(x_train)
np.save("para", encoded_imgs)
#print encoded_imgs
#exit(0)
decoded_imgs = decoder.predict(encoded_imgs)


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
