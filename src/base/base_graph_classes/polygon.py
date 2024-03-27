from base.base_graph_classes.edge import Edge
from base.base_graph_classes.point import Point



class Poly():
    '''
    Polygon is represented by its vertices.
    
    Polygon exists inside the graph, so some info about the Poly is actually info about the graph,
    i.e. an edge of the Poly can be inner or outer edge (of the graph).  
    '''
        
    def __init__(self, n:int, *args):

        if all([not isinstance(arg, Point) for arg in args]):
            raise Exception(f"Polygon vertices must all be of class `Point`.")
        
        if len([*args]) < 3:
            print("small polygon")
        
        self.n = n
        self.verts = [*args]

        self.manage_edges_types(n)
    

    def __repr__(self) -> str:  
        return f"{self.verts}"
    

    def __eq__(self, poly_2) -> bool:

        if set(self.verts) == set(poly_2.verts):
            return True 
        return False


    def __hash__(self) -> int:
        return hash(str(self))
    

    def __getitem__(self, i:int) -> Point:
        try:
            return self.verts[i]
        except:
            raise Exception(f"`i` must be int from 0 to {len(self.verts)-1}, now i is {type(i)} equal to {i}.")


    def manage_edges_types(self, n:int) -> None:
        '''
        Adds edges to polygon. Divides edges to inner and outer of the graph.

        Takes n:int - number of edges in the graph.

        Returns None.
        '''

        up_edge_points = [Point(0, n-1), Point(n-1, n-1)]
        down_edge_points = [Point(0, 0), Point(n-1,0)]

        self.inner_edges = []
        self.outer_edges = []
        self.is_up_edge = False
        self.is_down_edge = False

        now_verts = self.verts.copy()
        now_verts += [self.verts[0]]

        for i in range(1, len(now_verts)):
            vert_1 = now_verts[i-1]
            vert_2 = now_verts[i]

            edge = Edge(vert_1, vert_2)

            if vert_1 in down_edge_points and vert_2 in down_edge_points:
                self.if_up_edge = True
            elif vert_1 in up_edge_points and vert_2 in up_edge_points:
                self.if_up_edge = True
            elif vert_1.x == vert_2.x:
                self.outer_edges.append(edge)
            else:
                self.inner_edges.append(edge)


    def get_area(self) -> float:
        '''
        Calculates area of the polygon using shoelace formula:
        https://en.wikipedia.org/wiki/Shoelace_formula

        Returns the area:float.
        '''

        area_times_2 = 0

        num_of_verts = len(self.verts)
        for i in range(num_of_verts):
            j = i + 1

            if i == num_of_verts-1:
                j = 0

            x_1 = self[i].x
            y_1 = self[i].y
            x_2 = self[j].x
            y_2 = self[j].y

            area_times_2 += x_1*y_2 - x_2*y_1

        return abs(area_times_2)/2
