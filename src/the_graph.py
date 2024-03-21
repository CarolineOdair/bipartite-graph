import numpy as np
import matplotlib.pyplot as plt
from point import Point, VertexPoint, IntersectionPoint
from edge import Edge
from polygon import Poly
from edge_utils import cross_prod, angle_between_edges
import settings


class Graph():
    edges = None
    verts = None
    intersection_points = []
    all_points = []
    graph_levels = None

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
        self.intersection_points = intersection_points

        self.add_branches_to_points(edges, self.intersection_points)
        levels = self.get_polygons()

        self.edges = edges
        
        self.graph_levels = levels





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
                        processed_edges.append(Edge(x, y))
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


    # branches points section
    def add_branches_to_points(self, edges, intersection_points) -> None:

        left_verts = [vert for vert in self.verts if vert.x == 0]
        right_verts = [vert for vert in self.verts if vert.x == self.NUM_OF_VERTS-1]

        # TODO delete from branches_points points having only 2 branches points
        # manage left side of square
        for vert in left_verts:
            vert.branches_points = self.get_branches_points_to_verts(edges, vert, "left")

        # manage right side of square
        for vert in right_verts:
            vert.branches_points = self.get_branches_points_to_verts(edges, vert, "right")

        # manage intersection_points
        for point in intersection_points:
            point.branches_points = self.get_branches_points_to_inter_point(edges, point)

        for vert in left_verts:
            self.delete_branches_points_having_at_most_two_branches_points(vert, left_verts)

        for vert in right_verts:
            self.delete_branches_points_having_at_most_two_branches_points(vert, right_verts)

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
    
    def delete_branches_points_having_at_most_two_branches_points(self, vert, verts):

        n = self.NUM_OF_VERTS

        bottom_corners = [Point(0, 0), Point(n-1, 0)]
        if vert not in bottom_corners:
            point_to_fix = [point for point in vert.branches_points if point.coords == (vert.x, vert.y-1)][0]
            if not self.if_ok_num_of_branches_points(point_to_fix):
                new_point = self.get_fixed_point(vert, verts, -1)
                vert.branches_points.remove(point_to_fix)
                vert.branches_points.append(new_point)
        
        upper_corners = [Point(0, n-1), Point(n-1, n-1)]
        if vert not in upper_corners:
            point_to_fix = [point for point in vert.branches_points if point.coords == (vert.x, vert.y+1)][0]
            if not self.if_ok_num_of_branches_points(point_to_fix):
                new_point = self.get_fixed_point(vert, verts, 1)
                vert.branches_points.remove(point_to_fix)
                vert.branches_points.append(new_point)
        
        # return vert

    def get_fixed_point(self, vert, verts, fix:int) -> Point:
        new_point = [point for point in verts if point.coords == (vert.x, vert.y+fix)][0]
        if self.if_ok_num_of_branches_points(new_point):
            new_point = self.get_fixed_point(vert, verts, fix)
        return new_point


    def if_ok_num_of_branches_points(self, point) -> bool:

        n = self.NUM_OF_VERTS
        corner_points = [Point(0,0), Point(0, n-1), Point(n-1, n-1), Point(n-1, 0)]
        
        if point in corner_points:
            return True
        elif (point.x == 0 or point.x == n-1) and len(point.branches_points) >= 3:
            return True
        elif point.x != 0 and point.x != n-1:
            return True

        return False
    

    # polygons section
    def get_polygons(self):
        MAX_ITER = 200  # in case sth goes wrong 

        graph_levels = []

        i = 0
        if_continue = True

        graph_level_0 = self.get_first_graph_level()
        graph_levels.append(graph_level_0)

        while if_continue and i < MAX_ITER:

            prev_level_info = graph_levels[-1]

            temp_level = prev_level_info["level"] + 1
            temp_bottom_boundary = prev_level_info["upper_boundary"]
            polys =[]

            for edge in temp_bottom_boundary:
                poly = self.get_polygon_by_edge(edge)
                if poly is not None and poly not in polys:
                    polys.append(poly)

            temp_edges = [edge for poly in polys for edge in poly.inner_edges 
                          if edge not in temp_bottom_boundary and edge.reversed_edge() not in temp_bottom_boundary]

            edges = []
            edges = [edge for edge in temp_edges if edge not in edges and edge.reversed_edge() not in edges]

            graph_level = {
                "level": temp_level,
                "polygons": polys,
                "upper_boundary": edges,
                "bottom_boundary": temp_bottom_boundary
            }
            graph_levels.append(graph_level)

            i += 1
            if_continue = self.if_continue_level_searching(graph_level["upper_boundary"])

        return graph_levels



    def if_continue_level_searching(self, graph_lever_upper_boundary_polygons):

        if len(graph_lever_upper_boundary_polygons) == 0:
            return False

        return True
    
    def get_first_graph_level(self) -> dict:

        start_edge = Edge(Point(0,0), Point(self.NUM_OF_VERTS-1, 0))
        start_poly = self.get_polygon_by_edge(start_edge)
        graph_level_0 = {
            "level": 0,
            "polygons": [start_poly],
            "upper_boundary": [edge for edge in start_poly.inner_edges],
            "bottom_boundary": [start_edge]
        }

        return graph_level_0
    

    def get_polygon_by_edge(self, edge:Edge):

        if edge.end_points[0].x < edge.end_points[1].x:
            start_point = edge.end_points[0]
        elif edge.end_points[0].x > edge.end_points[1].x:
            start_point = edge.end_points[1]
        else:
            return []

        polygon_edges = [start_point]

        cont = True
        i = 0
        while cont and i < 10:
            next_point = self.get_next_edge_in_polygon(edge, start_point)

            if next_point in polygon_edges:
                # print(polygon_edges, next_point)
                cont = False

            else:
                polygon_edges.append(next_point)

                edge = Edge(next_point, start_point)
                start_point = next_point

            i += 1

        polygon = Poly(self.NUM_OF_VERTS, *polygon_edges)
        return polygon


    def get_next_edge_in_polygon(self, edge, start_point:Point):

        all_points = self.verts + self.intersection_points

        if start_point == edge.end_points[0]:
            end_point = edge.end_points[1]
        elif start_point == edge.end_points[1]:
            end_point = edge.end_points[0]
        else:
            raise Exception(f"No such point in edge end_points.")

        for point in all_points:
            if point == start_point:
                start_point = point

        temp_point = start_point
        temp_angle = np.pi * 2

        for point in start_point.branches_points:

            if point != end_point:

                angle = angle_between_edges(Edge(start_point, end_point), Edge(start_point, point))

                cross_product = cross_prod(Edge(start_point, end_point), Edge(start_point, point))

                if cross_product[2] >= 0 and angle < temp_angle:
                    temp_angle = angle
                    temp_point = point
                
                
        next_point = temp_point
        
        return next_point



    # draw section
    def draw(self, edges:bool=True, intersections:bool=False, polygons:bool=False, frame:bool=False) -> plt:
        '''
        Draws the graph using matplotlib.

        Returns the figure:plt.
        '''
        n = self.NUM_OF_VERTS

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot()
        ax.grid()

        points = [i for i in range(n)]

        ax.scatter(x=[0 for i in range(n)], y=points, **settings.right_side_points)
        ax.scatter(x=[n-1 for i in range(n)], y=points, **settings.left_side_points)

        if edges and not (self.edges is None):
            self.add_edges_to_draw(ax)
        if intersections and not (self.edges is None):
            self.add_intersections_to_draw(ax)
        if polygons and not (self.graph_levels is None):
            self.add_polygons_to_draw(ax)
        if frame:
            self.add_frame_to_draw(ax)

        
        return plt
    

    
    def add_edges_to_draw(self, ax) -> None:
        '''
        Adds edges to axes.
        
        Returns None.
        '''

        for edge in self.edges:
            x = [0, self.NUM_OF_VERTS-1]
            y = [edge.end_points[0].y, edge.end_points[1].y]
            ax.plot(x, y, **settings.graph_edges_lines)


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


        ax.scatter(x, y, **settings.intersection_points)

    def add_polygons_to_draw(self, ax):
        odd_levels_polys = [poly for level in self.graph_levels for poly in level.get("polygons") if level.get("level") % 2 == 1]
        even_levels_polys = [poly for level in self.graph_levels for poly in level.get("polygons") if level.get("level") % 2 == 0]

        for poly in even_levels_polys:
            X = np.array([list(point.coords) for point in poly.verts])
            t1 = plt.Polygon(X, **settings.first_level_polygons)
            plt.gca().add_patch(t1)
            
        for poly in odd_levels_polys:
            X = np.array([list(point.coords) for point in poly.verts])
            t1 = plt.Polygon(X, **settings.second_level_polygons)
            plt.gca().add_patch(t1)
        
    def add_frame_to_draw(self, ax):

        n = self.NUM_OF_VERTS
        x = [0, 0, n-1, n-1, 0]
        y = [0, n-1, n-1, 0, 0]
        ax.plot(x, y, **settings.frame_lines)
        