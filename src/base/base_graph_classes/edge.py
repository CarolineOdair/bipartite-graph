from base.base_graph_classes.point import Point



class EdgeType:
    OUTER = "outer"
    INNER = "inner"
    UNDEFINED = "undefined"
    POLYGONAL = "polygonal"



class Edge():
    '''
    Edge is represented by its end points.

    Edge can be interpreted as bound vector.
    '''

    TYPE = EdgeType.UNDEFINED
    line_coefs = None
    intersection_points = []


    def __init__(self, x:Point, y:Point):

        if not (isinstance(x, Point) and isinstance(y, Point)):
            raise Exception(f"`x` and `y` must be Points, now type of x is {type(x)} and type of y is {type(y)}")
        
        self.end_points = [x, y]


    def __repr__(self) -> str:
        return f"{self.end_points}"


    def __getitem__(self, i:int) -> Point:
        if i == 0 or i == 1:
            return self.end_points[i]
        raise Exception(f"`i` must be int equal to 0 or 1, now i is {type(i)} equal to {i}.")
    

    def __eq__(self, edge_2) -> bool:
        if self.end_points == edge_2.end_points:
            return True 
        return False
    

    def __neq__(self, point_2) -> bool:
        return not self == point_2
    
    
    def __abs__(self) -> float:
        '''
        Returns the length of self as float.
        '''
        vect = self.to_vector(self)

        return (vect.x**2 + vect.y**2)**0.5
    

    def __hash__(self) -> int:
        return hash(str(self))
    

    def to_vector(self) -> Point:
        '''
        Changes self (bound vector) to free vector (Point).

        Returns Point.
        '''

        return Point(self.end_points[1].x - self.end_points[0].x, self.end_points[1].y - self.end_points[0].y)
    

    def reversed_edge(self):
        '''
        Returns edge with endpoints switched (does not influence itself).

        Returns Edge.
        '''
        return Edge(self.end_points[1], self.end_points[0])
