import math
from math import sqrt
from Renderer.ThemeClass import *
import pygame


class GraphRenderer:
    def __init__(self, display=None, graph=None):
        self.display = display
        self.setting = self.Settings()
        self.camera = self.Camera()
        self.graph = graph
        self.vertex_show_info = None
        self.edge_show_info = None
        self.button_show_info = None
        self.selected_area = {"x1": 0, "y1": 0, "x2": 0, "y2": 0}
        # ## theme
        self.light_theme = BlueLightTheme()
        self.dark_theme = OrangeDarkTheme()
        self.theme = self.dark_theme
        # ## buttons
        self.buttons = list()

    def set_graph(self, graph):
        self.graph = graph
        camera_borders = [0, 0, 0, 0]
        if graph is not None and len(graph.borders) >= 4:
            camera_borders[0] = graph.borders[0] - (self.display.get_width() / self.camera.scale)
            camera_borders[1] = graph.borders[1]
            camera_borders[2] = graph.borders[2] - (self.display.get_height() / self.camera.scale)
            camera_borders[3] = graph.borders[3]
        self.camera.set_borders([-border for border in camera_borders])

    def set_display(self, display):
        self.display = display

    def set_buttons(self, buttons):
        self.buttons = buttons

    def set_selected_area(self, sizes):
        self.selected_area = sizes

    def change_theme(self):
        if type(self.theme) == OrangeDarkTheme:
            self.theme = self.light_theme
        else:
            self.theme = self.dark_theme

        for button in self.buttons:
            button.set_theme(self.theme)

    def get_vertexes_by_area(self, area):
        if self.graph is None:
            return []
        min_x = - self.camera.position[0] + (min(area["x1"], area["x2"]) / self.camera.scale)
        max_x = - self.camera.position[0] + (max(area["x1"], area["x2"]) / self.camera.scale)

        min_y = - self.camera.position[1] + (min(area["y1"], area["y2"]) / self.camera.scale)
        max_y = - self.camera.position[1] + (max(area["y1"], area["y2"]) / self.camera.scale)
        vertexes_to_return = []
        for vertex in self.graph.vertexes:
            if min_x < vertex.position[0] < max_x and min_y < vertex.position[1] < max_y:
                vertexes_to_return.append(vertex)

        return vertexes_to_return

    def get_vertex_by_position(self, position):
        if self.graph is None:
            return None
        for vertex in self.graph.vertexes:
            vertex_position_to_draw = [0, 0]
            vertex_position_to_draw[0] = (vertex.position[0] + self.camera.position[0]) * self.camera.scale
            vertex_position_to_draw[1] = (vertex.position[1] + self.camera.position[1]) * self.camera.scale

            # ## (x-a)^2 + (y-b)^2 <= R^2
            xa2 = ((position[0] - vertex_position_to_draw[0]) ** 2)
            yb2 = ((position[1] - vertex_position_to_draw[1]) ** 2)
            r2 = (self.setting.vertexes_radius ** 2)
            if xa2 + yb2 < r2:
                return vertex
        return None

    def get_edges_by_area(self, area):
        edges_to_return = []
        if self.graph is None:
            return edges_to_return

        if area["x1"] == area["x2"] and area["y1"] == area["y2"]:
            return edges_to_return

        min_x = - self.camera.position[0] + (min(area["x1"], area["x2"]) / self.camera.scale)
        max_x = - self.camera.position[0] + (max(area["x1"], area["x2"]) / self.camera.scale)

        min_y = - self.camera.position[1] + (min(area["y1"], area["y2"]) / self.camera.scale)
        max_y = - self.camera.position[1] + (max(area["y1"], area["y2"]) / self.camera.scale)

        rectangle = [
            ((min_x, min_y), (min_x, max_y)),
            ((min_x, max_y), (max_x, max_y)),
            ((max_x, max_y), (max_x, min_y)),
            ((max_x, min_y), (min_x, min_y))
        ]
        # https://e-maxx.ru/algo/segments_intersection_checking
        area = lambda a, b, c: (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        intersect_1 = lambda a_, b_, c_, d_: max(min(a_, b_), min(c_, d_)) <= min(max(a_, b_), max(c_, d_))
        intersect = lambda a, b, c, d: (intersect_1(a[0], b[0], c[0], d[0])
                                        and intersect_1(a[1], b[1], c[1], d[1])
                                        and area(a, b, c) * area(a, b, d) <= 0
                                        and area(c, d, a) * area(c, d, b) <= 0)

        for edge in self.graph.edges:
            vertex_first_position = self.graph.get_vertex_by_identifier(edge.vertex_identifier_first).position
            vertex_second_position = self.graph.get_vertex_by_identifier(edge.vertex_identifier_second).position
            intersection_exist = False
            for side in rectangle:
                if intersect(vertex_first_position, vertex_second_position, side[0], side[1]):
                    intersection_exist = True
                    break
            if intersection_exist:
                edges_to_return.append(edge)
            # checking the case when both edges vertexes are inside the selected area
            else:
                Ds_vertex_first = [0, 0, 0, 0]
                Ds_vertex_second = [0, 0, 0, 0]
                for side in rectangle:
                    vertex1 = self.graph.get_vertex_by_identifier(edge.vertex_identifier_first)
                    vertex2 = self.graph.get_vertex_by_identifier(edge.vertex_identifier_first)
                    Ds_vertex_first[rectangle.index(side)] = (side[1][0] - side[0][0]) * (vertex1.position[1] - side[0][1]) - \
                                                             (vertex1.position[0] - side[0][0]) * (side[1][1] - side[0][1])
                    Ds_vertex_second[rectangle.index(side)] = (side[1][0] - side[0][0]) * (vertex2.position[1] - side[0][1]) - \
                                                             (vertex2.position[0] - side[0][0]) * (side[1][1] - side[0][1])
                    # D = (x2 - x1) * (yp - y1) - (xp - x1) * (y2 - y1)
                    # If D > 0, the point is on the left-hand side.
                    # If D < 0, the point is on the right-hand side.
                    # If D = 0, the point is on the line.
                if (
                    (
                        (min(Ds_vertex_first) <= 0 and max(Ds_vertex_first) <= 0)
                        or
                        (min(Ds_vertex_first) >= 0 and max(Ds_vertex_first) >= 0)
                    )
                    or
                    (
                        (min(Ds_vertex_second) <= 0 and max(Ds_vertex_second) <= 0)
                        or
                        (min(Ds_vertex_second) >= 0 and max(Ds_vertex_second) >= 0)
                    )
                ):
                    if edge not in edges_to_return:
                        edges_to_return.append(edge)

        return edges_to_return

    def get_edge_by_position(self, position):
        if self.graph is None:
            return None
        for edge in self.graph.edges:
            vertex_first = self.graph.get_vertex_by_identifier(edge.vertex_identifier_first)
            vertex_second = self.graph.get_vertex_by_identifier(edge.vertex_identifier_second)
            # ## ## defining the points of the square where the transmitted position can be
            vertex_first_position_to_draw = [0, 0]
            vertex_first_position_to_draw[0] = (vertex_first.position[0] + self.camera.position[0]) * self.camera.scale
            vertex_first_position_to_draw[1] = (vertex_first.position[1] + self.camera.position[1]) * self.camera.scale
            vertex_second_position_to_draw = [0, 0]
            vertex_second_position_to_draw[0] = (vertex_second.position[0] + self.camera.position[0]) * self.camera.scale
            vertex_second_position_to_draw[1] = (vertex_second.position[1] + self.camera.position[1]) * self.camera.scale

            T01 = vertex_first_position_to_draw
            T02 = vertex_second_position_to_draw
            T1 = [0, 0]
            T2 = [0, 0]
            distance_between_vertexes = sqrt((abs(T01[0] - T02[0]) ** 2) + (abs(T01[1] - T02[1]) ** 2))
            coefficient_points = self.setting.vertexes_radius / distance_between_vertexes
            dist_x_between_T12_T0102 = (abs(T01[0] - T02[0])) * coefficient_points
            dist_y_between_T12_T0102 = (abs(T01[1] - T02[1])) * coefficient_points

            T1[0] = T01[0] - dist_x_between_T12_T0102 if T01[0] > T02[0] else T01[0] + dist_x_between_T12_T0102
            T1[1] = T01[1] - dist_y_between_T12_T0102 if T01[1] > T02[1] else T01[1] + dist_y_between_T12_T0102

            T2[1] = T02[1] - dist_y_between_T12_T0102 if T01[1] < T02[1] else T02[1] + dist_y_between_T12_T0102
            T2[0] = T02[0] - dist_x_between_T12_T0102 if T01[0] < T02[0] else T02[0] + dist_x_between_T12_T0102

            T3 = [0, 0]
            T4 = [0, 0]
            T5 = [0, 0]
            T6 = [0, 0]

            distance_between_points = sqrt((abs(T1[0] - T2[0]) ** 2) + (abs(T1[1] - T2[1]) ** 2))
            dist_x_between_T1_T2 = (abs(T1[0] - T2[0]))
            dist_y_between_T1_T2 = (abs(T1[1] - T2[1]))
            coefficient = self.setting.edges_width / distance_between_points
            dist_x_between_T12_T3456 = dist_y_between_T1_T2 * coefficient
            dist_y_between_T12_T3456 = dist_x_between_T1_T2 * coefficient
            T3[0] = T1[0] - dist_x_between_T12_T3456 \
                if vertex_first_position_to_draw[0] < vertex_second_position_to_draw[0] \
                else T1[0] + dist_x_between_T12_T3456
            T3[1] = T1[1] + dist_y_between_T12_T3456 \
                if vertex_first_position_to_draw[1] < vertex_second_position_to_draw[1] \
                else T1[1] - dist_y_between_T12_T3456

            T5[0] = T2[0] - dist_x_between_T12_T3456 \
                if vertex_first_position_to_draw[0] < vertex_second_position_to_draw[0] \
                else T2[0] + dist_x_between_T12_T3456
            T5[1] = T2[1] + dist_y_between_T12_T3456 \
                if vertex_first_position_to_draw[1] < vertex_second_position_to_draw[1] \
                else T2[1] - dist_y_between_T12_T3456

            # ## ###
            T4[0] = T1[0] + dist_x_between_T12_T3456 \
                if vertex_first_position_to_draw[0] < vertex_second_position_to_draw[0] \
                else T1[0] - dist_x_between_T12_T3456
            T4[1] = T1[1] - dist_y_between_T12_T3456 \
                if vertex_first_position_to_draw[1] < vertex_second_position_to_draw[1] \
                else T1[1] + dist_y_between_T12_T3456

            T6[0] = T2[0] + dist_x_between_T12_T3456 \
                if vertex_first_position_to_draw[0] < vertex_second_position_to_draw[0] \
                else T2[0] - dist_x_between_T12_T3456
            T6[1] = T2[1] - dist_y_between_T12_T3456 \
                if vertex_first_position_to_draw[1] < vertex_second_position_to_draw[1] \
                else T2[1] + dist_y_between_T12_T3456

            # ## ### draw lines
            # pygame.draw.aaline(self.display, (255, 40, 0), T1, T2)  # red
            # pygame.draw.aaline(self.display, (0, 40, 255), T3, T5)  # blue
            # pygame.draw.aaline(self.display, (40, 255, 0), T4, T6)  # green

            #         \          T4 .________________. T6          /
            #  vertex1| T01 .___ T1 !______EDGE______! T2 ___. T02 |vertex2
            #         /          T3 !________________! T5          \

            # ## ## determining the order of points on the coordinate plane
            sides_of_the_rectangle = []
            specified = False
            if T3[0] > T4[0] > T5[0] > T6[0]:
                if T4[1] > T3[1] > T6[1] > T5[1]:
                    sides_of_the_rectangle = [(T5, T3), (T3, T4), (T4, T6), (T6, T5)]
                else:
                    sides_of_the_rectangle = [(T6, T4), (T4, T3), (T3, T5), (T5, T6)]
                specified = True

            if T5[1] > T6[1] > T3[1] > T4[1]:
                if T3[0] > T4[0] > T5[0] > T6[0]:
                    sides_of_the_rectangle = [(T6, T4), (T4, T3), (T3, T5), (T5, T6)]
                else:
                    sides_of_the_rectangle = [(T5, T3), (T3, T4), (T4, T6), (T6, T5)]
                specified = True

            if not specified:
                sides_of_the_rectangle = [(T6, T4), (T4, T3), (T3, T5), (T5, T6)]

            # for side in sides_of_the_rectangle:
            #     pygame.draw.aaline(self.display, (255, 255, 0), side[0], side[1])  # yellow

            Ds = [0, 0, 0, 0]
            for side in sides_of_the_rectangle:
                Ds[sides_of_the_rectangle.index(side)] = (side[1][0] - side[0][0]) * (position[1] - side[0][1]) - \
                                                         (position[0] - side[0][0]) * (side[1][1] - side[0][1])
                # D = (x2 - x1) * (yp - y1) - (xp - x1) * (y2 - y1)
                # If D > 0, the point is on the left-hand side.
                # If D < 0, the point is on the right-hand side.
                # If D = 0, the point is on the line.
            if (min(Ds) <= 0 and max(Ds) <= 0) or (min(Ds) >= 0 and max(Ds) >= 0):
                return edge

    def check_buttons_intersection(self, position):
        for button in self.buttons:
            if button["button"].check_intersection(position):
                return button
        return None

    # ## MAIN
    class Camera:
        def __init__(self):
            self.move_shift_start = [0, 0]
            self.move_shift_finish = [0, 0]

            self.position = [0, 0]
            self.move_state = False

            self.scale = 1
            self.borders = [0, 0, 0, 0]

        def set_borders(self, borders):
            self.borders = borders

        def change_scale(self, percent):
            self.scale += percent
            self.scale = 2 if self.scale > 2 else self.scale
            self.scale = 0.1 if self.scale < 0.1 else self.scale

        def reset_shift(self):
            self.move_shift_start = [0, 0]
            self.move_shift_finish = [0, 0]

        def set_shift(self, shift_start, shift_finish):
            self.move_shift_start = shift_start
            self.move_shift_finish = shift_finish

        def recalculate_position(self):
            shift_x = (self.move_shift_finish[0] - self.move_shift_start[0]) / self.scale
            shift_y = (self.move_shift_finish[1] - self.move_shift_start[1]) / self.scale
            self.position[0] += shift_x
            self.position[1] += shift_y

            # ## graph borders with
            # X
            if self.position[0] > self.borders[0]:
                self.position[0] = self.borders[0]
            elif self.position[0] < self.borders[1]:
                self.position[0] = self.borders[1]
            # Y
            if self.position[1] > self.borders[2]:
                self.position[1] = self.borders[2]
            elif self.position[1] < self.borders[3]:
                self.position[1] = self.borders[3]

    # settings are not available yet
    class Settings:
        def __init__(self):
            self.background_start_pos_x = 0
            self.background_start_pos_y = 0
            self.background_width = 500
            self.background_height = 500
            #
            self.edges_width = 8
            self.loop_edge_radius = 25
            self.vertexes_radius = 8
            self.graph_scale = 1
            self.arrow_size = 8
            #
            self.info_padding = 5
            self.info_margin_vertical = 3
            self.info_margin_horizontal = 6
            self.info_main_size = 18
            self.info_additional_size = 18
            #
            self.text_size = 18

    def render_background(self):
        self.display.fill(self.theme.BG_COLOR)

        if self.graph is None:
            return

        if len(self.graph.borders) >= 4:
            x1 = (self.graph.borders[0] + self.camera.position[0]) * self.camera.scale
            x2 = (self.graph.borders[1] + self.camera.position[0]) * self.camera.scale
            y1 = (self.graph.borders[2] + self.camera.position[1]) * self.camera.scale
            y2 = (self.graph.borders[3] + self.camera.position[1]) * self.camera.scale
        else:
            x1 = x2 = self.camera.position[0] * self.camera.scale
            y1 = y2 = self.camera.position[1] * self.camera.scale

        uneven_border_width = 15
        cell_size = 20
        count_x = math.ceil((x2 - x1) / cell_size)
        count_y = math.ceil((y2 - y1) / cell_size)
        x2 = x1 + count_x * cell_size + uneven_border_width
        y2 = y1 + count_y * cell_size + uneven_border_width
        x1 -= uneven_border_width
        y1 -= uneven_border_width

        for i in range(count_x + 1):
            x = x1 + uneven_border_width + i * cell_size
            pygame.draw.aalines(self.display, self.theme.GRID_COLOR, True, [(x, y1), (x, y2)])

        for i in range(count_y + 1):
            y = y1 + uneven_border_width + i * cell_size
            pygame.draw.aalines(self.display, self.theme.GRID_COLOR, True, [(x1, y), (x2, y)])

    def render_edges(self):
        if self.graph is None:
            return

        self.edge_show_info = None
        for edge in self.graph.edges:
            if edge.show_info:
                self.edge_show_info = edge
            color_to_draw = self.theme.EDGE_COLOR_ACTIVE if edge.active else self.theme.EDGE_COLOR
            if edge.color is not None:
                color_to_draw = edge.color
            # ##
            vertex_first = self.graph.get_vertex_by_identifier(edge.vertex_identifier_first)
            vertex_second = self.graph.get_vertex_by_identifier(edge.vertex_identifier_second)

            vertex_first_position_to_draw = [0, 0]
            vertex_first_position_to_draw[0] = (vertex_first.position[0] + self.camera.position[0]) * self.camera.scale
            vertex_first_position_to_draw[1] = (vertex_first.position[1] + self.camera.position[1]) * self.camera.scale
            vertex_second_position_to_draw = [0, 0]
            vertex_second_position_to_draw[0] = (vertex_second.position[0] + self.camera.position[0]) * self.camera.scale
            vertex_second_position_to_draw[1] = (vertex_second.position[1] + self.camera.position[1]) * self.camera.scale

            # ## loops
            loop_radius = self.setting.loop_edge_radius * self.camera.scale
            if edge.vertex_identifier_first == edge.vertex_identifier_second:
                pygame.draw.circle(self.display, color_to_draw,
                                   (vertex_first_position_to_draw[0],
                                    vertex_first_position_to_draw[1] - loop_radius),
                                   loop_radius, self.setting.edges_width)
                continue

            # ## simple edges
            pygame.draw.aaline(self.display, color_to_draw,
                               vertex_first_position_to_draw, vertex_second_position_to_draw)

            if edge.oriented:
                # vertex_second.position
                T0 = vertex_second_position_to_draw
                T23 = [0, 0]
                T1 = [0, 0]
                T2 = [0, 0]
                T3 = [0, 0]

                # it's fine
                distance_between_vertexes = \
                    sqrt((abs(vertex_first_position_to_draw[0] - vertex_second_position_to_draw[0]) ** 2) +
                         (abs(vertex_first_position_to_draw[1] - vertex_second_position_to_draw[1]) ** 2))

                # SCVA is scale coefficient vertex arrow [between center and edge of vertex]
                SCVA = self.setting.vertexes_radius / distance_between_vertexes
                dist_x_between_T1_T0 = \
                    (abs(vertex_first_position_to_draw[0] - vertex_second_position_to_draw[0])) * SCVA
                dist_y_between_T1_T0 = \
                    (abs(vertex_first_position_to_draw[1] - vertex_second_position_to_draw[1])) * SCVA

                T1[0] = T0[0] - dist_x_between_T1_T0 \
                    if vertex_first_position_to_draw[0] < vertex_second_position_to_draw[0] \
                    else T0[0] + dist_x_between_T1_T0
                T1[1] = T0[1] - dist_y_between_T1_T0 \
                    if vertex_first_position_to_draw[1] < vertex_second_position_to_draw[1] \
                    else T0[1] + dist_y_between_T1_T0

                ####### # fine
                scale_coefficient = self.setting.arrow_size / distance_between_vertexes
                dist_x_between_T1_T23 = \
                    (abs(vertex_first_position_to_draw[0] - vertex_second_position_to_draw[0])) * scale_coefficient
                dist_y_between_T1_T23 = \
                    (abs(vertex_first_position_to_draw[1] - vertex_second_position_to_draw[1])) * scale_coefficient

                T23[0] = T1[0] - dist_x_between_T1_T23 \
                    if vertex_first_position_to_draw[0] < vertex_second_position_to_draw[0] \
                    else T1[0] + dist_x_between_T1_T23
                T23[1] = T1[1] - dist_y_between_T1_T23 \
                    if vertex_first_position_to_draw[1] < vertex_second_position_to_draw[1] \
                    else T1[1] + dist_y_between_T1_T23

                dist_x_between_T23_T2_and_T3 = dist_y_between_T1_T23 / 2
                dist_y_between_T23_T2_and_T3 = dist_x_between_T1_T23 / 2

                T2[0] = T23[0] - dist_x_between_T23_T2_and_T3 \
                    if vertex_first_position_to_draw[0] < vertex_second_position_to_draw[0] \
                    else T23[0] + dist_x_between_T23_T2_and_T3
                T2[1] = T23[1] + dist_y_between_T23_T2_and_T3 \
                    if vertex_first_position_to_draw[1] < vertex_second_position_to_draw[1] \
                    else T23[1] - dist_y_between_T23_T2_and_T3

                T3[0] = T23[0] + dist_x_between_T23_T2_and_T3 \
                    if vertex_first_position_to_draw[0] < vertex_second_position_to_draw[0] \
                    else T23[0] - dist_x_between_T23_T2_and_T3
                T3[1] = T23[1] - dist_y_between_T23_T2_and_T3 \
                    if vertex_first_position_to_draw[1] < vertex_second_position_to_draw[1] \
                    else T23[1] + dist_y_between_T23_T2_and_T3

                T2[0] = int(T2[0])
                T2[1] = int(T2[1])
                T3[0] = int(T3[0])
                T3[1] = int(T3[1])
                pygame.draw.polygon(self.display, color_to_draw, [T1, T2, T3])
                pygame.draw.aalines(self.display, color_to_draw, True, [T1, T2, T3])

                #       vertex_second
                #       .T1
                #      /|\
                #     / | \
                #    /  |  \
                # T2.___.___.T3
                #       |T23
                #       |
                #      vertex_first

    def render_vertexes(self):
        if self.graph is None:
            return

        self.vertex_show_info = None
        for vertex in self.graph.vertexes:
            # ## color
            if vertex.show_info:
                self.vertex_show_info = vertex
            AREA_COLOR_LOCAL = self.theme.AREA_COLOR_ACTIVE if vertex.active else self.theme.AREA_COLOR
            CIRCLE_COLOR_LOCAL = self.theme.CIRCLE_COLOR_ACTIVE if vertex.active else self.theme.CIRCLE_COLOR
            if vertex.color is not None:
                CIRCLE_COLOR_LOCAL = vertex.color

            # ## circle
            vertex_position_to_draw = [0, 0]
            vertex_position_to_draw[0] = (vertex.position[0] + self.camera.position[0]) * self.camera.scale
            vertex_position_to_draw[1] = (vertex.position[1] + self.camera.position[1]) * self.camera.scale

            pygame.draw.circle(self.display, AREA_COLOR_LOCAL,
                               (vertex_position_to_draw[0], vertex_position_to_draw[1]),
                               self.setting.vertexes_radius)
            pygame.draw.circle(self.display, CIRCLE_COLOR_LOCAL,
                               (vertex_position_to_draw[0], vertex_position_to_draw[1]),
                               self.setting.vertexes_radius, 1)
            # ## identifier
            font = pygame.font.Font(self.theme.FONT, self.setting.vertexes_radius * 2)
            vertex_identifier = font.render(vertex.identifier, True, CIRCLE_COLOR_LOCAL)

            vertex_identifier_x = vertex_position_to_draw[0] + self.setting.vertexes_radius
            vertex_identifier_y = vertex_position_to_draw[1] + self.setting.vertexes_radius
            if vertex_identifier_x + vertex_identifier.get_width() > self.display.get_width():
                vertex_identifier_x -= (self.setting.vertexes_radius * 2 + vertex_identifier.get_width())
            if vertex_identifier_y + vertex_identifier.get_height() > self.display.get_height():
                vertex_identifier_y -= (self.setting.vertexes_radius * 2 + vertex_identifier.get_height())
            self.display.blit(vertex_identifier, (vertex_identifier_x, vertex_identifier_y))

    def render_selected_area(self):
        if self.selected_area != {"x1": 0, "y1": 0, "x2": 0, "y2": 0}:
            width = abs(self.selected_area["x1"] - self.selected_area["x2"])
            height = abs(self.selected_area["y1"] - self.selected_area["y2"])
            position_x = self.selected_area["x1"] if self.selected_area["x1"] < self.selected_area["x2"] else self.selected_area["x2"]
            position_y = self.selected_area["y1"] if self.selected_area["y1"] < self.selected_area["y2"] else self.selected_area["y2"]

            rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            color = list(self.theme.GRID_COLOR)
            color.append(96)
            rect_surface.fill(tuple(color))
            pygame.draw.rect(self.display, self.theme.BUTTON_COLOR_TEXT, (position_x, position_y, width, height), 1)
            self.display.blit(rect_surface, (position_x, position_y))

    def render_info(self):
        # ## ### VERTEX INFO
        if self.vertex_show_info is not None:
            vertex = self.vertex_show_info
            vertex_position_to_draw = [0, 0]
            vertex_position_to_draw[0] = (vertex.position[0] + self.camera.position[0]) * self.camera.scale
            vertex_position_to_draw[1] = (vertex.position[1] + self.camera.position[1]) * self.camera.scale
            font = pygame.font.Font(self.theme.FONT, int(self.setting.vertexes_radius * 1.5))
            texts_to_draw = list()
            vertex_degree = 0
            for edge in self.graph.edges:
                if edge.vertex_identifier_first == vertex.identifier or \
                        edge.vertex_identifier_second == vertex.identifier:
                    if edge.oriented:
                        text = f"({edge.vertex_identifier_first})-" \
                               f"-[{edge.identifier}]->({edge.vertex_identifier_second})"
                    else:
                        text = f"({edge.vertex_identifier_first})-" \
                               f"-[{edge.identifier}]--({edge.vertex_identifier_second})"

                    texts_to_draw.append(font.render(text, True, self.theme.BUTTON_COLOR_TEXT))
                    vertex_degree += 1 if edge.vertex_identifier_first != edge.vertex_identifier_second else 2
            # degree
            texts_to_draw.insert(0, font.render(f"degree: {vertex_degree}", True, self.theme.BUTTON_COLOR_TEXT))
            # content
            texts_to_draw.insert(0, font.render(f"content: {vertex.content}", True, self.theme.BUTTON_COLOR_TEXT))
            # vertex
            texts_to_draw.insert(0, font.render(f"y:{str(vertex.position[1])}", True, self.theme.BUTTON_COLOR_TEXT))
            texts_to_draw.insert(0, font.render(f"x:{str(vertex.position[0])}", True, self.theme.BUTTON_COLOR_TEXT))
            texts_to_draw.insert(0, font.render(f"vertex: {vertex.identifier}", True, self.theme.BUTTON_COLOR_TEXT))

            # ## draw bg
            # calculate sizes
            max_width_of_text = 0
            for text in texts_to_draw:
                if text.get_width() >= max_width_of_text:
                    max_width_of_text = text.get_width()
            sum_height_of_text = 0
            for text in texts_to_draw:
                sum_height_of_text += text.get_height()

            # ## VERTEX CONTENT AS IMG
            try:
                img = pygame.image.load(str(vertex.content))
                img_width = img.get_width()
                img_height = img.get_height()
                img = pygame.transform.scale(img, (max_width_of_text, img_height * (max_width_of_text / img_width)))
                texts_to_draw.insert(1, img)
                sum_height_of_text += img.get_height()
            except Exception as _:
                pass

            bg_width = max_width_of_text + self.setting.info_margin_horizontal * 2
            bg_height = sum_height_of_text + self.setting.info_margin_vertical * 2 * (len(texts_to_draw) + 1)
            # calculate position
            position_x = vertex_position_to_draw[0] + self.setting.vertexes_radius
            position_y = vertex_position_to_draw[1] + self.setting.vertexes_radius
            if position_x + bg_width > self.display.get_width():
                position_x -= (self.setting.vertexes_radius * 2 + bg_width)
            if position_y + bg_height > self.display.get_height():
                position_y -= (self.setting.vertexes_radius * 2 + bg_height)
            # draw bg
            bg_rectangle = (position_x, position_y, bg_width, bg_height)
            pygame.draw.rect(self.display, self.theme.BUTTON_COLOR_AREA, bg_rectangle)
            pygame.draw.rect(self.display, self.theme.BUTTON_COLOR_TEXT, bg_rectangle, 1)

            # draw text
            for text in texts_to_draw:
                text_x = position_x + self.setting.info_margin_horizontal
                text_y = position_y + self.setting.info_margin_vertical
                for text_ in texts_to_draw:
                    text_y += self.setting.info_margin_vertical
                    if text_ != text:
                        text_y += text_.get_height() + self.setting.info_margin_vertical
                    else:
                        break
                self.display.blit(text, (text_x, text_y))

        # ## ### EDGE INFO
        if self.edge_show_info is not None:
            edge = self.edge_show_info

            vertex_first = self.graph.get_vertex_by_identifier(edge.vertex_identifier_first)
            vertex_second = self.graph.get_vertex_by_identifier(edge.vertex_identifier_second)
            font = pygame.font.Font(self.theme.FONT, int(self.setting.vertexes_radius * 1.5))

            vertex_first_position_to_draw = [0, 0]
            vertex_first_position_to_draw[0] = (vertex_first.position[0] + self.camera.position[0]) * self.camera.scale
            vertex_first_position_to_draw[1] = (vertex_first.position[1] + self.camera.position[1]) * self.camera.scale
            vertex_second_position_to_draw = [0, 0]
            vertex_second_position_to_draw[0] = (vertex_second.position[0] + self.camera.position[0]) * self.camera.scale
            vertex_second_position_to_draw[1] = (vertex_second.position[1] + self.camera.position[1]) * self.camera.scale

            T1 = vertex_first_position_to_draw
            T2 = vertex_second_position_to_draw
            T3 = [0, 0]

            dist_x_between_T1_T2 = (abs(T1[0] - T2[0]))
            dist_y_between_T1_T2 = (abs(T1[1] - T2[1]))

            T3[0] = T1[0] - dist_x_between_T1_T2 / 2 \
                if vertex_first_position_to_draw[0] > vertex_second_position_to_draw[0] \
                else T1[0] + dist_x_between_T1_T2 / 2
            T3[1] = T1[1] + dist_y_between_T1_T2 / 2 \
                if vertex_first_position_to_draw[1] < vertex_second_position_to_draw[1] \
                else T1[1] - dist_y_between_T1_T2 / 2

            texts_to_draw = list()
            # vertex - edge - vertex
            if edge.oriented:
                text = f"({edge.vertex_identifier_first})-" \
                       f"-[{edge.identifier}]->({edge.vertex_identifier_second})"
            else:
                text = f"({edge.vertex_identifier_first})-" \
                       f"-[{edge.identifier}]--({edge.vertex_identifier_second})"

            texts_to_draw.append(font.render(text, True, self.theme.BUTTON_COLOR_TEXT))
            # edge
            texts_to_draw.insert(0, font.render(f"edge: {edge.identifier}", True, self.theme.BUTTON_COLOR_TEXT))
            texts_to_draw.append(font.render(f"weight: {edge.weight}", True, self.theme.BUTTON_COLOR_TEXT))
            texts_to_draw.append(font.render(f"oriented: {edge.oriented}", True, self.theme.BUTTON_COLOR_TEXT))

            # ## draw bg
            # calculate sizes
            max_width_of_text = 0
            for text in texts_to_draw:
                if text.get_width() >= max_width_of_text:
                    max_width_of_text = text.get_width()
            sum_height_of_text = 0
            for text in texts_to_draw:
                sum_height_of_text += text.get_height()

            bg_width = max_width_of_text + self.setting.info_margin_horizontal * 2
            bg_height = sum_height_of_text + self.setting.info_margin_vertical * 2 * (len(texts_to_draw) + 1)
            # calculate position
            position_x = (edge.show_info_position[0] + self.camera.position[0]) * self.camera.scale
            position_y = (edge.show_info_position[1] + self.camera.position[1]) * self.camera.scale
            if position_x + bg_width > self.display.get_width():
                position_x -= (self.setting.vertexes_radius * 2 + bg_width)
            if position_y + bg_height > self.display.get_height():
                position_y -= (self.setting.vertexes_radius * 2 + bg_height)
            # draw bg
            bg_rectangle = (position_x, position_y, bg_width, bg_height)
            pygame.draw.rect(self.display, self.theme.BUTTON_COLOR_AREA, bg_rectangle)
            pygame.draw.rect(self.display, self.theme.BUTTON_COLOR_TEXT, bg_rectangle, 1)
            # draw text
            for text in texts_to_draw:
                text_x = position_x + self.setting.info_margin_horizontal
                text_y = position_y + self.setting.info_margin_vertical
                for text_ in texts_to_draw:
                    text_y += self.setting.info_margin_vertical
                    if text_ != text:
                        text_y += text_.get_height() + self.setting.info_margin_vertical
                    else:
                        break
                self.display.blit(text, (text_x, text_y))

    def render_buttons(self):
        self.button_show_info = None
        for button in self.buttons:
            if button["button"].show_info:
                self.button_show_info = button
            try:
                button["button"].render()
            except Exception as ex:
                print(ex)

        if self.button_show_info:
            font = pygame.font.Font(self.theme.FONT, int(self.setting.vertexes_radius * 1.5))
            lines = self.button_show_info['button'].info
            if len(lines) <= 0:
                return

            texts_to_draw = []
            for line in lines:
                texts_to_draw.append(font.render(f"{line}", True, self.theme.BUTTON_COLOR_TEXT))

            max_width_of_text = 0
            for text in texts_to_draw:
                if text.get_width() >= max_width_of_text:
                    max_width_of_text = text.get_width()
            sum_height_of_text = 0
            for text in texts_to_draw:
                sum_height_of_text += text.get_height()

            bg_width = max_width_of_text + self.setting.info_margin_horizontal * 2
            bg_height = sum_height_of_text + self.setting.info_margin_vertical * 2 * (len(texts_to_draw) + 1)
            # calculate position
            position_x = self.button_show_info["button"].position[0] + self.button_show_info["button"].width - 20
            position_y = self.button_show_info["button"].position[1] + self.button_show_info["button"].height / 2
            if position_x + bg_width > self.display.get_width():
                position_x -= bg_width + self.button_show_info["button"].width
            if position_y + bg_height > self.display.get_height():
                position_y -= bg_height
            # draw bg
            bg_rectangle = (position_x, position_y, bg_width, bg_height)
            pygame.draw.rect(self.display, self.theme.BUTTON_COLOR_AREA, bg_rectangle)
            pygame.draw.rect(self.display, self.theme.BUTTON_COLOR_TEXT, bg_rectangle, 1)

            # draw text
            for text in texts_to_draw:
                text_x = position_x + self.setting.info_margin_horizontal
                text_y = position_y + self.setting.info_margin_vertical
                for text_ in texts_to_draw:
                    text_y += self.setting.info_margin_vertical
                    if text_ != text:
                        text_y += text_.get_height() + self.setting.info_margin_vertical
                    else:
                        break
                self.display.blit(text, (text_x, text_y))

    def render(self):
        if self.display is None:
            raise Exception("No display in graph renderer")

        self.render_background()
        self.render_edges()
        self.render_vertexes()
        self.render_selected_area()
        self.render_info()
        self.render_buttons()

        pygame.display.flip()
