import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint


class Graph():
    def __init__(self, number_of_vertices:int, edges:list=None):
        '''
        The Graph object has two main attributes:
            number of vertices on one side - `number_of_vertices`:int (greater than 1);
            edges - `edges`:list 
                edges list contains tuples (at least one) with two numbers:int (from 0 to `number_of_vertices`-1))
                1st number is a vertex from 1st set (left one) and 2nd number is a vertex from 2nd set (right one)
        '''

        if not isinstance(number_of_vertices, int):
            raise Exception(f"`number_of_vertices` must be of type int, now it is {type(number_of_vertices)}.")
        if number_of_vertices < 2:
            raise Exception(f"`number_of_vertices` must be at least 2, now it is {number_of_vertices}.")
        
        self.NUMBER_OF_VERTICES = number_of_vertices
        
        self.set_edges(edges)

        
    def set_edges(self, edges:list) -> None:
        '''
        Validates `edges` and adds `self.EDGES` and `self.DETAILED_EDGES_INFO`

        Returns None.
        '''

        self.EDGES = None
        self.DETAILED_EDGES_INFO = None

        if edges is None:
            pass

        elif not isinstance(edges, list):
            raise Exception(f"`number_of_vertices` must be of type list, now it is {type(edges)}.")
        
        elif isinstance(edges, list):

            if len(edges) == 0:
                print(f"`edges` is empty, no edges has been set.")

            elif all([isinstance(element, tuple) and len(element) == 2 for element in edges]):
                indexes = [item for tuple_ in edges for item in tuple_]
                are_good_number = all(isinstance(item, int) and item >= 0 and item <= self.NUMBER_OF_VERTICES-1 for item in indexes)

                if are_good_number:
                    self.EDGES = list(set(edges))
                else:
                    raise Exception(f"Vertices indexes in `edges` must be from 0 to {self.NUMBER_OF_VERTICES-1} including.")

            else:
                raise Exception(f"All elements of `edges` must be tuple with 2 elements.")
            
        self.DETAILED_EDGES_INFO = self.add_detailed_edges_info()

            
            

    def add_detailed_edges_info(self) -> list:
        '''
        Returns list of dictionaries with detailed info about every edge:
            - "vertices":tuple - vertices the edge connects;
            - "line_coefs":tuple - coefficients of the line going through the vertices;
            - "intersection_points":list - points (x,y) the edge intersects with other edges;
            - "intersection_vertices":list - edges mentioned in "intersection_points" description.
        '''

        if self.EDGES is None:
            raise Exception(f"Method `add_detailed_edges_inf` should be used only if `self.EDGES` is not None.")

        detailed_edges_info = []

        for edge in self.EDGES:

            detailed_edge = {
            "vertices": edge,
            "line_coefs": ((edge[1] - edge[0]) / (self.NUMBER_OF_VERTICES-1), edge[0]),
            "intersection_points": [],
            "intersection_vertices": []
            }

            detailed_edges_info.append(detailed_edge)

        for index in range(len(detailed_edges_info)):

            edge_0 = detailed_edges_info[index]
            a_0, b_0 = edge_0["line_coefs"]

            for index_ in range(index+1, len(detailed_edges_info)):
                
                edge_1 = detailed_edges_info[index_]
                a_1, b_1 = edge_1["line_coefs"]

                if a_0 - a_1 != 0:

                    x_intersection = (b_1 - b_0) / (a_0 - a_1)

                    if x_intersection < self.NUMBER_OF_VERTICES-1 and x_intersection > 0:

                        y_intersection = a_0 * x_intersection + b_0 
                        intersection_point = (x_intersection, y_intersection)

                        edge_0["intersection_points"].append(intersection_point)
                        edge_0["intersection_vertices"].append(edge_1["vertices"])
                        edge_1["intersection_points"].append(intersection_point)
                        edge_1["intersection_vertices"].append(edge_0["vertices"])

        return detailed_edges_info


    # draw section
    def draw(self, edges:bool=True, intersections:bool=False) -> plt:
        '''
        Draws the graph using matplotlib.

        Returns the figure:plt.
        '''
        n = self.NUMBER_OF_VERTICES

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot()
        # ax.grid()

        points = [i for i in range(n)]

        ax.scatter(x=[0 for i in range(n)], y=points, color="royalblue", s=50, zorder=99)
        ax.scatter(x=[n-1 for i in range(n)], y=points, color="royalblue", s=50, zorder=99)

        if edges and not (self.EDGES is None):
            self.add_edges_to_draw(ax)
        if intersections and not (self.DETAILED_EDGES_INFO is None):
            self.add_intersections_to_draw(ax)

        
        return plt
    

    
    def add_edges_to_draw(self, ax) -> None:
        '''
        Adds edges to axes.
        
        Returns None.
        '''

        for edge in self.EDGES:
            x = [0, self.NUMBER_OF_VERTICES-1]
            y = [edge[0], edge[1]]
            ax.plot(x, y, color="goldenrod", zorder=25)



    def add_intersections_to_draw(self, ax) -> None:
        '''
        Adds intersection points to axes.
        
        Returns None.
        '''

        edges = self.DETAILED_EDGES_INFO
        
        intersection_points = [item for edge in edges for item in edge["intersection_points"]]
        intersection_points = set(intersection_points)

        ax.scatter(*zip(*intersection_points), color="black", zorder=75)
        