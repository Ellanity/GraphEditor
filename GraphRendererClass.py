from math import sqrt
import pygame
from ThemeClass import OrangeDarkTheme, BlueLightTheme

FONT = "CONSOLA.ttf"


class GraphRenderer:
    def __init__(self, display=None, graph=None):
        self.display = display
        self.setting = self.Settings()
        self.camera = self.Camera()
        self.graph = graph
        # ## theme
        self.light_theme = BlueLightTheme()
        self.dark_theme = OrangeDarkTheme()
        self.theme = self.light_theme
        # ## buttons in future
        self.info_location = [0, 0, 0, 0]  # x y width height

    class Camera:
        def __init__(self):
            self.move_shift_start = [0, 0]
            self.move_shift_finish = [0, 0]

            self.position = [0, 0]
            self.move_state = False

        def reset_shift(self):
            self.move_shift_start = [0, 0]
            self.move_shift_finish = [0, 0]

        def set_shift(self, shift_start, shift_finish):
            self.move_shift_start = shift_start
            self.move_shift_finish = shift_finish

        def recalculate_position(self):
            shift_x = self.move_shift_finish[0] - self.move_shift_start[0]
            shift_y = self.move_shift_finish[1] - self.move_shift_start[1]
            self.position[0] += shift_x
            self.position[1] += shift_y

    # settings are not available yet
    class Settings:
        def __init__(self):
            self.background_start_pos_x = 0
            self.background_start_pos_y = 0
            self.background_width = 500
            self.background_height = 500
            #
            self.edges_width = 2
            self.vertexes_radius = 8
            self.graph_scale = 1
            self.arrow_size = 8
            #
            self.info_padding = 5
            self.info_margin_vertical = 3
            self.info_margin_horizontal = 6
            self.info_main_size = 18
            self.info_additional_size = 18

    def set_graph(self, graph):
        self.graph = graph

    def set_display(self, display):
        self.display = display

    def render_background(self):
        self.display.fill(self.theme.BG_COLOR)

    def render_edges(self):
        for edge in self.graph.edges:
            color_to_draw = self.theme.EDGE_COLOR if edge.color is None else edge.color
            # ##
            vertex_first = self.graph.get_vertex_by_identifier(edge.vertex_identifier_first)
            vertex_second = self.graph.get_vertex_by_identifier(edge.vertex_identifier_second)

            vertex_first_position_to_draw = [0, 0]
            vertex_first_position_to_draw[0] = vertex_first.position[0] + self.camera.position[0]
            vertex_first_position_to_draw[1] = vertex_first.position[1] + self.camera.position[1]
            vertex_second_position_to_draw = [0, 0]
            vertex_second_position_to_draw[0] = vertex_second.position[0] + self.camera.position[0]
            vertex_second_position_to_draw[1] = vertex_second.position[1] + self.camera.position[1]

            pygame.draw.aaline(self.display, color_to_draw,
                               vertex_first_position_to_draw, vertex_second_position_to_draw)

            if edge.oriented:
                # vertex_second.position
                T0 = vertex_second_position_to_draw
                T23 = [0, 0]
                T1 = [0, 0]
                T2 = [0, 0]
                T3 = [0, 0]

                # it's fine too
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
            vertex_position_to_draw = [0, 0]
            vertex_position_to_draw[0] = vertex.position[0] + self.camera.position[0]
            vertex_position_to_draw[1] = vertex.position[1] + self.camera.position[1]

            if (position[0] - vertex_position_to_draw[0]) ** 2 + (position[1] - vertex_position_to_draw[1]) ** 2 \
                    < self.setting.vertexes_radius ** 2:
                return vertex
        return None

    def change_theme(self):
        if type(self.theme) == OrangeDarkTheme:
            self.theme = self.light_theme
        else:
            self.theme = self.dark_theme

    def info_intersection(self, position):
        if self.info_location[0] < position[0] < self.info_location[0] + self.info_location[2] and \
                self.info_location[1] < position[1] < self.info_location[1] + self.info_location[3]:
            return True
        return False

    # make more buttons (not only info) in future
    class Button(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = None
            self.rect = None
            self.position_x = 0
            self.position_y = 0
            self.type_ = str()

        def set_image(self, image):
            self.image = image
            self.recalculate_the_rect()

        def recalculate_the_rect(self):
            self.rect = pygame.Rect(self.position_x, self.position_y, self.image.get_width(), self.image.get_height())

    def render_vertexes(self):
        for vertex in self.graph.vertexes:
            # ## color
            AREA_COLOR_LOCAL = self.theme.ACTIVE_AREA_COLOR if vertex.active else self.theme.AREA_COLOR
            CIRCLE_COLOR_LOCAL = self.theme.ACTIVE_CIRCLE_COLOR if vertex.active else self.theme.CIRCLE_COLOR
            if vertex.color is not None:
                CIRCLE_COLOR_LOCAL = vertex.color

            # ## circle
            vertex_position_to_draw = [0, 0]
            vertex_position_to_draw[0] = vertex.position[0] + self.camera.position[0]
            vertex_position_to_draw[1] = vertex.position[1] + self.camera.position[1]

            pygame.draw.circle(self.display, AREA_COLOR_LOCAL,
                               (vertex_position_to_draw[0], vertex_position_to_draw[1]),
                               self.setting.vertexes_radius)
            pygame.draw.circle(self.display, CIRCLE_COLOR_LOCAL,
                               (vertex_position_to_draw[0], vertex_position_to_draw[1]),
                               self.setting.vertexes_radius, 1)
            # ## identifier
            font = pygame.font.Font(FONT, self.setting.vertexes_radius * 2)
            vertex_identifier = font.render(vertex.identifier, True, CIRCLE_COLOR_LOCAL)

            vertex_identifier_x = vertex_position_to_draw[0] + self.setting.vertexes_radius
            vertex_identifier_y = vertex_position_to_draw[1] + self.setting.vertexes_radius
            if vertex_identifier_x + vertex_identifier.get_width() > self.display.get_width():
                vertex_identifier_x -= (self.setting.vertexes_radius * 2 + vertex_identifier.get_width())
            if vertex_identifier_y + vertex_identifier.get_height() > self.display.get_height():
                vertex_identifier_y -= (self.setting.vertexes_radius * 2 + vertex_identifier.get_height())
            self.display.blit(vertex_identifier, (vertex_identifier_x, vertex_identifier_y))

    def render_graph_info(self):
        # ## create texts with info
        font_main = pygame.font.Font(FONT, self.setting.info_main_size)
        font_additional = pygame.font.Font(FONT, self.setting.info_additional_size)
        # graph name
        texts_to_draw = list()
        texts_to_draw.append(font_main.render(f"Graph: {self.graph.identifier}",
                                              True, self.theme.INFO_TEXT_COLOR))  # graph_identifier
        texts_to_draw.append(font_additional.render(f"Vertexes: {len(self.graph.vertexes)}",
                                                    True, self.theme.INFO_TEXT_COLOR))  # vertexes_count
        texts_to_draw.append(font_additional.render(f"Edges: {len(self.graph.edges)}",
                                                    True, self.theme.INFO_TEXT_COLOR))  # edges_count

        # ## draw bg
        max_width_of_text = 0
        for text in texts_to_draw:
            if text.get_width() >= max_width_of_text:
                max_width_of_text = text.get_width()
        sum_height_of_text = 0
        for text in texts_to_draw:
            sum_height_of_text += text.get_height()

        bg_width = max_width_of_text + self.setting.info_margin_horizontal * 2
        bg_height = sum_height_of_text + self.setting.info_margin_vertical * 2 * (len(texts_to_draw) + 1)
        self.info_location = [self.setting.info_padding, self.setting.info_padding, bg_width, bg_height]
        bg_rectangle = (self.setting.info_padding, self.setting.info_padding, bg_width, bg_height)
        pygame.draw.rect(self.display, self.theme.INFO_AREA_COLOR, bg_rectangle)
        pygame.draw.rect(self.display, self.theme.INFO_TEXT_COLOR, bg_rectangle, 1)
        # ## find location of texts
        for text in texts_to_draw:
            text_x = self.setting.info_padding + self.setting.info_margin_horizontal
            text_y = self.setting.info_padding + self.setting.info_margin_vertical
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
        if self.graph is None:
            raise Exception("No graph in graph renderer")

        self.render_background()
        self.render_edges()
        self.render_vertexes()
        self.render_graph_info()

        pygame.display.flip()
