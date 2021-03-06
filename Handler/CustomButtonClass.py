import datetime
import random
from copy import copy

import pygame


class CustomButton:
    def __init__(self, event_handler):
        # main
        self.event_handler = event_handler
        self.on_click = None
        self.on_press = None
        self.content = list()  # list of dicts  {string, color(r,g,b), size}
        self.position = [5, 5]
        self.width = 0
        self.height = 0
        # additional
        self.font = None
        self.theme = None  # self.event_handler.app.renderer.theme
        self.background_color = (255, 255, 255)
        self.border_color = (0, 0, 0)
        self.text_color = (0, 0, 0)
        self.text_margin_horizontal = 6
        self.text_margin_vertical = 3
        self.padding = 5
        self.text_size = 16
        #
        self.active = False
        self.show_info = False
        self.info = []

    def check_intersection(self, position):
        if self.position[0] < position[0] < self.position[0] + self.width and \
                self.position[1] < position[1] < self.position[1] + self.height:
            return True
        return False

    def click(self, ):
        if self.on_click is not None:
            self.on_click()
        else:
            self.on_click_self()

    def press(self):
        if self.on_press is not None:
            self.on_press()

    def update(self):
        if self.theme is not None:
            self.set_theme(self.theme)
        self.update_self()

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

        if self.active:
            self.background_color = theme.AREA_COLOR_ACTIVE
            self.border_color = theme.CIRCLE_COLOR_ACTIVE
            self.text_color = theme.CIRCLE_COLOR_ACTIVE

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
        last_but_height_with_same_x = 5
        for button in self.event_handler.buttons:
            if button["button"].position[0] == self.position[0]:
                last_but_height_with_same_x = button["button"].position[1]
                last_prefix = str(button["type"]).split(" ")[0].lower()
                break

        for button in self.event_handler.buttons:
            button_x = button["button"].position[0]
            if button_x != self.position[0]:
                continue
            else:
                prefix = str(button["type"]).split(" ")[0].lower()
                if prefix != last_prefix:
                    height += 10
                    last_but_height_with_same_x = height
                if button["button"] is self:
                    break
                height = last_but_height_with_same_x + button["button"].height + 5
                last_but_height_with_same_x = height
                last_prefix = prefix

        self.position[1] = height

    def update_self(self):
        pass

    def on_click_self(self):
        pass


class ButtonGraphInfo(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.on_click = self.event_handler.app.renderer.change_theme
        self.text_size = 18
        self.info = ["> Main info about current graph", "> Also it can change program color theme"]

    def update_self(self):
        if self.event_handler.app.store.current_graph is None:
            return
        self.calculate_height()
        content = list()
        content.append({'string': f"Graph: {self.event_handler.app.store.current_graph.identifier}"})
        content.append({'string': f"Vertexes: {len(self.event_handler.app.store.current_graph.vertexes)}"})
        content.append({'string': f"Edges: {len(self.event_handler.app.store.current_graph.edges)}"})
        content.append({'string': f"scale: {int(self.event_handler.app.renderer.camera.scale * 100)}%"})
        self.set_content(content)


#####################
### GRAPH BUTTONS ###
#####################
class ButtonGraphCommands(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"GRAPH COMMANDS"}]
        self.show_buttons = True
        self.info = ["> Click to show or hide graph commands"]

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
        for button in self.event_handler.buttons:
            if button["type"] != "graph info" \
                    and button["type"] != "graph delete" \
                    and button["type"] != "graph choose" \
                    and button["button"] is not self:
                if str(button["type"]).split(" ")[0].lower() == "graph":
                    if self.show_buttons:
                        button["button"].position[0] -= button["button"].width + 5
                    else:
                        button["button"].position[0] = 5  # += button["button"].width + 5
                    button["button"].update()
        self.show_buttons = not self.show_buttons


class ButtonGraphCreate(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"graph create"}]
        self.info = ["> An empty graph is created"]

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
        new_graph_name = f"Graph_{datetime.datetime.now()}_{random.randint(0, 1000000)}".replace(" ", "_")
        self.event_handler.app.store.create_graph(identifier=new_graph_name)
        self.event_handler.app.store.set_current_graph(new_graph_name)


