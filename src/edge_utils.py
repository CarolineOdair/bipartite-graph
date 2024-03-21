from edge import Edge
from math import acos

def inner_prod(edge_1:Edge, edge_2:Edge) -> float:
    '''
    Euclidean inner product. Takes two Egde objects,
    return float. 
    '''
    # validate_if_all_edge(edge_1, edge_2)

    edge_1 = edge_1.to_vector()
    edge_2 = edge_2.to_vector()

    return edge_1.x * edge_2.x + edge_1.y * edge_2.y

def cross_prod(edge_1:Edge, edge_2:Edge) -> tuple:
    '''
    Cross product defined for the project about graph.

    Takes two Edge objects ( 2 dimensional line segments 'edge = (x, y)' !), treats them as 'edge = (x, y, 0)' and
    returns tuple representing their cross product.        
    '''
    validate_if_all_edge(edge_1, edge_2)

    edge_1 = edge_1.to_vector()
    edge_2 = edge_2.to_vector()

    return (0, 0, edge_1.x * edge_2.y - edge_2.x * edge_1.y)

def angle_between_edges(edge_1:Edge, edge_2:Edge) -> float:
    '''
    Using formula <a, b> = |a| * |b| * cos(phi)
    calculate phi value - angle between edges a and b.

    Takes two Edge objects and returns float representing the angle from 0 to pi.
    '''

    validate_if_all_edge(edge_1, edge_2)

    edge_1 = edge_1.to_vector()
    edge_2 = edge_2.to_vector()

    cos_value = inner_prod(edge_1, edge_2) / (abs(edge_1) * abs(edge_2))  

    return acos(round(cos_value, 2))
    

def validate_if_all_edge(*args) -> None:
    if not all([isinstance(arg, Edge) for arg in args]):
        raise Exception(f"All given elements must be instance of the class Edge.")
