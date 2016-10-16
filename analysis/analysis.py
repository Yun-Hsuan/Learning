import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn import tree
from IPython.display import Image
import pydotplus
from math import floor
from sklearn.utils import shuffle

def load_csv(fname, yNum, M, N):

    df = pd.read_csv(fname, index_col=0)
    df = shuffle(df)
    label = np.array(df.columns)
    index = np.array(df.index)
    X = np.array(df)
    Y = np.array(X[:, -1], dtype='float64')
    X = np.delete(X, -1, 1)

    print " ======== Start Transform String to float ======== "
    print " ..."

    tf = preprocessing.LabelEncoder()
    tx = X.reshape(-1)
    tf.fit(tx)
    tx = tf.transform(tx)
    tx = np.reshape(tx, X.shape)

    y_max  = np.amax(Y)
    y_min  = np.amin(Y)
    scaler = (y_max-y_min)/yNum

    yL = []
    #labelize Y
    for i in xrange(len(Y)):
        yL.append(int(floor((Y[i]-y_min)/scaler)))

    print " ..."
    print " ========  End Transform String to float  ======== "
    
    inputNum = len(X)
    trainNum = (inputNum/(N+M)) * M

    index_train = index[:trainNum]
    X_train     = tx[:trainNum]
    Y_train     = np.array(yL[:trainNum])

    index_test = index[trainNum:]
    X_test     = tx[trainNum:]
    Y_test     = np.array(yL[trainNum:])
    

    return [label, index_train, X_train, Y_train], \
           [label, index_test, X_test, Y_test], 


if __name__ == '__main__':	

    ifname = '../ggdata/ggdata_full.csv'
    classifierNum = 10
    record_N_important_variable = 200
    treeNum       = 50
    result_fp         = "result"
    important_para_fp = "important_para"

    print " ========== Start Loading the data Set ========== "
    print " ..."

    train, test = load_csv(ifname, classifierNum,4,1)

    print " ..."
    print " ==========  End Loading the data Set  ========== "



    print " ==== Start Training ..."
    print " ..."
    #clf = DecisionTreeClassifier(random_state=0)
    clf = RandomForestClassifier(n_estimators=treeNum)
    clf = clf.fit(train[2], train[3])
    print " ==== End Training ..."

    unorder_ipara = clf.feature_importances_

    #print np.amax(np.array(unorder_ipara))
    #print np.sum(np.array(unorder_ipara))
    
    order_ipara_idx = sorted(range(len(unorder_ipara)), key=lambda k: unorder_ipara[k], reverse=True)

    ofp = open(important_para_fp,"w")

    for i in xrange(record_N_important_variable):
        ofp.write(str(train[0][order_ipara_idx[i]])+","+str(round(unorder_ipara[order_ipara_idx[i]],10))+"\n")

    ofp.close()

    print "End ============"

    clf_err = 1.0 - clf.score(test[2], test[3])

    result =  clf.predict_proba(test[2])
    print result

    print "Error: " + str(clf_err) + "\n"

    fout = open(result_fp, 'w')
    cnt_i = 0
    for wafer in result:
        fout.write(str(test[1][cnt_i]) + ',' + str(np.argmax(wafer)) + ','+ str(test[3][cnt_i])+'\n')
        cnt_i += 1
    fout.write("Error: "+str(round(clf_err, 10)))
    
    #tree.export_graphviz(clf, out_file = 'tree.dot')
    #graph = pydotplus.graph_from_dot_file('tree.dot')
    #graph.write_pdf('tree.pdf')
    #Image(graph.create_png())
