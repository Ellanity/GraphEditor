import math
from math import sqrt
from ThemeClass import OrangeDarkTheme, BlueLightTheme
from CustomButtonClass import *


class GraphRenderer:
    def __init__(self, display=None, graph=None):
        self.display = display
        self.setting = self.Settings()
        self.camera = self.Camera()
        self.graph = graph
        # ## theme
        self.light_theme = BlueLightTheme()
        self.dark_theme = OrangeDarkTheme()
        self.theme = self.dark_theme
        # ## buttons in future
        self.info_location = [0, 0, 0, 0]  # x y width height
        self.buttons = list()
        self.__init_buttons__()

    def set_graph(self, graph):
        self.graph = graph
        camera_borders = [0, 0, 0, 0]
        camera_borders[0] = graph.borders[0] - (self.display.get_width() / self.camera.scale)
        camera_borders[1] = graph.borders[1]
        camera_borders[2] = graph.borders[2] - (self.display.get_height() / self.camera.scale)
        camera_borders[3] = graph.borders[3]
        self.camera.set_borders([-border for border in camera_borders])

    def set_display(self, display):
        self.display = display

    def get_vertex_by_position(self, position):
        if self.graph is None:
            return None
        for vertex in self.graph.vertexes:
            vertex_position_to_draw = [0, 0]
            vertex_position_to_draw[0] = (vertex.position[0] + self.camera.position[0]) * self.camera.scale
            vertex_position_to_draw[1] = (vertex.position[1] + self.camera.position[1]) * self.camera.scale

            # ## (x-a)^2 + (y-b)^2 <= R^2
            xa2 = (((position[0] - vertex_position_to_draw[0]) * self.camera.scale) ** 2)
            yb2 = (((position[1] - vertex_position_to_draw[1]) * self.camera.scale) ** 2)
            r2 = (self.setting.vertexes_radius ** 2) * self.camera.scale
            if xa2 + yb2 < r2:
                return vertex
        return None

    # ## BUTTONS

    def add_button(self, button):
        self.buttons.append(button)

    def delete_button(self, identifier):
        for button in self.buttons:
            if button.identifier == identifier:
                self.buttons.remove(button)
                return

    def __init_buttons__(self):
        # graph info button
        graph_info_button = CustomButton("graph info button", self.display)
        graph_info_button.set_theme(self.theme)
        graph_info_button.position = [5, 5]
        graph_info_button.on_click = self.change_theme
        self.buttons.append(graph_info_button)

    def update_buttons(self):
        self.update_button_graph_info()

    def update_button_graph_info(self):
        if self.graph is None:
            return
        for button in self.buttons:
            if button.identifier == "graph info button":
                # {string, color(r,g,b), size}
                content = list()
                content.append({'string': f"Graph: {self.graph.identifier}"})
                content.append({'string': f"Vertexes: {len(self.graph.vertexes)}"})
                content.append({'string': f"Edges: {len(self.graph.edges)}"})
                button.set_content(content)
                button.display = self.display

    def check_buttons_intersection(self, position):
        for button in self.buttons:
            if button.check_intersection(position):
                return button
        return None

    def change_theme(self):
        if type(self.theme) == OrangeDarkTheme:
            self.theme = self.light_theme
        else:
            self.theme = self.dark_theme

        for button in self.buttons:
            button.set_theme(self.theme)

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
            self.edges_width = 1
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

        x1 = (self.graph.borders[0] + self.camera.position[0]) * self.camera.scale
        x2 = (self.graph.borders[1] + self.camera.position[0]) * self.camera.scale
        y1 = (self.graph.borders[2] + self.camera.position[1]) * self.camera.scale
        y2 = (self.graph.borders[3] + self.camera.position[1]) * self.camera.scale

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
        for edge in self.graph.edges:
            color_to_draw = self.theme.EDGE_COLOR if edge.color is None else edge.color
            # ##
            vertex_first = self.graph.get_vertex_by_identifier(edge.vertex_identifier_first)
            vertex_second = self.graph.get_vertex_by_identifier(edge.vertex_identifier_second)

            vertex_first_position_to_draw = [0, 0]
            vertex_first_position_to_draw[0] = (vertex_first.position[0] + self.camera.position[0]) * self.camera.scale
            vertex_first_position_to_draw[1] = (vertex_first.position[1] + self.camera.position[1]) * self.camera.scale
            vertex_second_position_to_draw = [0, 0]
            vertex_second_position_to_draw[0] = \
                (vertex_second.position[0] + self.camera.position[0]) * self.camera.scale
            vertex_second_position_to_draw[1] = \
                (vertex_second.position[1] + self.camera.position[1]) * self.camera.scale

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

    def render_vertexes(self):
        for vertex in self.graph.vertexes:
            # ## color
            AREA_COLOR_LOCAL = self.theme.ACTIVE_AREA_COLOR if vertex.active else self.theme.AREA_COLOR
            CIRCLE_COLOR_LOCAL = self.theme.ACTIVE_CIRCLE_COLOR if vertex.active else self.theme.CIRCLE_COLOR
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

            if vertex.show_info is True:
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

                        texts_to_draw.append(font.render(text, True, self.theme.BUTTON_TEXT_COLOR))
                        vertex_degree += 1 if edge.vertex_identifier_first != edge.vertex_identifier_second else 2
                texts_to_draw.insert(0, font.render(f"degree: {vertex_degree}", True, self.theme.BUTTON_TEXT_COLOR))
                texts_to_draw.insert(0, font.render(f"content: {vertex.content}", True, self.theme.BUTTON_TEXT_COLOR))
                texts_to_draw.insert(0, font.render(f"vertex: {vertex.identifier}", True, self.theme.BUTTON_TEXT_COLOR))

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
                position_x = vertex_position_to_draw[0] + self.setting.vertexes_radius
                position_y = vertex_position_to_draw[1] + self.setting.vertexes_radius
                if position_x + bg_width > self.display.get_width():
                    position_x -= (self.setting.vertexes_radius * 2 + bg_width)
                if position_y + bg_height > self.display.get_height():
                    position_y -= (self.setting.vertexes_radius * 2 + bg_height)
                # draw bg
                bg_rectangle = (position_x, position_y, bg_width, bg_height)
                pygame.draw.rect(self.display, self.theme.BUTTON_AREA_COLOR, bg_rectangle)
                pygame.draw.rect(self.display, self.theme.BUTTON_TEXT_COLOR, bg_rectangle, 1)
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
        self.update_buttons()
        for button in self.buttons:
            try:
                button.render()
            except Exception as _:
                pass

    def render(self):
        if self.display is None:
            raise Exception("No display in graph renderer")
        if self.graph is None:
            raise Exception("No graph in graph renderer")

        self.render_background()
        self.render_edges()
        self.render_vertexes()
        self.render_buttons()

        pygame.display.flip()
