from base.the_graph import Graph


n = 6
edges = [(2,2), (2,1), (2,4), (1,3), (4,1), (3,5), (5,3), (4,0), (1,0), (3,4), (0,3), (2,4), (4,1)]

graph = Graph(n, edges)

first, second = graph.get_area_of_polys()
print(first, second)
print(graph.check_if_sums_up_to_square(first, second))

plot = graph.draw(edges=True, intersections=True, polygons=True, frame=True)
plot.show()

