import os
import numpy as np
from PIL import Image
from scipy.ndimage.interpolation import zoom
from scipy import misc


root_dir = "/home/yun-hsuan/GitRepo/tgg_data/plot/"
rgb_mat_dir = "../train_rgb512/"

for L in xrange(300):
    if L == 136 or L == 257 or L == 23 or L == 14 or L == 180 or L == 49:
        image_dir = root_dir + str(L+1)
        image_files = os.listdir(image_dir)
        cnt = 1
        for fp in image_files:
            img = Image.open(image_dir+"/"+fp).convert("L")
            img_resize = img.resize((64, 64), Image.BILINEAR)
            arr = np.array(img_resize, dtype='float32')
            np.save(rgb_mat_dir+"image_"+str(L+1)+"_"+str(cnt), arr)
            cnt += 1

