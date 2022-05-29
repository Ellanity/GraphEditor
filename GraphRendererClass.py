from math import sqrt

import pygame

AREA_COLOR = BG_COLOR = (240, 245, 255)
ACTIVE_CIRCLE_COLOR = (32, 79, 206)
ACTIVE_AREA_COLOR = (176, 194, 242)
CIRCLE_COLOR = (0, 0, 0)
EDGE_COLOR = (0, 0, 0)


class GraphRenderer:
    def __init__(self, display=None, clock=None, graph=None):
        self.display = display
        self.clock = clock
        self.graph = graph
        self.setting = self.Settings()

    # settings are not available yet
    class Settings:
        def __init__(self):
            self.background_start_pos_x = 0
            self.background_start_pos_y = 0
            self.background_width = 500
            self.background_height = 500
            self.edges_width = 2
            self.vertexes_radius = 8
            self.graph_scale = 1
            self.arrow_size = 8

    def set_graph(self, graph):
        self.graph = graph

    def set_display(self, display):
        self.display = display

    def set_clock(self, clock):
        self.clock = clock

    def render_background(self):
        self.display.fill(BG_COLOR)

    def render_edges(self):
        for edge in self.graph.edges:
            vertex_first = self.graph.get_vertex_by_identifier(edge.vertex_identifier_first)
            vertex_second = self.graph.get_vertex_by_identifier(edge.vertex_identifier_second)
            # print(edge.identifier, vertex_first.position, vertex_second.position, EDGE_COLOR )
            pygame.draw.aaline(self.display, EDGE_COLOR, vertex_first.position, vertex_second.position)

            if edge.oriented:
                # print(edge.identifier)
                # vertex_second.position
                T0 = vertex_second.position
                T23 = [0, 0]
                T1 = [0, 0]
                T2 = [0, 0]
                T3 = [0, 0]

                # it's fine too
                distance_between_vertexes = sqrt((abs(vertex_first.position[0] - vertex_second.position[0]) ** 2) +
                                                 (abs(vertex_first.position[1] - vertex_second.position[1]) ** 2))

                # SCVA is scale coefficient vertex arrow [between center and edge of vertex]
                SCVA = self.setting.vertexes_radius / distance_between_vertexes
                dist_x_between_T1_T0 = (abs(vertex_first.position[0] - vertex_second.position[0])) * SCVA
                dist_y_between_T1_T0 = (abs(vertex_first.position[1] - vertex_second.position[1])) * SCVA

                T1[0] = T0[0] - dist_x_between_T1_T0 if vertex_first.position[0] < vertex_second.position[0] \
                    else T0[0] + dist_x_between_T1_T0
                T1[1] = T0[1] - dist_y_between_T1_T0 if vertex_first.position[1] < vertex_second.position[1] \
                    else T0[1] + dist_y_between_T1_T0

                ####### # fine
                scale_coefficient = self.setting.arrow_size / distance_between_vertexes
                dist_x_between_T1_T23 = (abs(vertex_first.position[0] - vertex_second.position[0])) * scale_coefficient
                dist_y_between_T1_T23 = (abs(vertex_first.position[1] - vertex_second.position[1])) * scale_coefficient

                T23[0] = T1[0] - dist_x_between_T1_T23 if vertex_first.position[0] < vertex_second.position[0] \
                    else T1[0] + dist_x_between_T1_T23
                T23[1] = T1[1] - dist_y_between_T1_T23 if vertex_first.position[1] < vertex_second.position[1] \
                    else T1[1] + dist_y_between_T1_T23
                # print("T0: ", vertex_first.position, "T1: ", T1, "DISTxy: ",
                # dist_x_between_T1_T23, dist_y_between_T1_T23, "T23: ", T23)

                dist_x_between_T23_T2_and_T23_T3 = dist_y_between_T1_T23 / 2
                dist_y_between_T23_T2_and_T23_T3 = dist_x_between_T1_T23 / 2

                T2[0] = T23[0] - dist_x_between_T23_T2_and_T23_T3 if vertex_first.position[0] \
                                                                     < vertex_second.position[0] \
                    else T23[0] + dist_x_between_T23_T2_and_T23_T3
                T2[1] = T23[1] + dist_y_between_T23_T2_and_T23_T3 if vertex_first.position[1] \
                                                                     < vertex_second.position[1] \
                    else T23[1] - dist_y_between_T23_T2_and_T23_T3

                T3[0] = T23[0] + dist_x_between_T23_T2_and_T23_T3 if vertex_first.position[0] \
                                                                     < vertex_second.position[0] \
                    else T23[0] - dist_x_between_T23_T2_and_T23_T3
                T3[1] = T23[1] - dist_y_between_T23_T2_and_T23_T3 if vertex_first.position[1] \
                                                                     < vertex_second.position[1] \
                    else T23[1] + dist_y_between_T23_T2_and_T23_T3

                T2[0] = int(T2[0])
                T2[1] = int(T2[1])
                T3[0] = int(T3[0])
                T3[1] = int(T3[1])
                # print("T23: ", T23, "DISTxy: ",
                # dist_x_between_T23_T2_and_T23_T3, dist_y_between_T23_T2_and_T23_T3, "T2: ", T2, "T3: ", T3)
                pygame.draw.polygon(self.display, EDGE_COLOR, [T1, T2, T3])
                pygame.draw.aalines(self.display, EDGE_COLOR, True, [T1, T2, T3])

                #       vertex_second
                #       .T1
                #      /|\
                #     / | \
                #    /  |  \
                # T2.___.___.T3
                #       |T23
                #       |
                #      vertex_first

        """
        pygame.draw.line(sc, WHITE, [10, 30], [290, 15], 3)
        pygame.draw.line(sc, WHITE, [10, 50], [290, 35])
        pygame.draw.aaline(sc, WHITE, [10, 70], [290, 55])
        -----------------------
        pi = 3.14
        pygame.draw.arc(sc, WHITE, (10, 50, 280, 100), 0, pi)
        pygame.draw.arc(sc, PINK, (50, 30, 200, 150), pi, 2*pi, 3)
        """

    def get_vertex_by_position(self, position):
        if self.graph is None:
            return None
        for vertex in self.graph.vertexes:
            if (position[0] - vertex.position[0]) ** 2 + (position[1] - vertex.position[1]) ** 2 \
                    < self.setting.vertexes_radius ** 2:
                return vertex
        return None

    def render_vertexes(self):
        for vertex in self.graph.vertexes:
            # circle
            AREA_COLOR_LOCAL = ACTIVE_AREA_COLOR if vertex.active else AREA_COLOR
            CIRCLE_COLOR_LOCAL = ACTIVE_CIRCLE_COLOR if vertex.active else CIRCLE_COLOR
            pygame.draw.circle(self.display, AREA_COLOR_LOCAL,
                               (vertex.position[0], vertex.position[1]), self.setting.vertexes_radius)
            pygame.draw.circle(self.display, CIRCLE_COLOR_LOCAL,
                               (vertex.position[0], vertex.position[1]), self.setting.vertexes_radius, 1)
            # identifier
            font = pygame.font.Font(None, self.setting.vertexes_radius * 2)
            vertex_identifier = font.render(vertex.identifier, True, CIRCLE_COLOR_LOCAL)

            vertex_identifier_x = vertex.position[0] + self.setting.vertexes_radius
            vertex_identifier_y = vertex.position[1] + self.setting.vertexes_radius
            if vertex_identifier_x + vertex_identifier.get_width() > self.display.get_width():
                vertex_identifier_x -= (self.setting.vertexes_radius * 2 + vertex_identifier.get_width())
            if vertex_identifier_y + vertex_identifier.get_height() > self.display.get_height():
                vertex_identifier_y -= (self.setting.vertexes_radius * 2 + vertex_identifier.get_height())
            self.display.blit(vertex_identifier, (vertex_identifier_x, vertex_identifier_y))

    def render(self):
        if self.display is None:
            raise Exception("No display in graph renderer")
        if self.graph is None:
            raise Exception("No graph in graph renderer")
        if self.clock is None:
            raise Exception("No clock in graph renderer")

        self.render_background()
        self.render_edges()
        self.render_vertexes()

        pygame.display.flip()
