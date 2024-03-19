import numpy as np
from point import Point

class EdgeType:
    OUTER = "outer"
    INNER = "inner"
    UNDEFINED = "undefined"
    POLYGONAL = "polygonal"

class Edge():
    TYPE = EdgeType.UNDEFINED
    line_coefs = None
    intersection_points = []

    def __init__(self, x:Point, y:Point):

        if not (isinstance(x, Point) and isinstance(y, Point)):
            raise Exception(f"`x` and `y` must be Points, now type of x is {type(x)} and type of y is {type(y)}")
        
        self.end_points = [x, y]

    def __repr__(self):  
        return f"{self.end_points}"


    def __getitem__(self, i:int) -> Point:
        if i == 0 or i == 1:
            return self.end_points[i]
        raise Exception(f"`i` must be int equal to 0 or 1, now i is {type(i)} equal to {i}.")
    
    def __eq__(self, edge):
        if self.end_points == edge.end_points:
            return True 
        return False
    
class OuterEdge(Edge):
    TYPE = EdgeType.OUTER

class InnerEdge(Edge):
    TYPE = EdgeType.INNER

class PolygonalEdge(InnerEdge):
    TYPE = EdgeType.POLYGONAL