import os
import numpy as np
from PIL import Image
from scipy.ndimage.interpolation import zoom
from scipy import misc
import matplotlib.pyplot as plt


root_dir = "/home/yun-hsuan/GitRepo/tgg_data/plot/test"
rgb_mat_dir = "../test_rgb512/"

for i in xrange(300):
    if i == 136:
        image_dir = root_dir# + str(i+1)
        image_files = os.listdir(image_dir)
        cnt = 1
        for fp in image_files:
            img = Image.open(image_dir+"/"+fp).convert("L")
            img_resize = img.resize((64, 64), Image.BILINEAR)
            arr = np.array(img_resize, dtype='float32')
            np.save(rgb_mat_dir+"image_"+str(i+1)+"_"+str(cnt), arr)
            cnt += 1
