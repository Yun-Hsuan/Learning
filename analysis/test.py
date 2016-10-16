from IPython.display import Image
import pydotplus
from sklearn.datasets import load_iris
from sklearn import tree

clf  = tree.DecisionTreeClassifier()
iris = load_iris()
clf = clf.fit(iris.data, iris.target)

dot_data = tree.export_graphviz(clf, out_file = None)
graph = pydotplus.graph_from_dot_data(dot_data)
Image(graph.create_png())