class ButtonGraphCreateErdosRenyiModel(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"graph create erdos-renyi"}]
        self.info = ["> A random graph is created according to the model with parameters",
                     "> to complete the input of one parameter, enter, space",
                     "> n - count of vertexes",
                     "> p - probability of existence of each of all possible edges"]

    def update_self(self):
        self.calculate_height()
        if self.event_handler.display_handler.typing_erdos_renyi_model_args:
            args = str(self.event_handler.display_handler.typing_erdos_renyi_model_args_text).split(" ")
            if len(args) >= 2:
                self.content = [{'string': f"graph create erdos-renyi: n={args[0]} p={args[1]}"}]
            elif len(args) == 1:
                self.content = [{'string': f"graph create erdos-renyi: n={args[0]} p="}]
            else:
                self.content = [{'string': f"graph create erdos-renyi: n="}]

        else:
            self.content = [{'string': f"graph create erdos-renyi"}]

    def on_click_self(self):
        if not self.event_handler.display_handler.typing_erdos_renyi_model_args:
            self.event_handler.display_handler.typing_erdos_renyi_model_args = True
            self.event_handler.display_handler.typing_erdos_renyi_model_args_text = ""
        else:
            args = str(self.event_handler.display_handler.typing_erdos_renyi_model_args_text).split(" ")
            self.event_handler.app.store.graph_create_erdos_renyi_model(args[0], args[1])
            self.event_handler.display_handler.typing_erdos_renyi_model_args = False


class ButtonGraphColorizeSubgraphs(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"graph colorize subgraphs"}]
        self.info = ["> Colorize subgraphs"]

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
        if self.event_handler.app.store.current_graph is not None:
            self.event_handler.app.graph_calculator.colorize_subgraphs(self.event_handler.app.store.current_graph)


class ButtonGraphExportGepp(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"graph export gepp"}]
        self.info = ["> Export graph in gepp file"]

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
        self.event_handler.app.store.export_graph_gepp(self.event_handler.app.store.current_graph.identifier)


class ButtonGraphExportJson(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"graph export json"}]
        self.info = ["> Export graph in json file"]

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
        self.event_handler.app.store.export_graph_json(self.event_handler.app.store.current_graph.identifier)


class ButtonGraphImport(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"graph import"}]
        self.info = ["> Import graph from any type of file"]

    def update_self(self):
        self.calculate_height()
        if self.event_handler.display_handler.typing_graph_to_import:
            self.content = [{'string': f"graph name to import: {self.event_handler.display_handler.typing_graph_to_import_text}"}]
        else:
            self.content = [{'string': f"graph import"}]

    def on_click_self(self):
        if not self.event_handler.display_handler.typing_graph_to_import:
            self.event_handler.display_handler.typing_graph_to_import = True
        else:
            self.event_handler.app.store.import_graph(self.event_handler.display_handler.typing_graph_to_import_text)
            self.event_handler.display_handler.typing_graph_to_import = False
            self.event_handler.display_handler.typing_graph_to_import_text = ""
            self.content = [{'string': f"graph import"}]


class ButtonGraphFindMinPath(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"graph find min path"}]
        self.info = ["> Find min path between first and second vertexes", "> if it exists, lol"]

    def update_self(self):
        self.calculate_height()
        if len(self.event_handler.app.store.current_subgraph_vertexes) == 2 and self.position[0] > 0:
            v1 = self.event_handler.app.store.current_subgraph_vertexes[0].identifier
            v2 = self.event_handler.app.store.current_subgraph_vertexes[1].identifier
            self.content = [{'string': f"graph find min path {v1} -> {v2}"}]
        else:
            self.content = [{'string': f"graph find min path"}]

    def on_click_self(self):
        if len(self.event_handler.app.store.current_subgraph_vertexes) == 2:
            v1 = self.event_handler.app.store.current_subgraph_vertexes[0].identifier
            v2 = self.event_handler.app.store.current_subgraph_vertexes[1].identifier
            self.event_handler.app.graph_calculator.find_min_path(self.event_handler.app.store.current_graph, v1, v2)


class ButtonGraphMakeCircle(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"graph make circle"}]
        self.info = ["> Converts the image of the graph into a circle",
                     "> choosing the maximum radius",
                     "> and the same indentation between the vertices "]

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
        self.event_handler.app.graph_calculator.graph_make_circle(self.event_handler.app.store.current_graph)


class ButtonGraphMakeComplete(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"graph make complete"}]
        self.info = ["> make graph complete..."]

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
        self.event_handler.app.graph_calculator.graph_make_complete(self.event_handler.app.store.current_graph)


