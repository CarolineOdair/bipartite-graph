from typing import Tuple


class PointType:
    VERTEX = "vertex"
    INTERSECTION = "intersection"
    UNDEFINED = "undefined"



class Point():
    '''
    Point is represented by its coordinates.

    Point can be interpreted as vector.
    '''

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


    def __repr__(self) -> str:  
        return f"{self.coords}"
    

    def __add__(self, point_2) -> Tuple[float, float]:
        return (self.x + point_2.x, self.y + point_2.y)
    

    def __getitem__(self, i:int) -> float:
        if i == 0 or i == 1:
            return self.coords[i]
        raise Exception(f"`i` must be int equal to 0 or 1, now i is {type(i)} equal to {i}.")
    

    def __eq__(self, point_2) -> bool:
        if self.coords == point_2.coords:
            return True 
        return False
    

    def __neq__(self, point_2) -> bool:
        return not self == point_2
    

    def __abs__(self) -> float:
        '''
        Returns the length of self in as float.
        '''
        return (self.x**2 + self.y**2)**0.5
    

    def __hash__(self) -> int:
        return hash(str(self))
    

    def to_vector(self):
        return self
    
    

class VertexPoint(Point):
    TYPE = PointType.VERTEX


class IntersectionPoint(Point):
    TYPE = PointType.INTERSECTION
