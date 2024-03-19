import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
from point import Point, VertexPoint, IntersectionPoint
from edge import Edge, InnerEdge, OuterEdge, PolygonalEdge
from edge_utils import cross_prod, angle_between_edges


class Graph():
    edges = None
    verts = None
    intersection_points = []
    all_points = []

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
        
        self.NUM_OF_VERTS = number_of_vertices

        self.verts = [
            VertexPoint(0, num) for num in range(self.NUM_OF_VERTS)
            ] + [
            VertexPoint(self.NUM_OF_VERTS-1, num) for num in range(self.NUM_OF_VERTS)             
            ]

        
        self.set_edges(edges)

        
    def set_edges(self, edges:list) -> None:
        '''
        Validates `edges` and adds `self.edges` and `intersection_points`.

        Returns None.
        '''

        edges = self.validate_and_set_edges(edges)
        edges = self.add_detailed_edges_info(edges)
        intersection_points = self.add_intersection_points(edges)
        self.add_branches_to_points(edges, intersection_points)

        self.edges = edges
        self.intersection_points = intersection_points





    def validate_and_set_edges(self, edges:list) -> list:

        n = self.NUM_OF_VERTS

        if edges is None:
            pass

        elif not isinstance(edges, list):
            raise Exception(f"`number_of_vertices` must be of type list, now it is {type(edges)}.")
        
        elif isinstance(edges, list):

            if len(edges) == 0:
                print(f"`edges` is empty, no edges has been set.")

            elif all([isinstance(element, tuple) and len(element) == 2 for element in edges]):
                indexes = [item for tuple_ in edges for item in tuple_]
                are_good_number = all(isinstance(item, int) and item >= 0 and item <= n-1 for item in indexes)

                if are_good_number:
                    edges_without_duplicates = [edge for edge in edges if edge != (0, 0) and edge != (n-1, n-1)]
                    edges_without_duplicates = list(set(edges_without_duplicates))
                    
                    processed_edges = []
                    for edge in edges_without_duplicates:
                        x = [point for point in self.verts if point.coords == (0, edge[0])][0]
                        y = [point for point in self.verts if point.coords == (n-1, edge[1])][0]
                        processed_edges.append(InnerEdge(x, y))
                else:
                    raise Exception(f"Vertices indexes in `edges` must be from 0 to {n-1} including.")

            else:
                raise Exception(f"All elements of `edges` must be tuple with 2 elements.")
            
        return processed_edges

            
    def add_detailed_edges_info(self, edges:list) -> None:

        if edges is None:
            raise Exception(f"Method `add_detailed_edges_info` should be used only if `self.edges` is not None.")

        for edge in edges:

            vert_0 = edge.end_points[0]
            vert_1 = edge.end_points[1]

            edge.line_coefs = ((vert_1.y - vert_0.y) / (self.NUM_OF_VERTS-1), vert_0.y)

        for i in range(len(edges)):

            inter_points = []
            edge_0 = edges[i]
            a_0, b_0 = edge_0.line_coefs

            for j in range(len(edges)):
                
                edge_1 = edges[j]
                a_1, b_1 = edge_1.line_coefs

                if a_0 - a_1 != 0:


                    x_intersection = (b_1 - b_0) / (a_0 - a_1)

                    if x_intersection < self.NUM_OF_VERTS-1 and x_intersection > 0:

                        y_intersection = a_0 * x_intersection + b_0 
                        intersection_point = IntersectionPoint(round(x_intersection, 4), round(y_intersection, 4))

                        inter_points.append(intersection_point)

            edge_0.intersection_points = inter_points

        return edges


    
    def add_intersection_points(self, edges:list) -> list:

        intersection_coords = []
        intersection_points = []

        for edge in edges:
            for point in edge.intersection_points:
                if point.coords not in intersection_coords:
                    intersection_points.append(point)
                    intersection_coords.append(point.coords)

        return intersection_points


    def add_branches_to_points(self, edges, intersection_points) -> None:

        left_verts = [vert for vert in self.verts if vert.x == 0]
        right_verts = [vert for vert in self.verts if vert.x == self.NUM_OF_VERTS-1]


        # manage left side of square
        for vert in left_verts:
            vert.branches_points = self.get_branches_points_to_verts(edges, vert, "left")

        # manage right side of square
        for vert in right_verts:
            vert.branches_points = self.get_branches_points_to_verts(edges, vert, "right")

        # manage intersection_points
        for point in intersection_points:
            point.branches_points = self.get_branches_points_to_inter_point(edges, point)

    def get_branches_points_to_verts(self, edges:list, vert:Point, side:str) -> list:

        if side == "left":
            side = 0
        elif side == "right":
            side = 1
        else:
            raise Exception(f"`side` must be `right` or `left`, not f{side}.")
        
        branches_points = []

        if vert.coords in [(0, 0), (0, self.NUM_OF_VERTS-1), (self.NUM_OF_VERTS-1, 0), (self.NUM_OF_VERTS, self.NUM_OF_VERTS)]:
            temp_br = [point for point in self.verts if point.x != vert.x and point.y == vert.y][0]
            branches_points.append(temp_br)

        horizontal_br = [point for point in self.verts if point.x == vert.x and (point.y == vert.y-1 or point.y == vert.y+1)]
        branches_points += horizontal_br

        for edge in edges:
            if edge.end_points[side].y == vert.y:
               
                int_points = edge.intersection_points

                if len(int_points) != 0:
                    int_points.sort(key=lambda point: point.x, reverse=bool(side))
                    branches_points.append(int_points[0])
                else:
                    branches_points.append(edge.end_points[1-side])

        return branches_points


    def get_branches_points_to_inter_point(self, edges:list, point:Point) -> list:

        branches_points = []

        for edge in edges:
            int_points_coords = [pt.coords for pt in edge.intersection_points]

            if point.coords in int_points_coords:
                point_before = edge.end_points[0]
                point_after = edge.end_points[1]

                for inter_point in edge.intersection_points:
                    if inter_point.x < point.x and inter_point.x > point_before.x:
                        point_before = inter_point

                    if inter_point.x > point.x and inter_point.x < point_after.x:
                        point_after = inter_point
                
                branches_points.append(point_before)
                branches_points.append(point_after)

        return branches_points



    # draw section
    def draw(self, edges:bool=True, intersections:bool=False) -> plt:
        '''
        Draws the graph using matplotlib.

        Returns the figure:plt.
        '''
        n = self.NUM_OF_VERTS

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot()
        ax.grid()

        points = [i for i in range(n)]

        ax.scatter(x=[0 for i in range(n)], y=points, color="royalblue", s=50, zorder=99)
        ax.scatter(x=[n-1 for i in range(n)], y=points, color="royalblue", s=50, zorder=99)

        if edges and not (self.edges is None):
            self.add_edges_to_draw(ax)
        if intersections and not (self.edges is None):
            self.add_intersections_to_draw(ax)

        
        return plt
    

    
    def add_edges_to_draw(self, ax) -> None:
        '''
        Adds edges to axes.
        
        Returns None.
        '''

        for edge in self.edges:
            x = [0, self.NUM_OF_VERTS-1]
            y = [edge.end_points[0].y, edge.end_points[1].y]
            ax.plot(x, y, color="goldenrod", zorder=25)


    def add_intersections_to_draw(self, ax) -> None:
        '''
        Adds intersection points to axes.
        
        Returns None.
        '''

        x = []
        y = []

        for point in self.intersection_points:
            x.append(point.x)
            y.append(point.y)

        ax.scatter(x, y, color="black", zorder=75)
        