class ButtonGraphRename(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"graph rename"}]
        self.info = ["> Don't even try to enter the same names for different graphs"]

    def update_self(self):
        self.calculate_height()
        if self.event_handler.display_handler.renaming_graph:
            self.content = [{'string': f"graph renaming: {self.event_handler.display_handler.renaming_graph_text}"}]
        else:
            self.content = [{'string': f"graph rename"}]

    def on_click_self(self):
        if not self.event_handler.display_handler.renaming_graph:
            self.event_handler.display_handler.renaming_graph = True
            self.event_handler.display_handler.renaming_graph_text = ""
        else:
            self.event_handler.app.store.current_graph.identifier = self.event_handler.display_handler.renaming_graph_text
            self.event_handler.display_handler.renaming_graph = False


class ButtonGraphRenameAllEdges(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"graph rename all edges"}]
        self.info = ["> Makes normal names for edges"]

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
        if self.event_handler.app.store.current_graph is None:
            return
        graph = self.event_handler.app.store.current_graph
        for edge in graph.edges:
            graph.rename_edge(identifier=edge.identifier, identifier_new=edge.identifier + "_")
        for edge in graph.edges:
            identifier_new = "e" + str(graph.edges.index(edge) + 1)
            graph.rename_edge(identifier=edge.identifier, identifier_new=identifier_new)


class ButtonGraphRenameAllVertexes(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"graph rename all vertexes"}]
        self.info = ["> Makes normal names for vertexes"]

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
        if self.event_handler.app.store.current_graph is None:
            return
        graph = self.event_handler.app.store.current_graph
        for vertex in graph.vertexes:
            graph.rename_vertex(identifier=vertex.identifier, identifier_new=vertex.identifier + "_")
        for vertex in graph.vertexes:
            identifier_new = "v" + str(graph.vertexes.index(vertex) + 1)
            graph.rename_vertex(identifier=vertex.identifier, identifier_new=identifier_new)


class ButtonGraphResetColor(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"graph reset color"}]
        self.info = ["> All vertexes and edges become normal color"]

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
        self.event_handler.app.store.current_graph.reset_graph_color()


class ButtonGraphChoose(CustomButton):
    def __init__(self, event_handler, graph):
        super().__init__(event_handler)
        self.graph = graph
        self.height_shift = 0
        self.info = ["> U can choose this graph"]

    def update_self(self):
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


class ButtonGraphDelete(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"graph delete"}]
        self.info = ["> Please don't touch this button if u didn't export your graph before"]

    def update_self(self):
        if self.event_handler.app.store.current_graph is None:
            return
        self.position[1] = self.event_handler.app.display.get_height() - self.height - 5

    def on_click_self(self):
        self.event_handler.app.store.delete_graph(self.event_handler.app.store.current_graph.identifier)
        self.event_handler.app.renderer.graph = None
        if len(self.event_handler.app.store.graphs) > 0:
            self.event_handler.app.store.current_graph = self.event_handler.app.store.graphs[0]


#####################
### EDGES BUTTONS ###
#####################
class ButtonEdgeCommands(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"EDGE COMMANDS"}]
        self.info = ["> Click to show or hide edge commands"]
        self.show_buttons = True

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
        for button in self.event_handler.buttons:
            if button["button"] is not self:
                if str(button["type"]).split(" ")[0].lower() == "edge":
                    if self.show_buttons:
                        button["button"].position[0] -= button["button"].width + 5
                    else:
                        button["button"].position[0] += button["button"].width + 5
                    button["button"].update()
        self.show_buttons = not self.show_buttons


class ButtonEdgeCreate(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"edge create"}]
        self.info = ["> Edges are created between all selected vertexes",
                     "> [all vertexes in subgraph]",
                     "> Better use E button on your keyboard"]

    def update_self(self):
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


class ButtonEdgeChangeOrientationSide(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"edge change orientation side"}]
        self.info = ["> Change orientation of all selected edges [O on keyboard]"]

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
            if self.event_handler.app.store.current_graph is not None:
                for edge in self.event_handler.app.store.current_subgraph_edges:
                    if edge.oriented:
                        ev1 = copy(edge.vertex_identifier_first)
                        ev2 = copy(edge.vertex_identifier_second)
                        edge.vertex_identifier_first = ev2
                        edge.vertex_identifier_second = ev1


class ButtonEdgeChangeStatusOriented(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"edge change status oriented"}]
        self.info = ["Change all selected edges orientation state [N on keyboard]"]

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
            if self.event_handler.app.store.current_graph is not None:
                for edge in self.event_handler.app.store.current_subgraph_edges:
                    edge.oriented = not edge.oriented


