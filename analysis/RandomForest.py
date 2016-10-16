from sklearn.ensemble import RandomForestClassifier
from itertools import izip
import numpy as np

input_feature = '/tmp2/r03222055/glove.train'
input_choices = '/tmp2/r03222055/glove_choices.train'
input_index   = '/tmp2/r03222055/answer_index'

predict_feature = '/tmp2/r03222055/glove.test'
predict_choices = '/tmp2/r03222055/glove_choices.test'

X = []
Y = []

f_fea = open(input_feature)
f_ch  = open(input_choices)
f_idx = open(input_index)

p_fea = open(predict_feature)
p_ch  = open(predict_choices)

print "handle train data"

for fea, idx in izip(f_fea, f_idx):
    fv = [ float(v) for v in fea.split() ]
    for i in range(5):
        ans = f_ch.readline()
        ch  = [ float(v) for v in ans.split() ]
        if i == int(idx):
            X.append(np.concatenate((fv, ch)))
            Y.append(1)
        else:
            X.append(np.concatenate((fv, ch)))
            Y.append(0)


f_fea.close()
f_ch.close()
f_idx.close()

print 'start training'

clf = RandomForestClassifier(n_estimators=50)
clf = clf.fit(X, Y)

print 'training finished'

PX = []
for fea in p_fea:
    fv = [float(v) for v in fea.split() ]
    for i in range(5):
        ans = p_ch.readline()
        ch = [ float(v) for v in ans.split() ]
        PX.append(np.concatenate((fv, ch)))

p_fea.close()
p_ch.close()

print 'start predict'

result =  clf.predict_log_proba(PX)

fout = open('/tmp2/r03222055/result', 'w')
for (a,b) in result:
    fout.write(str(a) + ' ' + str(b) + '\n')

fout.close()



















