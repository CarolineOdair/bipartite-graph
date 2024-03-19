from the_graph import Graph
from point import Point
import matplotlib.pyplot as plt

n = 5
edges = [(1,3), (2,2), (1,0), (2,1), (4,1), (3,4), (2,4), (4,1)]

graph = Graph(n, edges)

plot = graph.draw(edges=True, intersections=True)
plot.show()
# graph.get_first_polygon()
