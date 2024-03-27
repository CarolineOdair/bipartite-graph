from math import acos
from typing import Union, Tuple

from base.base_graph_classes.edge import Edge
from base.base_graph_classes.point import Point



def inner_prod(vector_1:Union[Edge, Point], vector_2:Union[Edge, Point]) -> float:
    '''
    Euclidean inner product. Takes two Edge or Point objects,
    return float. 
    '''
    validate_if_all_edge_or_point(vector_1, vector_2)

    vector_1 = vector_1.to_vector()
    vector_2 = vector_2.to_vector()

    return vector_1.x * vector_2.x + vector_1.y * vector_2.y


def cross_prod(vector_1:Union[Edge, Point], vector_2:Union[Edge, Point]) -> Tuple[int, int, float]:
    '''
    Cross product defined for the project about graph.

    Takes two Edge or Point objects ( 2 dimensional line segments 'edge = (x, y)' !), treats them as 'edge = (x, y, 0)' and
    returns tuple representing their cross product.        
    '''
    validate_if_all_edge_or_point(vector_1, vector_2)

    vector_1 = vector_1.to_vector()
    vector_2 = vector_2.to_vector()

    return (0, 0, vector_1.x * vector_2.y - vector_2.x * vector_1.y)


def angle_between_edges(vector_1:Union[Edge, Point], vector_2:Union[Edge, Point]) -> float:
    '''
    Using formula <a, b> = |a| * |b| * cos(phi)
    calculate phi value - angle between edges a and b.

    Takes two Edge or Point objects and returns float representing the angle from 0 to pi.
    '''

    validate_if_all_edge_or_point(vector_1, vector_2)

    vector_1 = vector_1.to_vector()
    vector_2 = vector_2.to_vector()

    cos_value = inner_prod(vector_1, vector_2) / (abs(vector_1) * abs(vector_2))  

    return acos(round(cos_value, 2))
    

def validate_if_all_edge_or_point(*args) -> None:
    if not all([isinstance(arg, Edge) or isinstance(arg, Point) for arg in args]):
        raise Exception(f"All given elements must be instance of the class Edge or Point.")
