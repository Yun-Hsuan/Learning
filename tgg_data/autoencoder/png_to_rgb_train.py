import os
import numpy as np
from PIL import Image
from scipy.ndimage.interpolation import zoom
from scipy import misc


root_dir = "/home/yun-hsuan/GitRepo/tgg_data/plot/"
rgb_mat_dir = "../train_rgb/"

for L in xrange(300):
    if L == 136 or L == 257 or L == 23 or L == 14 or L == 180 or L == 49:
        image_dir = root_dir + str(L+1)
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
            np.save(rgb_mat_dir+"image_"+str(L+1)+"_"+str(cnt), arr_save)
            cnt += 1


