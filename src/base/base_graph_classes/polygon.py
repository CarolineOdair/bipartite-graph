from base.base_graph_classes.edge import Edge
from base.base_graph_classes.point import Point



class Poly():

    def __init__(self, n:int, *args):

        if all([not isinstance(arg, Point) for arg in args]):
            raise Exception(f"Polygon vertices must all be of class `Point`.")
        
        if len([*args]) < 3:
            print("small polygon")
        
        self.n = n
        self.verts = [*args]

        self.manage_edges_types(n)
    
    def __repr__(self):  
        return f"{self.verts}"
    
    def __eq__(self, poly_2):

        if set(self.verts) == set(poly_2.verts):
            return True 
        return False

    def __hash__(self):
        return hash(str(self))
    
    def __getitem__(self, i:int) -> Point:
        try:
            return self.verts[i]
        except:
            raise Exception(f"`i` must be int from 0 to {len(self.verts)-1}, now i is {type(i)} equal to {i}.")
        
    # def get_polygon_without_duplicated_points(self):
    #     new_verts = []
    #     # new_verts = [vert for vert in self.verts if vert not in new_verts] 
    #     return Poly(self.n, *new_verts)


    def manage_edges_types(self, n):

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
