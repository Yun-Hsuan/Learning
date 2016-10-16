from sklearn.datasets import load_iris
from sklearn import tree
import os
import pydotplus
#from IPython.display import Image

important_para = [2, 1, 4, 5, 3]

order_ipara = sorted(range(len(important_para)), key=lambda k: important_para[k], reverse=True)

print order_ipara

exit()

clf  = tree.DecisionTreeClassifier()
iris = load_iris()
clf = clf.fit(iris.data, iris.target)

with open("iris.dot", "w") as f:
    f = tree.export_graphviz(clf, out_file=f)

#os.unlink('iris.dot')
tree.export_graphviz(clf, out_file = 'QQ.dot')
graph = pydotplus.graph_from_dot_file('iris.dot')
graph.write_pdf('iris.pdf')

