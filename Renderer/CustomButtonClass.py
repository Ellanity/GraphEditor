import datetime
import random

import pygame


class CustomButton:
    def __init__(self, event_handler):
        # main
        # self.identifier = identifier
        self.event_handler = event_handler
        self.on_click = None
        self.on_press = None
        # additional
        self.position = [0, 0]
        self.font = None
        self.theme = None  # self.event_handler.app.renderer.theme
        self.background_color = (255, 255, 255)
        self.border_color = (0, 0, 0)
        self.text_color = (0, 0, 0)
        self.width = 0
        self.height = 0
        self.content = list()  # list of dicts  {string, color(r,g,b), size}
        self.text_margin_horizontal = 6
        self.text_margin_vertical = 3
        self.padding = 5
        self.text_size = 18

    def check_intersection(self, position):
        if self.position[0] < position[0] < self.position[0] + self.width and \
                self.position[1] < position[1] < self.position[1] + self.height:
            return True
        return False

    def click(self, ):
        if self.on_click is not None:
            self.on_click()

    def press(self):
        if self.on_press is not None:
            self.on_press()

    def set_position(self, position):
        self.position = position

    def add_content(self, content):
        self.content.append(content)

    def set_content(self, content):
        self.content = content

    def set_theme(self, theme):
        self.theme = theme
        self.background_color = theme.BUTTON_COLOR_AREA
        self.border_color = theme.BUTTON_COLOR_TEXT
        self.text_color = theme.BUTTON_COLOR_TEXT
        self.font = theme.FONT

    def render(self):
        self.set_theme(self.event_handler.app.renderer.theme)
        texts_to_draw = list()
        for text in self.content:
            texts_to_draw.append(pygame.font.Font(self.font, self.text_size).render(text['string'],
                                                                                    True, self.text_color))
        # ## draw bg
        max_width_of_text = 0
        for text in texts_to_draw:
            if text.get_width() >= max_width_of_text:
                max_width_of_text = text.get_width()
        sum_height_of_text = 0
        for text in texts_to_draw:
            sum_height_of_text += text.get_height()

        bg_width = max_width_of_text + self.text_margin_horizontal * 2
        bg_height = sum_height_of_text + self.text_margin_vertical * 2 * (len(texts_to_draw) + 1)
        self.width = bg_width
        self.height = bg_height
        bg_rectangle = (self.position[0], self.position[1], bg_width, bg_height)
        pygame.draw.rect(self.event_handler.app.display, self.background_color, bg_rectangle)
        pygame.draw.rect(self.event_handler.app.display, self.border_color, bg_rectangle, 1)
        # ## find location of texts
        for text in texts_to_draw:
            text_x = self.position[0] + self.text_margin_horizontal
            text_y = self.position[1] + self.text_margin_vertical
            for text_ in texts_to_draw:
                text_y += self.text_margin_vertical
                if text_ != text:
                    text_y += text_.get_height() + self.text_margin_vertical
                else:
                    break
            self.event_handler.app.display.blit(text, (text_x, text_y))

    def calculate_height(self):
        height = 5
        last_prefix = ""
        if len(self.event_handler.buttons) > 0:
            last_prefix = str(self.event_handler.buttons[0]["type"]).split(" ")[0]

        for button in self.event_handler.buttons:
            # prefix height
            prefix = str(button["type"]).split(" ")[0]
            if prefix != last_prefix:
                height += 33
            last_prefix = prefix
            # buttons height
            if button["button"] is self:
                break
            height += button["button"].height + 5
        self.position[1] = height

    def update(self):
        pass

    def on_click_self(self):
        pass