class ButtonEdgeDelete(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"edge delete"}]
        self.info = ["> No comments",
                     "> really, it just delete all selected edges, what i can say more?",
                     "> Use DEL on keyboard", "> Vertexes same"]

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
        if self.event_handler.app.store.current_edge is not None:
            self.event_handler.app.store.current_graph.delete_edge(self.event_handler.app.store.current_edge.identifier)
        for edge in self.event_handler.app.store.current_subgraph_edges:
            self.event_handler.app.store.current_graph.delete_edge(edge.identifier)


class ButtonEdgeRename(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"edge rename"}]
        self.info = ["> It's going to be difficult, but I believe in you",
                     "> Life hack, click on the button, then select the desired edge with LCTRL",
                     "> It seems to work"]

    def update_self(self):
        self.calculate_height()
        if self.event_handler.app.store.edge_to_rename:
            self.content = [{'string': f"edge renaming: {self.event_handler.app.store.edge_to_rename.identifier}"}]
        else:
            self.content = [{'string': f"edge rename"}]

    def on_click_self(self):
        if not self.event_handler.display_handler.renaming_edge:
            if len(self.event_handler.app.store.current_subgraph_edges) == 1:
                self.event_handler.display_handler.renaming_edge = True
                if self.event_handler.app.store.edge_to_rename != self.event_handler.app.store.current_subgraph_edges[0]:
                    self.event_handler.display_handler.renaming_edge_text = ""
                self.event_handler.app.store.edge_to_rename = self.event_handler.app.store.current_subgraph_edges[0]
        else:
            self.event_handler.app.store.current_graph.rename_edge(identifier=self.event_handler.app.store.edge_to_rename.identifier,
                                                                     identifier_new=self.event_handler.display_handler.renaming_edge_text)
            self.event_handler.display_handler.renaming_edge = False
            self.event_handler.app.store.edge_to_rename = None


class ButtonEdgeResetColor(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"edge reset color"}]
        self.info = ["> edge reset color? hm... what can this button do?",
                     "> resets all selected edges color, if u really dont understand"]

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
        if self.event_handler.app.store.current_graph is not None:
            for edge in self.event_handler.app.store.current_subgraph_edges:
                edge.color = None


class ButtonEdgeSetWeight(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"edge set weight"}]
        self.info = ["> Enter weight (0 or more) and click here again, or press Enter"]

    def update_self(self):
        self.calculate_height()
        if self.event_handler.display_handler.typing_edge_weight \
                and len(self.event_handler.app.store.current_subgraph_edges) >= 1:
            self.content = [
                {'string': f"set edge {self.event_handler.app.store.current_subgraph_edges[0].identifier} "
                           f"weight: {self.event_handler.display_handler.typing_edge_weight_text}"}]
        else:
            self.content = [{'string': f"edge set weight"}]

    def on_click_self(self):
        if not self.event_handler.display_handler.typing_edge_weight:
            self.event_handler.display_handler.typing_edge_weight = True
        else:
            if len(self.event_handler.app.store.current_subgraph_edges) == 1:
                self.event_handler.app.store.current_graph.set_edge_weight(identifier=self.event_handler.app.store.current_subgraph_edges[0].identifier,
                                                                           weight=self.event_handler.display_handler.typing_edge_weight_text)
            self.event_handler.display_handler.typing_edge_weight = False
            self.event_handler.display_handler.typing_edge_weight_text = ""
            self.content = [{'string': f"edge_weight"}]


########################
### VERTEXES BUTTONS ###
########################
class ButtonVertexCommands(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"VERTEX COMMANDS"}]
        self.info = ["> Click to show or hide vertex commands"]
        self.show_buttons = True

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
        for button in self.event_handler.buttons:
            if button["button"] is not self:
                if str(button["type"]).split(" ")[0].lower() == "vertex":
                    if self.show_buttons:
                        button["button"].position[0] -= button["button"].width + 5
                    else:
                        button["button"].position[0] += button["button"].width + 5
                    button["button"].update()
        self.show_buttons = not self.show_buttons


class ButtonVertexCreate(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"vertex create"}]
        self.info = ["> Vertex is created in center of window",
                     "> Better use double click [in such way u can choose position!]"]

    def update_self(self):
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


class ButtonVertexDelete(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"vertex delete"}]
        self.info = ["> Read [edge delete] button info", "> Use DEL on keyboard."]

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
        if self.event_handler.app.store.current_vertex is not None:
            self.event_handler.app.store.current_graph.delete_vertex(self.event_handler.app.store.current_vertex.identifier)
        for vertex in self.event_handler.app.store.current_subgraph_vertexes:
            self.event_handler.app.store.current_graph.delete_vertex(vertex.identifier)


