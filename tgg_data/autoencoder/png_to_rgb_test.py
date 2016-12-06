import os
import numpy as np
from PIL import Image
from scipy.ndimage.interpolation import zoom
from scipy import misc


root_dir = "/home/yun-hsuan/GitRepo/tgg_data/plot/test"
rgb_mat_dir = "../test_rgb/"

for i in xrange(300):
    if i != 136 or i != :
        continue
    image_dir = root_dir# + str(i+1)
    image_files = os.listdir(image_dir)
    cnt = 1
    for fp in image_files:
        arr = []
        img = Image.open(image_dir+"/"+fp).convert("L")
        arr_buf = np.array(img, dtype='float32')
        for i in xrange(len(arr_buf)/20):
            row = []
            for j in xrange(len(arr_buf[i])/20 ):
                tmp = 0
                for k in xrange(20):
                    for l in xrange(20):
                        tmp += arr_buf[(20*i)+k][(20*j)+l]
                tmp = tmp / 400. / 255.
                row.append(tmp)
            arr.append(row)
        arr_save = np.array(arr, dtype= 'float32')
        np.save(rgb_mat_dir+"image_"+str(i+1)+"_"+str(cnt), arr_save)
        cnt += 1


