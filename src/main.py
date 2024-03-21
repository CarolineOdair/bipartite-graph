from the_graph import Graph

n = 6
edges = [(2,2), (2,1), (2,4), (4,1), (3,5), (1,0), (3,4), (0,3), (2,4), (4,1)]
# edges = [(2,2), (2,1), (2,4), (4,1), (3,5), (4,0), (1,0), (3,4), (0,3), (2,4), (4,1)]

graph = Graph(n, edges)

plot = graph.draw(edges=True, intersections=True, polygons=True, frame=True)
plot.show()