class ButtonVertexContent(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"vertex content"}]
        self.info = ["> I still believe that u can do it", "> Life hack in [edge rename] button, try it here too"]

    def update_self(self):
        self.calculate_height()
        if self.event_handler.display_handler.typing_vertex_content \
                and len(self.event_handler.app.store.current_subgraph_vertexes) >= 1:
            self.content = [
                {'string': f"set vertex {self.event_handler.app.store.current_subgraph_vertexes[0].identifier} "
                           f"content: {self.event_handler.display_handler.typing_vertex_content_text}"}]
        else:
            self.content = [{'string': f"vertex content"}]

    def on_click_self(self):
        if not self.event_handler.display_handler.typing_vertex_content:
            self.event_handler.display_handler.typing_vertex_content = True
        else:
            if len(self.event_handler.app.store.current_subgraph_vertexes) == 1:
                self.event_handler.app.store.current_graph.set_vertex_content(identifier=self.event_handler.app.store.current_subgraph_vertexes[0].identifier,
                                                                              content=self.event_handler.display_handler.typing_vertex_content_text)
            self.event_handler.display_handler.typing_vertex_content = False
            self.event_handler.display_handler.typing_vertex_content_text = ""


class ButtonVertexFindByContent(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"vertex find by content"}]
        self.info = ["Its cool, u enter content and it finds vertex, color it and moves camera"]

    def update_self(self):
        self.calculate_height()
        if self.event_handler.display_handler.typing_vertex_content_find:
            self.content = [{'string': f"vertex find by content: {self.event_handler.display_handler.typing_vertex_content_find_text}"}]
        else:
            self.content = [{'string': f"vertex find by content"}]

    def on_click_self(self):
        if not self.event_handler.display_handler.typing_vertex_content_find:
            self.event_handler.display_handler.typing_vertex_content_find = True
        else:
            if self.event_handler.app.store.current_graph.vertexes is None:
                return
            for vertex in self.event_handler.app.store.current_graph.vertexes:
                if str(vertex.content) == str(self.event_handler.display_handler.typing_vertex_content_find_text):
                    vertex.color = (255, 0, 255)
                    self.event_handler.app.renderer.camera.position[0] = \
                        -(vertex.position[0]) + (self.event_handler.app.display.get_width() / 2) / self.event_handler.app.renderer.camera.scale
                    self.event_handler.app.renderer.camera.position[1] = \
                        -(vertex.position[1]) + (self.event_handler.app.display.get_height() / 2) / self.event_handler.app.renderer.camera.scale
                    break
            self.event_handler.display_handler.typing_vertex_content_find = False


class ButtonVertexRename(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"vertex rename"}]
        self.info = ["> Lol, u can... Life hack in [edge rename]",
                     "> Can try to use LCTRL + I on keyboard, maybe it will be easier"]

    def update_self(self):
        self.calculate_height()
        if self.event_handler.app.store.vertex_to_rename:
            self.content = [{'string': f"vertex renaming: {self.event_handler.app.store.vertex_to_rename.identifier}"}]
        else:
            self.content = [{'string': f"vertex rename"}]

    def on_click_self(self):
        if not self.event_handler.display_handler.renaming_vertex:
            if len(self.event_handler.app.store.current_subgraph_vertexes) == 1:
                self.event_handler.display_handler.renaming_vertex = True
                if self.event_handler.app.store.vertex_to_rename != self.event_handler.app.store.current_subgraph_vertexes[0]:
                    self.event_handler.display_handler.renaming_vertex_text = ""
                self.event_handler.app.store.vertex_to_rename = self.event_handler.app.store.current_subgraph_vertexes[0]
        else:
            self.event_handler.app.store.current_graph.rename_vertex(identifier=self.event_handler.app.store.vertex_to_rename.identifier,
                                                                     identifier_new=self.event_handler.display_handler.renaming_vertex_text)
            self.event_handler.display_handler.renaming_vertex = False
            self.event_handler.app.store.vertex_to_rename = None


class ButtonVertexResetColor(CustomButton):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.content = [{'string': f"vertex reset color"}]
        self.info = ["> Just resets all selected vertexes color"]

    def update_self(self):
        self.calculate_height()

    def on_click_self(self):
        if self.event_handler.app.store.current_graph is not None:
            for vertex in self.event_handler.app.store.current_subgraph_vertexes:
                vertex.color = None
