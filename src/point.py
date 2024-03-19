import numpy as np

class PointType:
    VERTEX = "vertex"
    INTERSECTION = "intersection"
    UNDEFINED = "undefined"

class Point():
    TYPE = PointType.UNDEFINED
    branches_points =[]

    def __init__(self, x:float, y:float):

        is_x_ok = isinstance(x, float) or isinstance(x, int)
        is_y_ok = isinstance(y, float) or isinstance(y, int)
        if not (is_x_ok and is_y_ok):
            raise Exception(f"`x` and `y` must be floats or int, now type of x is {type(x)} and type of y is {type(y)}")
        
        self.x = x
        self.y = y
        self.coords = (x, y)

    def __repr__(self):  
        return f"{self.coords}"
    
    def __add__(self, point_2) -> tuple:
        return (self.x + point_2.x, self.y + point_2.y)
    
    def __getitem__(self, i:int) -> float:
        if i == 0 or i == 1:
            return self.coords[i]
        raise Exception(f"`i` must be int equal to 0 or 1, now i is {type(i)} equal to {i}.")
    
    def __eq__(self, point_2):
        if self.coords == point_2.coords:
            return True 
        return False
    
    

class VertexPoint(Point):
    TYPE = PointType.VERTEX

class IntersectionPoint(Point):
    TYPE = PointType.INTERSECTION
