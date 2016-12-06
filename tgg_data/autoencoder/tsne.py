import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import NullFormatter

from sklearn.manifold import TSNE

import numpy as np
import scipy as sci


X = np.load("para.npy")

model = TSNE(n_components=2, random_state=0)
np.set_printoptions(suppress=True)
X = model.fit_transform(X)

xdata = []
ydata = []

for i in xrange(len(X)):
    xdata.append(X[i][0])
    ydata.append(X[i][1])


fig, ax = plt.subplots()
ax.plot(xdata, ydata, 'ro')

plt.show()
print X
