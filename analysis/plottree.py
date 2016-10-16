from IPython.display import Image
import pydotplus

graph = pydotplus.graph_from_dot_file('tree.dot')
graph.write_pdf('tree.pdf')
