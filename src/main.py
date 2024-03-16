from the_graph import Graph

n = 3
edges = [(1,2), (1,0), (0,2), (2,1)]

graph = Graph(n, edges)

plot = graph.draw(edges=True, intersections=True)
plot.show()