class ButtonGraphInfo(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.set_theme(self.event_handler.app.renderer.theme)
        self.on_click = self.event_handler.app.renderer.change_theme
        self.position[0] = 5

    def update(self):
        if self.event_handler.app.store.current_graph is None:
            return
        self.calculate_height()
        content = list()
        content.append({'string': f"Graph: {self.event_handler.app.store.current_graph.identifier}"})
        content.append({'string': f"Vertexes: {len(self.event_handler.app.store.current_graph.vertexes)}"})
        content.append({'string': f"Edges: {len(self.event_handler.app.store.current_graph.edges)}"})
        self.set_content(content)


class ButtonGraphDelete(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.set_theme(self.event_handler.app.renderer.theme)
        self.on_click = self.on_click_self
        self.position[0] = 5
        self.text_size = 16
        self.content = [{'string': f"graph delete"}]

    def update(self):
        if self.event_handler.app.store.current_graph is None:
            return
        self.position[1] = self.event_handler.app.display.get_height() - self.height - 5

    def on_click_self(self):
        self.event_handler.app.store.delete_graph(self.event_handler.app.store.current_graph.identifier)
        self.event_handler.app.renderer.graph = None
        if len(self.event_handler.app.store.graphs) > 0:
            self.event_handler.app.store.current_graph = self.event_handler.app.store.graphs[0]


class ButtonEdgeCreate(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.set_theme(self.event_handler.app.renderer.theme)
        self.text_size = 16
        self.content = [{'string': f"edge create"}]
        self.on_click = self.on_click_self
        self.position[0] = 5

    def update(self):
        self.calculate_height()

    def on_click_self(self):
        if self.event_handler.app.store.current_graph is None:
            return
        vertexes_identifiers_in_subgraph = [vertex.identifier for vertex in
                                            self.event_handler.app.store.current_subgraph_vertexes]

        edges_to_delete = []
        for edge in self.event_handler.app.store.current_graph.edges:
            if edge.vertex_identifier_first in vertexes_identifiers_in_subgraph \
                    and edge.vertex_identifier_second in vertexes_identifiers_in_subgraph:
                edges_to_delete.append(edge)
        for edge in edges_to_delete:
            self.event_handler.app.store.current_graph.delete_edge(edge.identifier)

        connected_vertexes = list()
        for vertex1 in self.event_handler.app.store.current_subgraph_vertexes:
            for vertex2 in self.event_handler.app.store.current_subgraph_vertexes:
                if vertex1.identifier != vertex2.identifier \
                        and vertex1.identifier not in connected_vertexes \
                        and vertex2.identifier not in connected_vertexes:
                    edge_identifier = f"e-{vertex1.identifier}-{vertex2.identifier}-{random.randint(0, 1000000)}"
                    vertex_identifier_first = vertex1.identifier
                    vertex_identifier_second = vertex2.identifier
                    oriented = False
                    self.event_handler.app.store.current_graph.add_edge(
                        identifier=edge_identifier,
                        vertex_identifier_first=vertex_identifier_first,
                        vertex_identifier_second=vertex_identifier_second,
                        oriented=oriented)
            connected_vertexes.append(vertex1.identifier)


class ButtonVertexCreate(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.set_theme(self.event_handler.app.renderer.theme)
        self.text_size = 16
        self.content = [{'string': f"vertex create"}]
        self.on_click = self.on_click_self
        self.position[0] = 5

    def update(self):
        self.calculate_height()

    def on_click_self(self):
        if self.event_handler.app.store.current_graph is None:
            return
        new_vertex_name = f"vertex_{datetime.datetime.now()}-{random.randint(0, 1000000)}".replace(" ", "_")
        content = "content"
        position_on_screen = [0, 0]
        position_on_screen[0] = self.event_handler.app.display.get_width() / 2
        position_on_screen[1] = self.event_handler.app.display.get_height() / 2
        position = [0, 0]
        position[0] = position_on_screen[0] / self.event_handler.app.renderer.camera.scale - self.event_handler.app.renderer.camera.position[0]
        position[1] = position_on_screen[1] / self.event_handler.app.renderer.camera.scale - self.event_handler.app.renderer.camera.position[1]
        self.event_handler.app.store.current_graph.add_vertex(identifier=new_vertex_name, content=content, position=position)


class ButtonGraphCreate(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.set_theme(self.event_handler.app.renderer.theme)
        self.text_size = 16
        self.content = [{'string': f"graph create"}]
        self.on_click = self.on_click_self
        self.position[0] = 5

    def update(self):
        self.calculate_height()

    def on_click_self(self):
        new_graph_name = f"Graph_{datetime.datetime.now()}_{random.randint(0, 1000000)}".replace(" ", "_")
        self.event_handler.app.store.create_graph(identifier=new_graph_name)
        self.event_handler.app.store.set_current_graph(new_graph_name)


class ButtonGraphChoose(CustomButton):
    def __init__(self, event_handler, graph):
        super().__init__(event_handler)
        self.set_theme(self.event_handler.app.renderer.theme)
        self.graph = graph
        self.text_size = 16
        self.on_click = self.on_click_self
        self.height_shift = 0

    def update(self):
        self.position[0] = self.event_handler.app.display.get_width() - self.width - 5
        height = 5
        for button in self.event_handler.buttons:
            if button["button"] is self:
                break
            if button["type"] == "graph choose":
                height += button["button"].height + 5
        self.position[1] = height + self.height_shift
        self.content = [{'string': f"{self.graph.identifier}"}]

    def on_click_self(self):
        self.event_handler.app.store.current_graph = self.graph


class ButtonGraphRename(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.set_theme(self.event_handler.app.renderer.theme)
        self.text_size = 16
        self.content = [{'string': f"graph rename"}]
        self.on_click = self.on_click_self
        self.position[0] = 5

    def update(self):
        self.calculate_height()

    def on_click_self(self):
        self.event_handler.display_handler.graph_renaming = True
        self.event_handler.display_handler.graph_renaming_text = ""


class ButtonGraphExport(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.set_theme(self.event_handler.app.renderer.theme)
        self.text_size = 16
        self.content = [{'string': f"graph export"}]
        self.on_click = self.on_click_self
        self.position[0] = 5

    def update(self):
        self.calculate_height()

    def on_click_self(self):
        self.event_handler.app.store.export_graph(self.event_handler.app.store.current_graph.identifier)


class ButtonGraphResetColor(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.set_theme(self.event_handler.app.renderer.theme)
        self.text_size = 16
        self.content = [{'string': f"graph reset color"}]
        self.on_click = self.on_click_self
        self.position[0] = 5

    def update(self):
        self.calculate_height()

    def on_click_self(self):
        self.event_handler.app.store.current_graph.reset_graph_color()
