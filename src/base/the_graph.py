import matplotlib.pyplot as plt
import numpy as np

import settings

from base.base_graph_classes import Edge, Point, VertexPoint, IntersectionPoint, Poly
from base.edge_utils import cross_prod, angle_between_edges




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
        Main function creating the graph. 
        Validates and sets all (apart from number of vertices) information about the graph.

        Takes `edges`:list.

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
        '''
        Validates `edges` and create edges.

        Takes `edges`:list.

        Returns list of processed edges.
        '''

        n = self.NUM_OF_VERTS

        if not isinstance(edges, list):
            raise Exception(f"`number_of_vertices` must be of type list, now it is {type(edges)}.")
        
        # manages case when `edges` is a list
        elif isinstance(edges, list):

            # 0 edges case
            if len(edges) == 0:
                print(f"`edges` is empty, no edges has been set.")

            # all elements are of type tuple and all tuples have exactly 2 element 
            elif all([isinstance(element, tuple) and len(element) == 2 for element in edges]):

                # checks if all element in the tuples are ints in the interval [0, n-1]
                indexes = [item for tuple_ in edges for item in tuple_]
                are_good_number = all(isinstance(item, int) and item >= 0 and item <= n-1 for item in indexes)

                if are_good_number:
                    # delete (0, 0) and (n-1, n-1) edges so they will not cause conflicts in the future
                    edges_without_duplicates = [edge for edge in edges if edge != (0, 0) and edge != (n-1, n-1)]
                    # delete duplicated edges
                    edges_without_duplicates = list(set(edges_without_duplicates))
                    
                    processed_edges = []
                    # creates Edges objects of given info
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
        '''
        Adds important info to edges such as line coefficients of the line going through the vertices 
        and intersection points of the lines.

        Takes `edges`:list.

        Returns None.
        '''

        if edges is None:
            raise Exception(f"Method `add_detailed_edges_info` should be used only if `self.edges` is not None.")

        # adds line coefficients
        for edge in edges:
            vert_0 = edge.end_points[0]
            vert_1 = edge.end_points[1]

            edge.line_coefs = ((vert_1.y - vert_0.y) / (self.NUM_OF_VERTS-1), vert_0.y)

        # adds intersection points of edges
        for i in range(len(edges)):
            inter_points = []
            edge_0 = edges[i]
            a_0, b_0 = edge_0.line_coefs

            for j in range(len(edges)):
                edge_1 = edges[j]
                a_1, b_1 = edge_1.line_coefs

                # if a_0 = a_1 - lines are parallel
                if a_0 - a_1 != 0:
                    # calculate 1st coordinate of the intersection point
                    x_intersection = (b_1 - b_0) / (a_0 - a_1)

                    # checks if intersection point is between 0 and n-1, that is inside the square
                    eps = 10**(-5)  # computation error
                    if x_intersection < self.NUM_OF_VERTS-1-eps and x_intersection > 0+eps:

                        # calculate 2nd coordinate of the intersection point
                        y_intersection = a_0 * x_intersection + b_0 
                        intersection_point = IntersectionPoint(round(x_intersection, 4), round(y_intersection, 4))

                        inter_points.append(intersection_point)

            edge_0.intersection_points = inter_points

        return edges

    
    def add_intersection_points(self, edges:list) -> list:
        '''
        Deletes duplicating intersection points from edges.

        Takes `edges`:list.

        Returns list of changed edges.
        '''

        intersection_coords = []
        intersection_points = []

        # iterates through edges
        for edge in edges:
            # chooses only points being intersection points
            for point in edge.intersection_points:
                # adds if there's no such point in the list
                if point.coords not in intersection_coords:
                    intersection_points.append(point)
                    intersection_coords.append(point.coords)

        return intersection_points


    # branches points section
    def add_branches_to_points(self, edges:list, intersection_points:list) -> None:
        '''
        Adds branches points to every point.

        Takes `edges`:list and `intersection_points`:list.

        Returns None.
        '''

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

        # changes branches points having at most 2 branches points 
        # to points having more branches points
        for vert in left_verts:
            self.delete_branches_points_having_at_most_two_branches_points(vert, left_verts)

        for vert in right_verts:
            self.delete_branches_points_having_at_most_two_branches_points(vert, right_verts)


    def get_branches_points_to_verts(self, edges:list, vert:Point, side:str) -> list:
        '''
        Adds branches points to the given vert of the graph.

        Takes `edges`:list, `vert`:Point, `side`:str ("left" or "right").

        Returns list of points.
        '''

        if side == "left":
            side = 0
        elif side == "right":
            side = 1
        else:
            raise Exception(f"`side` must be 'right' or 'left', not f{side}.")
        
        branches_points = []
        # manages corner verts
        if self.is_a_corner(vert):
            # gets corner lying on the same hight
            temp_br = [point for point in self.verts if point.x != vert.x and point.y == vert.y][0]
            branches_points.append(temp_br)

        # gets points lying above or below the given vert
        horizontal_br = [point for point in self.verts if point.x == vert.x and (point.y == vert.y-1 or point.y == vert.y+1)]
        branches_points += horizontal_br

        # gets branches points by graph edges
        for edge in edges:
            # manage edges depending on what side (right or left) of the graph they lie on 
            if edge.end_points[side].y == vert.y:
               
                int_points = edge.intersection_points

                if len(int_points) != 0:
                    # sort points
                    int_points.sort(key=lambda point: point.x, reverse=bool(side))
                    branches_points.append(int_points[0])
                else:
                    branches_points.append(edge.end_points[1-side])

        return branches_points


    def get_branches_points_to_inter_point(self, edges:list, point:Point) -> list:
        '''
        Adds branches points to intersection points.

        Takes `edges`:list and `point`:Point.

        Returns list of the Point objects.
        '''

        branches_points = []

        for edge in edges:
            # gets all intersection points of the edge
            int_points_coords = [pt.coords for pt in edge.intersection_points]

            # if the point is an intersection point of the edge 
            if point.coords in int_points_coords:
                # sets before and after (having smaller and greater x coordinate) points to ends of the graph edge
                point_before = edge.end_points[0]
                point_after = edge.end_points[1]

                # loops through intersection points
                for inter_point in edge.intersection_points:
                    # if the x coordinate is:  now best left point < current point < main point
                    # change now best left point to current point
                    if inter_point.x < point.x and inter_point.x > point_before.x:
                        point_before = inter_point

                    # if the x coordinate is: main point < current point < now best right point
                    # change now best right point to current point
                    if inter_point.x > point.x and inter_point.x < point_after.x:
                        point_after = inter_point
                
                branches_points.append(point_before)
                branches_points.append(point_after)

        return branches_points
    
    
    def delete_branches_points_having_at_most_two_branches_points(self, vert:Point, verts:list) -> None:
        '''
        Change branches points having at most branches points to points having more branches points.

        Takes `vert`:Point, `verts`:list.

        Returns None. 
        '''
        
        n = self.NUM_OF_VERTS

        # change points going down
        if not self.is_a_corner(vert, "down"):
            # gets point below the vert
            point_to_fix = [point for point in vert.branches_points if point.coords == (vert.x, vert.y-1)][0]
            if not self.if_ok_num_of_branches_points(point_to_fix):
                new_point = self.get_fixed_point(vert, verts, -1)
                vert.branches_points.remove(point_to_fix)
                vert.branches_points.append(new_point)
        
        # change points going up
        if not self.is_a_corner(vert, "up"):
            # gets point above the vert
            point_to_fix = [point for point in vert.branches_points if point.coords == (vert.x, vert.y+1)][0]
            if not self.if_ok_num_of_branches_points(point_to_fix):
                new_point = self.get_fixed_point(vert, verts, 1)
                vert.branches_points.remove(point_to_fix)
                vert.branches_points.append(new_point)
        

    def get_fixed_point(self, vert:Point, verts:list, fix:int) -> Point:
        '''
        Searches next point below or above (fix = -1 or fix = 1).

        Takes `vert`, `verts` and `fix`:int (-1 or 1).

        Returns point if it is ok (has proper number of branches points).
        '''
        if fix != -1 and fix != 1:
            raise Exception(f"`fix` must be int and must be equal to '-1' or '1', now it's {fix}, type {type(fix)}.")
        
        # searches for the next point
        new_point = [point for point in verts if point.coords == (vert.x, vert.y+fix)][0]

        # checks if it is ok: if yes, return it; if no, continue searching 
        if self.if_ok_num_of_branches_points(new_point):
            new_point = self.get_fixed_point(vert, verts, fix)

        return new_point


    def if_ok_num_of_branches_points(self, point:Point) -> bool:
        '''
        Checks if point has enough branches points:
            every corner is ok;
            every intersection point is ok;
            vert of the graph not being the corner is ok if has at least 3 branches points.

        Takes `point`:Point.

        Returns bool.
        '''

        n = self.NUM_OF_VERTS
        
        if self.is_a_corner(point):
            return True
        elif (point.x == 0 or point.x == n-1) and len(point.branches_points) >= 3:
            return True
        elif point.x != 0 and point.x != n-1:
            return True

        return False
    

    # polygons section
    def get_polygons(self) -> list:
        '''
        Gets all polygons of the graph.
        All means the smallest polygons created by drawing the edges.
        The intersections of the polygons interiors are empty sets.

        Returns list of polygons with important info.
        '''
        MAX_ITER = 200  # in case sth goes wrong 

        graph_levels = []

        i = 0
        if_continue = True

        # manage the first polygon outside the loop
        graph_level_0 = self.get_first_graph_level()
        graph_levels.append(graph_level_0)

        # loop until stop condition or max iterations hit 
        while if_continue and i < MAX_ITER:

            # previous graph level
            prev_level_info = graph_levels[-1]

            temp_level = prev_level_info["level"] + 1
            temp_bottom_boundary = prev_level_info["upper_boundary"]
            polys =[]

            # iterate through edges of the bottom boundary of the level in search for polygons
            for edge in temp_bottom_boundary:
                poly = self.get_polygon_by_edge(edge)
                # if polygon was found and it has not already been in the list of polygons (prevent duplications)
                if poly is not None and poly not in polys:
                    polys.append(poly)

            # adds the edges of the polygons if they are inner edges and are not bottom edges
            temp_edges = [edge for poly in polys for edge in poly.inner_edges 
                          if edge not in temp_bottom_boundary and edge.reversed_edge() not in temp_bottom_boundary]

            # sometimes the direction of the edge changes, adds the edge only one time (prevent duplications) 
            edges = []
            edges = [edge for edge in temp_edges if edge not in edges and edge.reversed_edge() not in edges]

            # graph level dictionary template 
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


    def if_continue_level_searching(self, graph_lever_upper_boundary_polygons:list):
        '''
        Checks if searching should be continued - if no upper (inner) boundary, no.

        Takes list of bottom edges.

        Returns bool.  
        '''

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
    

    def get_polygon_by_edge(self, edge:Edge) -> Poly:
        '''
        Gets the next polygon by the given edge.

        Takes `edge`:Edge.

        Returns Poly object.
        '''

        # set start_point to the point with smaller x coordinate
        if edge.end_points[0].x < edge.end_points[1].x:
            start_point = edge.end_points[0]
        elif edge.end_points[0].x > edge.end_points[1].x:
            start_point = edge.end_points[1]
        else:
            return []

        polygon_edges = [start_point]

        cont = True
        i = 0

        # loop until stop condition or i = 10 hits
        while cont and i < 10:
            # gets the next edge in the polygon
            next_point = self.get_next_edge_in_polygon(edge, start_point)

            # stops if polygon closes
            if next_point in polygon_edges:
                cont = False

            # case when polygon does not close
            else:
                polygon_edges.append(next_point)

                edge = Edge(next_point, start_point)
                start_point = next_point

            i += 1

        # create Poly object
        polygon = Poly(self.NUM_OF_VERTS, *polygon_edges)
        return polygon


    def get_next_edge_in_polygon(self, edge:Edge, start_point:Point) -> Point:
        '''
        Finds the next edge of the polygon (Point object).

        Takes `edge`:Edge (the last found polygon edge) and 
        `start_point` (point from which search should be started).

        Returns Point
        '''

        # search in all points in the graph - verts and intersection points
        all_points = self.verts + self.intersection_points

        # set end point of the edge
        if start_point == edge.end_points[0]:
            end_point = edge.end_points[1]
        elif start_point == edge.end_points[1]:
            end_point = edge.end_points[0]
        else:
            raise Exception(f"No such point in edge end_points.")

        # make start_point a point found in all_points (cuz they have info about the graph i.e. their branches points)
        for point in all_points:
            if point == start_point:
                start_point = point

        # set the point so it can be changed into another one
        temp_point = start_point
        # set the angle so it can be compared to other angles 
        temp_angle = np.pi * 2 

        # iterate through branches points 
        for point in start_point.branches_points:
            # do not want to find end_point - point of the current edge
            if point != end_point:

                # calculate the angle and cross product of the edges
                angle = angle_between_edges(Edge(start_point, end_point), Edge(start_point, point))
                cross_product = cross_prod(Edge(start_point, end_point), Edge(start_point, point))

                # cross product is used to orient the polygon
                # the angle must be the smallest
                if cross_product[2] >= 0 and angle < temp_angle:
                    temp_angle = angle
                    temp_point = point
                
        next_point = temp_point
        
        return next_point
    

    # calculating area section
    def get_area_of_polys(self) -> tuple:
        '''
        Calculates the area of polys in odd and even levels.

        Returns (even_area_val, odd_area_val).
        '''

        even_levels_polys = self.get_odd_or_even_levels_polys("even")
        odd_levels_polys = self.get_odd_or_even_levels_polys("odd")

        area_of_even_level = self.get_area_of_given_polys(even_levels_polys)
        area_of_odd_level = self.get_area_of_given_polys(odd_levels_polys)
        
        return (area_of_even_level, area_of_odd_level)
    

    def get_area_of_level(self, level:int) -> float:
        '''
        Calculates the area of polys in a given level of the graph.

        Takes `level`:int.

        Returns the area value:float.
        '''

        if not isinstance(level, int):
            raise Exception(f"`level` must be of type int, not it is {type(level)}")
        
        polys_to_calc = [poly for level in self.graph_levels for 
                         poly in level.get("polygons") if level.get("level") == level]
        
        if len(polys_to_calc) == 0:
            raise Exception("No such level in a graph.")
        
        return self.get_area_of_given_polys(polys_to_calc)


    def get_area_of_given_polys(self, polys) -> float:
        '''
        Calculates area of polys given in a list.

        Takes list of Poly objects.

        Returns the area:float.
        '''
        if not isinstance(polys, list):
            raise Exception(f"`polys` must be of type list, now it's {type(polys)}.")
        if not all([isinstance(poly, Poly) for poly in polys]):
            raise Exception(f"All elements of `polys` must be of type Poly.")

        polys_area = 0

        for poly in polys:
            polys_area += self.get_area_of_poly(poly)
        
        return polys_area


    def get_area_of_poly(self, poly:Poly) -> float:
        '''
        Calculates area of the given polygon using shoelace formula:
        https://en.wikipedia.org/wiki/Shoelace_formula
        
        Takes poly:Polygon.

        Returns the area:float.
        '''
        if not isinstance(poly, Poly):
            raise Exception(f"`poly` must be of type Poly, not it's {type(poly)}.")

        area = 0

        num_of_verts = len(poly.verts)
        for i in range(num_of_verts):
            j = i + 1

            if i == num_of_verts-1:
                j = 0

            x_1 = poly[i].x
            y_1 = poly[i].y
            x_2 = poly[j].x
            y_2 = poly[j].y

            area += x_1*y_2 - x_2*y_1

        return abs(area)/2


    def check_if_sums_up_to_square(self, area_1:float, area_2:float, error_val:float=0.001) -> bool:
        '''
        Checks if sum of two areas is equal to area of the graph square.

        Takes to floats representing areas and 
        optionally `error_val`:float representing permissible error of the area.

        Return bool.
        '''

        if not isinstance(error_val, float) and error_val not in [0, 1]:
            raise Exception(f"`error_val` must be float or int from the interval [0,1], now it's {error_val} of type {type(error_val)}")
            

        square_area = (self.NUM_OF_VERTS-1)**2
        bottom_value = (area_1 + area_2) * (1 - error_val)
        upper_value = (area_1 + area_2) * (1 + error_val)

        if square_area <= upper_value and square_area >= bottom_value:
            return True
        
        return False


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
            self.add_polygons_to_draw()
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


    def add_polygons_to_draw(self):
        '''
        Adds colored polygons to plt.
        
        Returns None.
        '''

        even_levels_polys = self.get_odd_or_even_levels_polys("even")
        odd_levels_polys = self.get_odd_or_even_levels_polys("odd")

        for poly in even_levels_polys:
            X = np.array([list(point.coords) for point in poly.verts])
            t1 = plt.Polygon(X, **settings.first_level_polygons)
            plt.gca().add_patch(t1)
            
        for poly in odd_levels_polys:
            X = np.array([list(point.coords) for point in poly.verts])
            t1 = plt.Polygon(X, **settings.second_level_polygons)
            plt.gca().add_patch(t1)
        

    def add_frame_to_draw(self, ax):
        '''
        Adds fame to axes.
        
        Returns None.
        '''

        n = self.NUM_OF_VERTS
        x = [0, 0, n-1, n-1, 0]
        y = [0, n-1, n-1, 0, 0]
        ax.plot(x, y, **settings.frame_lines)


    # graph utils section
    def get_odd_or_even_levels_polys(self, mode:str="both"):
        '''
        Returns all polygons in a given levels: odd, even or both.

        Takes `mode`:str ("even", "odd" or "both").

        Returns list of polygons. 
        ''' 

        if mode not in ["even", "odd", "both"]:
            raise Exception(f'''`mode` must be str equal to 'even', 'odd' or 'both', 
                            now it's {mode} of type {type(mode)}.''')
        
        if mode == "even":
            return [poly for level in self.graph_levels for poly in level.get("polygons") if level.get("level") % 2 == 0]
        elif mode == "odd":
            return [poly for level in self.graph_levels for poly in level.get("polygons") if level.get("level") % 2 == 1]
            
        return [poly for level in self.graph_levels for poly in level.get("polygons")]
    
    def is_a_corner(self, point:Point, mode:str="both"):
        '''
        Checks if given point is a corner point.

        Takes `point`:Point and mode:str ("up", "down" or "both").

        Returns bool.
        '''
        if not isinstance(point, Point):
            raise Exception(f"`point` must be of type Point, not it's {type(point)}.")
        if mode not in ["both", "up", "down"]:
            raise Exception(f'''`mode` must be of type str and equal to 'both', 'up' or 'down',
                            now it's {mode} of type {type(mode)}''')

        n = self.NUM_OF_VERTS

        corners = [Point(0,0), Point(n-1, 0), Point(0, n-1), Point(n-1, n-1)]

        if mode == "both" and point in corners:
            return True
        elif mode == "down" and point in corners[:2]:
            return True
        elif mode == "up" and point in corners[2:]:
            return True
        
        return False
    