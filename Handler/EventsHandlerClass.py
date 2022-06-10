import threading

from Handler.Commands import *
from Handler.CustomButtonClass import *


class EventsHandler:
    def __init__(self, app):
        self.app = app
        # console
        self.console_event_thread = self.EventThread("Console event thread", 1, self, "ConsoleHandler")
        self.console_event_thread.setDaemon(True)
        self.commands_list = list()
        self.__init_commands__()
        # display
        self.fps = 20
        self.display_handler = self.DisplayHandler(self.app)
        self.buttons = list()
        self.__init_buttons__()

    def __init_commands__(self):
        self.commands_list = [
            # ## common
            {"identifier": "render", "have_args": False, "action": CommandRender(self).run},
            # ## graph
            {"identifier": "graph create", "have_args": True, "action": CommandGraphCreate(self).run},
            {"identifier": "graph choose", "have_args": True, "action": CommandGraphChoose(self).run},
            {"identifier": "graph delete", "have_args": True, "action": CommandGraphDelete(self).run},
            {"identifier": "graph print in store", "have_args": False, "action": CommandGraphPrintInStore(self).run},
            {"identifier": "graph print current", "have_args": False, "action": CommandGraphPrintCurrent(self).run},
            {"identifier": "graph export gepp", "have_args": True, "action": CommandGraphExportGepp(self).run},
            {"identifier": "graph export json", "have_args": True, "action": CommandGraphExportJson(self).run},
            {"identifier": "graph import", "have_args": True, "action": CommandGraphImport(self).run},
            {"identifier": "graph rename", "have_args": True, "action": CommandGraphRename(self).run},
            {"identifier": "graph reset color", "have_args": True, "action": CommandGraphResetColor(self).run},
            {"identifier": "graph create erdos renyi", "have_args": True, "action": CommandGraphCreateErdosRenyiModel(self).run},
            # ## vertex
            {"identifier": "vertex create", "have_args": True, "action": CommandVertexCreate(self).run},
            {"identifier": "vertex delete", "have_args": True, "action": CommandVertexDelete(self).run},
            {"identifier": "vertex paint", "have_args": True, "action": CommandVertexPaint(self).run},
            {"identifier": "vertex content", "have_args": True, "action": CommandVertexContent(self).run},
            {"identifier": "vertex rename", "have_args": True, "action": CommandVertexRename(self).run},
            # ## edge
            {"identifier": "edge create", "have_args": True, "action": CommandEdgeCreate(self).run},
            {"identifier": "edge delete", "have_args": True, "action": CommandEdgeDelete(self).run},
            {"identifier": "edge paint", "have_args": True, "action": CommandEdgePaint(self).run},
            {"identifier": "edge rename", "have_args": True, "action": CommandEdgeRename(self).run},
            {"identifier": "edge set weight", "have_args": True, "action": CommandEdgeSetWeight(self).run},
            {"identifier": "edge change oriented state", "have_args": True, "action": CommandEdgeChangeOrientedState(self).run},

            # ## additional (event for lab)
            {"identifier": "incidence matrix", "have_args": False, "action": CommandIncidenceMatrix(self).run},
            {"identifier": "find min path", "have_args": True, "action": CommandFindMinPath(self).run},
            {"identifier": "graph check complete", "have_args": False, "action": CommandGraphCheckComplete(self).run},
            {"identifier": "graph make complete", "have_args": False, "action": CommandGraphMakeComplete(self).run},
            {"identifier": "graph make circle", "have_args": False, "action": CommandGraphMakeCircle(self).run},
            {"identifier": "graph vertexes rename all", "have_args": False, "action": CommandVertexRenameAll(self).run},
            {"identifier": "graph edges rename all", "have_args": False, "action": CommandEdgeRenameAll(self).run},
            {"identifier": "vertex find by content", "have_args": True, "action": CommandVertexFindByContent(self).run},
        ]

    class EventThread(threading.Thread):
        def __init__(self, name, identifier, event_handler, purpose):
            threading.Thread.__init__(self)
            self.threadID = identifier
            self.name = name
            self.purpose = purpose
            self.event_handler = event_handler
            self.event = ""

        def run(self):
            while True:
                try:
                    if self.purpose == "ConsoleHandler":
                        self.event = input()
                        self.event_handler.command(self.event)
                    self.event_handler.app.clock.tick(10)
                except Exception as ex:
                    print("ConsoleThread:", ex)

    def __init_buttons__(self):
        self.buttons = [
            {"type": "main info", "button": ButtonGraphInfo(self)},

            {"type": "GRAPH COMMANDS", "button": ButtonGraphCommands(self)},
            {"type": "graph create", "button": ButtonGraphCreate(self)},
            {"type": "graph rename", "button": ButtonGraphRename(self)},
            {"type": "graph export gepp", "button": ButtonGraphExportGepp(self)},
            {"type": "graph export json", "button": ButtonGraphExportJson(self)},
            {"type": "graph import", "button": ButtonGraphImport(self)},
            {"type": "graph reset color", "button": ButtonGraphResetColor(self)},
            {"type": "graph find min path", "button": ButtonGraphFindMinPath(self)},
            {"type": "graph make circle", "button": ButtonGraphMakeCircle(self)},
            {"type": "graph make complete", "button": ButtonGraphMakeComplete(self)},
            {"type": "graph rename all vertexes", "button": ButtonGraphRenameAllVertexes(self)},
            {"type": "graph rename all edges", "button": ButtonGraphRenameAllEdges(self)},
            {"type": "graph create erdos-renyi model", "button": ButtonGraphCreateErdosRenyiModel(self)},

            {"type": "EDGE COMMANDS", "button": ButtonEdgeCommands(self)},
            {"type": "edge create", "button": ButtonEdgeCreate(self)},
            {"type": "edge delete", "button": ButtonEdgeDelete(self)},
            {"type": "edge rename", "button": ButtonEdgeRename(self)},
            {"type": "edge set weight", "button": ButtonEdgeSetWeight(self)},
            {"type": "edge reset color", "button": ButtonEdgeResetColor(self)},
            {"type": "edge change orientation side", "button": ButtonEdgeChangeOrientationSide(self)},
            {"type": "edge change status oriented", "button": ButtonEdgeChangeStatusOriented(self)},

            {"type": "VERTEX COMMANDS", "button": ButtonVertexCommands(self)},
            {"type": "vertex create", "button": ButtonVertexCreate(self)},
            {"type": "vertex delete", "button": ButtonVertexDelete(self)},
            {"type": "vertex rename", "button": ButtonVertexRename(self)},
            {"type": "vertex content", "button": ButtonVertexContent(self)},
            {"type": "vertex find by content", "button": ButtonVertexFindByContent(self)},
            {"type": "vertex reset color", "button": ButtonVertexResetColor(self)},

            {"type": "graph delete", "button": ButtonGraphDelete(self)},
        ]

    def update_buttons(self):
        choose_graph_buttons = []
        for button in self.buttons:
            try:
                button["button"].update()
                if button["type"] == "graph choose":
                    choose_graph_buttons.append(button)
            except Exception as ex:
                print("update_buttons:", ex)

        choose_graph_buttons_to_delete = [button["button"].graph.identifier for button in choose_graph_buttons]
        for graph in self.app.store.graphs:
            if graph.identifier in choose_graph_buttons_to_delete:
                choose_graph_buttons_to_delete.remove(graph.identifier)
            else:
                new_button = {"type": "graph choose", "button": ButtonGraphChoose(self, graph)}
                self.buttons.append(new_button)

        buttons_to_delete = []
        for button in self.buttons:
            if button["type"] == "graph choose":
                if button["button"].graph.identifier in choose_graph_buttons_to_delete:
                    buttons_to_delete.append(button)

        for button in buttons_to_delete:
            self.buttons.remove(button)

    class DisplayHandler:
        def __init__(self, app):
            self.app = app
            self.selection_subgraph = False
            self.selection_area = False
            self.display_full_screen = False
            self.display_sizes = (self.app.display.get_width(), self.app.display.get_height())
            # input text
            self.renaming_vertex = False
            self.renaming_vertex_text = ""
            self.renaming_edge = False
            self.renaming_edge_text = ""
            self.renaming_graph = False
            self.renaming_graph_text = ""
            self.typing_graph_to_import = False
            self.typing_graph_to_import_text = ""
            self.typing_vertex_content = False
            self.typing_vertex_content_text = ""
            self.typing_edge_weight = False
            self.typing_edge_weight_text = ""
            self.typing_vertex_content_find = False
            self.typing_vertex_content_find_text = ""
            self.typing_erdos_renyi_model_args = False
            self.typing_erdos_renyi_model_args_text = ""
            #
            self.double_click_timer = 0
            self.double_click_pos = [0, 0]

        def run(self):
            pygame.display.update()
            self.reset_event_bools()
            self.app.events_handler.update_buttons()
            self.keyboard_pressed(pygame.key.get_pressed())

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.app.stop()
                # ## ### DISPLAY SIZES
                if pygame.VIDEORESIZE and not self.display_full_screen:
                    self.display_full_screen = False
                    self.display_sizes = (self.app.display.get_width(), self.app.display.get_height())
                if event.type == pygame.KEYDOWN:
                    self.keyboard_down(event)

                # ## ### RIGHT MOUSE BUTTON CLICK
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.double_click_timer == 0 or self.double_click_timer > 0.25:
                        # first click
                        self.double_click_timer = 0.001
                        self.double_click_pos = pygame.mouse.get_pos()
                        self.right_mouse_down()
                    else:
                        # second click
                        if self.double_click_timer > 0.25 or pygame.mouse.get_pos() != self.double_click_pos:
                            self.right_mouse_down()
                        else:
                            self.right_mouse_double_click()
                        self.double_click_timer = 0
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.right_mouse_up()
                # ## ### LEFT MOUSE BUTTON CLICK
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.left_mouse_down()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    self.left_mouse_up()
                # ## ### MOUSE WHEEL
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    self.wheel_mouse_forward()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                    self.wheel_mouse_backward()

            if len(events) < 0:
                return False

            self.mouse_movement()
            if self.double_click_timer != 0:
                self.double_click_timer += self.app.events_handler.fps / 1000
            return True

        def reset_event_bools(self):
            self.selection_subgraph = False
            self.selection_area = False

        def keyboard_pressed(self, keys_pressed):
            if keys_pressed[pygame.K_LCTRL]:
                self.selection_subgraph = True
            if keys_pressed[pygame.K_LSHIFT]:
                self.selection_area = True
                if not self.app.store.subgraph_area["started"]:
                    mouse_position = pygame.mouse.get_pos()
                    self.app.store.subgraph_area["x1"] = mouse_position[0]
                    self.app.store.subgraph_area["y1"] = mouse_position[1]
                    self.app.store.subgraph_area["started"] = True
                    for vertex in self.app.store.current_subgraph_vertexes:
                        vertex.active = False
                    self.app.store.current_subgraph_vertexes.clear()
                    for edge in self.app.store.current_subgraph_edges:
                        edge.active = False
                    self.app.store.current_subgraph_edges.clear()

        def keyboard_down(self, event):
            # ## ### VERTEX RENAME
            # get input
            if self.renaming_vertex:
                if self.app.store.vertex_to_rename is None or event.key == pygame.K_RETURN:
                    self.renaming_vertex = False
                    self.renaming_vertex_text = ""
                    self.app.store.vertex_to_rename = None
                else:
                    if event.key == pygame.K_BACKSPACE:
                        self.renaming_vertex_text = self.renaming_vertex_text[:-1]
                    elif event.key == pygame.K_i:
                        if self.app.store.current_vertex is not None and self.app.store.vertex_to_rename is not None \
                                and self.app.store.current_vertex != self.app.store.vertex_to_rename:
                            self.app.store.vertex_to_rename = self.app.store.current_vertex
                            self.renaming_vertex_text = ""

                    if event.key != pygame.K_RETURN and event.key != pygame.K_BACKSPACE:
                        # if len(self.renaming_vertex_text) < 50:
                        try:
                            self.renaming_vertex_text += event.unicode
                        except Exception as ex:
                            print("vertex renaming: ", ex)

                    self.app.store.current_graph.rename_vertex(identifier=self.app.store.vertex_to_rename.identifier,
                                                               identifier_new=self.renaming_vertex_text)
            # restart input
            if not self.renaming_vertex:
                self.renaming_vertex_text = ""
                self.app.store.vertex_to_rename = None
            # start input
            if not self.renaming_vertex \
                    and not self.renaming_edge \
                    and not self.renaming_graph \
                    and not self.typing_graph_to_import \
                    and not self.typing_vertex_content \
                    and not self.typing_edge_weight \
                    and not self.typing_vertex_content_find \
                    and not self.typing_erdos_renyi_model_args:
                if event.key == pygame.K_i and len(self.app.store.current_subgraph_vertexes) == 1:
                    self.renaming_vertex = True
                    if self.app.store.vertex_to_rename != self.app.store.current_subgraph_vertexes[0]:
                        self.renaming_vertex_text = ""
                    self.app.store.vertex_to_rename = self.app.store.current_subgraph_vertexes[0]

            # ## ### EDGE RENAME\
            if self.renaming_edge:
                if self.app.store.edge_to_rename is None or event.key == pygame.K_RETURN:
                    self.renaming_edge = False
                    self.renaming_edge_text = ""
                    self.app.store.edge_to_rename = None
                else:
                    if event.key == pygame.K_BACKSPACE:
                        self.renaming_edge_text = self.renaming_edge_text[:-1]
                    elif event.key == pygame.K_i and self.app.store.current_edge != self.app.store.edge_to_rename:
                        self.app.store.edge_to_rename = self.app.store.current_edge
                        self.renaming_edge_text = ""
                    elif event.key != pygame.K_RETURN:
                        # if len(self.renaming_edge_text) < 50:
                        self.renaming_edge_text += event.unicode

                    self.app.store.current_graph.rename_edge(identifier=self.app.store.edge_to_rename.identifier,
                                                             identifier_new=self.renaming_edge_text)
            if not self.renaming_edge:
                self.renaming_edge_text = ""
                self.app.store.edge_to_rename = None

            # ## ### GRAPH RENAME
            if self.renaming_graph:
                if self.app.store.current_graph is None or event.key == pygame.K_RETURN:
                    self.renaming_graph = False
                    self.renaming_graph_text = ""
                    self.app.store.vertex_to_rename = None
                else:
                    if event.key == pygame.K_BACKSPACE:
                        self.renaming_graph_text = self.renaming_graph_text[:-1]
                    elif event.key != pygame.K_RETURN:
                        self.renaming_graph_text += event.unicode

                    self.app.store.current_graph.identifier = self.renaming_graph_text
            if not self.renaming_graph:
                self.renaming_graph_text = ""

            # ## ### IMPORT GRAPH
            if self.typing_graph_to_import:
                if self.app.store.current_graph is None or event.key == pygame.K_RETURN:
                    self.typing_graph_to_import = False
                    self.app.store.import_graph(self.typing_graph_to_import_text)
                    self.typing_graph_to_import_text = ""
                else:
                    if event.key == pygame.K_BACKSPACE:
                        self.typing_graph_to_import_text = self.typing_graph_to_import_text[:-1]
                    elif event.key != pygame.K_RETURN:
                        self.typing_graph_to_import_text += event.unicode
            if not self.typing_graph_to_import:
                self.typing_graph_to_import_text = ""

            # ## ### VERTEX CONTENT
            if self.typing_vertex_content:
                if self.app.store.current_graph is None or event.key == pygame.K_RETURN:
                    self.typing_vertex_content = False
                    if len(self.app.store.current_subgraph_vertexes) == 1:
                        # noinspection PyUnresolvedReferences
                        self.app.store.current_graph.set_vertex_content(
                            identifier=self.app.store.current_subgraph_vertexes[0].identifier,
                            content=self.typing_vertex_content_text)
                    self.app.store.import_graph(self.typing_vertex_content_text)
                    self.typing_vertex_content_text = ""
                else:
                    if event.key == pygame.K_BACKSPACE:
                        self.typing_vertex_content_text = self.typing_vertex_content_text[:-1]
                    elif event.key != pygame.K_RETURN:
                        self.typing_vertex_content_text += event.unicode
            if not self.typing_vertex_content:
                self.typing_vertex_content_text = ""

            # ## ### EDGE WEIGHT
            if self.typing_edge_weight:
                if self.app.store.current_graph is None or event.key == pygame.K_RETURN:
                    self.typing_edge_weight = False
                    if len(self.app.store.current_subgraph_edges) == 1:
                        # noinspection PyUnresolvedReferences
                        self.app.store.current_graph.set_edge_weight(
                            identifier=self.app.store.current_subgraph_edges[0].identifier,
                            weight=self.typing_edge_weight_text)
                    self.typing_edge_weight_text = ""
                else:
                    if event.key == pygame.K_BACKSPACE:
                        self.typing_edge_weight_text = self.typing_edge_weight_text[:-1]
                    elif event.key != pygame.K_RETURN:
                        self.typing_edge_weight_text += event.unicode
            if not self.typing_edge_weight:
                self.typing_edge_weight_text = ""

            # ## ### FIND BY CONTENT
            # get input
            if self.typing_vertex_content_find:
                if self.app.store.current_graph is None or event.key == pygame.K_RETURN:
                    self.typing_vertex_content_find = False
                    # ## ### body
                    if self.app.store.current_graph is not None:
                        for vertex in self.app.store.current_graph.vertexes:
                            if str(vertex.content) == str(self.typing_vertex_content_find_text):
                                vertex.color = (255, 0, 255)
                                self.app.renderer.camera.position[0] = \
                                    -(vertex.position[0]) + (self.app.display.get_width() / 2) / self.app.renderer.camera.scale
                                self.app.renderer.camera.position[1] = \
                                    -(vertex.position[1]) + (self.app.display.get_height() / 2) / self.app.renderer.camera.scale
                                break
                    # ## ###
                    self.typing_vertex_content_find_text = ""
                else:
                    if event.key == pygame.K_BACKSPACE:
                        self.typing_vertex_content_find_text = self.typing_vertex_content_find_text[:-1]
                    elif event.key != pygame.K_RETURN:
                        self.typing_vertex_content_find_text += event.unicode
            if not self.typing_vertex_content_find:
                self.typing_vertex_content_find_text = ""
                
            # ## ### GRAPH ERDOS_RENYI MODEL
            # get input
            if self.typing_erdos_renyi_model_args:
                if self.app.store.current_graph is None or event.key == pygame.K_RETURN:
                    self.typing_erdos_renyi_model_args = False
                    # ## ### body
                    args = str(self.typing_erdos_renyi_model_args_text).split(" ")
                    self.app.store.graph_create_erdos_renyi_model(args[0], args[1])
                    self.typing_erdos_renyi_model_args = False
                    # ## ###
                    self.typing_erdos_renyi_model_args_text = ""
                else:
                    if event.key == pygame.K_BACKSPACE:
                        self.typing_erdos_renyi_model_args_text = self.typing_erdos_renyi_model_args_text[:-1]
                    elif event.key != pygame.K_RETURN:
                        self.typing_erdos_renyi_model_args_text += event.unicode
            if not self.typing_erdos_renyi_model_args:
                self.typing_erdos_renyi_model_args_text = ""

            # ## ### DISPLAY SIZE
            if event.key == pygame.K_F11 or event.key == pygame.K_ESCAPE:
                if not self.display_full_screen and event.key == pygame.K_F11:
                    self.app.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    self.display_full_screen = True
                else:
                    self.app.display = pygame.display.set_mode(self.display_sizes, pygame.RESIZABLE)
                    self.app.display = pygame.display.set_mode(self.display_sizes, pygame.RESIZABLE)
                    self.display_full_screen = False
            # ## ### OTHER KEYS
            if self.renaming_vertex_text or self.renaming_graph_text:
                return
            if event.key == pygame.K_DELETE:
                # vertex
                if self.app.store.current_vertex is not None:
                    self.app.store.current_graph.delete_vertex(self.app.store.current_vertex.identifier)
                    self.app.store.current_vertex = None
                # vertexes subgraph
                if len(self.app.store.current_subgraph_vertexes) is not None:
                    vertexes_to_delete = self.app.store.current_subgraph_vertexes
                    for vertex in vertexes_to_delete:
                        self.app.store.current_graph.delete_vertex(vertex.identifier)
                    self.app.store.current_subgraph_vertexes.clear()
                # edge
                if self.app.store.current_edge is not None:
                    self.app.store.current_graph.delete_edge(self.app.store.current_edge.identifier)
                if len(self.app.store.current_subgraph_edges) is not None:
                    edges_to_delete = self.app.store.current_subgraph_edges
                    for edge in edges_to_delete:
                        self.app.store.current_graph.delete_edge(edge.identifier)
                    self.app.store.current_subgraph_edges.clear()
            if event.key == pygame.K_n:
                if self.app.store.current_edge is not None:
                    self.app.store.current_edge.oriented = not self.app.store.current_edge.oriented
                if self.app.store.current_subgraph_edges is not None:
                    for edge in self.app.store.current_subgraph_edges:
                        if edge != self.app.store.current_edge:
                            edge.oriented = not edge.oriented
            if event.key == pygame.K_o:
                if self.app.store.current_edge is not None and self.app.store.current_edge.oriented:
                    ev1 = copy(self.app.store.current_edge.vertex_identifier_first)
                    ev2 = copy(self.app.store.current_edge.vertex_identifier_second)
                    self.app.store.current_edge.vertex_identifier_first = ev2
                    self.app.store.current_edge.vertex_identifier_second = ev1
                if self.app.store.current_subgraph_edges is not None:
                    for edge in self.app.store.current_subgraph_edges:
                        if edge != self.app.store.current_edge and edge.oriented:
                            ev1 = copy(edge.vertex_identifier_first)
                            ev2 = copy(edge.vertex_identifier_second)
                            edge.vertex_identifier_first = ev2
                            edge.vertex_identifier_second = ev1
            if event.key == pygame.K_e:
                vertexes_identifiers_in_subgraph = [vertex.identifier for vertex in
                                                    self.app.store.current_subgraph_vertexes]

                edges_to_delete = []
                for edge in self.app.store.current_graph.edges:
                    if edge.vertex_identifier_first in vertexes_identifiers_in_subgraph \
                            and edge.vertex_identifier_second in vertexes_identifiers_in_subgraph:
                        edges_to_delete.append(edge)
                for edge in edges_to_delete:
                    self.app.store.current_graph.delete_edge(edge.identifier)

                connected_vertexes = list()
                for vertex1 in self.app.store.current_subgraph_vertexes:
                    for vertex2 in self.app.store.current_subgraph_vertexes:
                        if vertex1.identifier != vertex2.identifier \
                                and vertex1.identifier not in connected_vertexes \
                                and vertex2.identifier not in connected_vertexes:
                            edge_identifier = f"e-{vertex1.identifier}-{vertex2.identifier}-{random.randint(0, 1000000)}"
                            vertex_identifier_first = vertex1.identifier
                            vertex_identifier_second = vertex2.identifier
                            oriented = False
                            self.app.store.current_graph.add_edge(
                                identifier=edge_identifier,
                                vertex_identifier_first=vertex_identifier_first,
                                vertex_identifier_second=vertex_identifier_second,
                                oriented=oriented)
                    connected_vertexes.append(vertex1.identifier)

        def right_mouse_down(self):

            mouse_position = list(pygame.mouse.get_pos())
            # ## check button
            button = self.app.renderer.check_buttons_intersection(mouse_position)
            if button is not None:
                button["button"].click()
            # ## if no button, check vertex
            else:
                self.app.store.current_vertex = self.app.renderer.get_vertex_by_position(position=mouse_position)
                self.app.store.current_edge = self.app.renderer.get_edge_by_position(position=mouse_position)
            if self.app.store.current_vertex is not None:
                # append current vertex in subgraph
                if self.app.store.current_vertex not in self.app.store.current_subgraph_vertexes:
                    self.app.store.current_subgraph_vertexes.append(self.app.store.current_vertex)
                self.app.store.current_vertex.active = True
                # set start shift for all vertexes in subgraph
                for vertex in self.app.store.current_subgraph_vertexes:
                    vertex.move_shift_start = mouse_position
            # check edge
            elif self.app.store.current_edge is not None:
                self.app.store.current_edge.active = True
                # append current vertex in subgraph
                if self.app.store.current_edge not in self.app.store.current_subgraph_edges:
                    self.app.store.current_subgraph_edges.append(self.app.store.current_edge)
            # ## if no vertex and edge check camera movement
            else:
                self.app.renderer.camera.move_state = True
                self.app.renderer.camera.move_shift_start = mouse_position
                self.app.store.reset_subgraph_area()

            if not self.selection_subgraph:
                if self.app.store.current_vertex is not None:
                    for vertex in self.app.store.current_subgraph_vertexes:
                        vertex.active = False
                    self.app.store.current_subgraph_vertexes.clear()
                    self.app.store.current_vertex.active = True
                    self.app.store.current_subgraph_vertexes.append(self.app.store.current_vertex)
                if self.app.store.current_edge is not None:
                    for edge in self.app.store.current_subgraph_edges:
                        edge.active = False
                    self.app.store.current_subgraph_edges.clear()
                    self.app.store.current_edge.active = True
                    self.app.store.current_subgraph_edges.append(self.app.store.current_edge)

        def right_mouse_double_click(self):

            mouse_position = list(pygame.mouse.get_pos())
            # ## check button
            vertex = None
            edge = None
            button = self.app.renderer.check_buttons_intersection(mouse_position)
            if button is not None:
                button["button"].click()
                return
            # ## check vertex and edge
            else:
                vertex = self.app.renderer.get_vertex_by_position(position=mouse_position)
                edge = self.app.renderer.get_edge_by_position(position=mouse_position)
            if vertex is not None or edge is not None:
                return
            # ## if it's empty space => create vertex
            if self.app.store.current_graph is not None:
                new_vertex_name = ("vertex_" + str(datetime.datetime.now()) + "-" + str(
                    random.randint(0, 1000000000))).replace(" ", "_")
                content = "content"
                position = [0, 0]
                position[0] = mouse_position[0] / self.app.renderer.camera.scale - self.app.renderer.camera.position[0]
                position[1] = mouse_position[1] / self.app.renderer.camera.scale - self.app.renderer.camera.position[1]
                self.app.store.current_graph.add_vertex(identifier=new_vertex_name, content=content, position=position)

        def right_mouse_up(self):
            # ## camera disable movement
            self.app.renderer.camera.move_state = False
            self.app.renderer.camera.reset_shift()
            # ## vertex disable movement
            if not self.selection_subgraph:
                # vertexes
                for vertex in self.app.store.current_subgraph_vertexes:
                    vertex.active = False
                self.app.store.current_subgraph_vertexes.clear()
                # edges
                for edge in self.app.store.current_subgraph_edges:
                    edge.active = False
                self.app.store.current_subgraph_edges.clear()
            for vertex in self.app.store.current_subgraph_vertexes:
                vertex.reset_shift()
            if self.app.store.current_graph is not None:
                self.app.store.current_graph.calculate_graph_borders()
            # if self.app.store.current_edge is not None:
            #     self.app.store.current_edge.active = False

            self.app.store.current_vertex = None
            self.app.store.current_edge = None

        def left_mouse_down(self):
            # ## check vertex
            mouse_position = list(pygame.mouse.get_pos())
            self.app.store.current_vertex_info = self.app.renderer.get_vertex_by_position(position=mouse_position)
            if self.app.store.current_vertex_info is not None:
                self.app.store.current_vertex_info.show_info = True
            else:
                self.app.store.current_edge_info = self.app.renderer.get_edge_by_position(position=mouse_position)
                if self.app.store.current_edge_info is not None:
                    mouse_position = pygame.mouse.get_pos()
                    self.app.store.current_edge_info.show_info = True
                    position = self.app.store.current_edge_info.show_info_position
                    position[0] = mouse_position[0] / self.app.renderer.camera.scale - \
                                  self.app.renderer.camera.position[0]
                    position[1] = mouse_position[1] / self.app.renderer.camera.scale - \
                                  self.app.renderer.camera.position[1]

        def left_mouse_up(self):
            if self.app.store.current_vertex_info is not None:
                self.app.store.current_vertex_info.show_info = False
            if self.app.store.current_edge_info is not None:
                self.app.store.current_edge_info.show_info = False

        def wheel_mouse_forward(self):
            button = self.app.renderer.check_buttons_intersection(pygame.mouse.get_pos())
            if button is not None and button["type"] == "graph choose":
                min_height_of_choose_graph_button = 10000000
                for button in self.app.events_handler.buttons:
                    if button["type"] == "graph choose":
                        min_height_of_choose_graph_button = min(button["button"].position[1],
                                                                min_height_of_choose_graph_button)
                if min_height_of_choose_graph_button < 0:
                    for button in self.app.events_handler.buttons:
                        if button["type"] == "graph choose":
                            button["button"].height_shift += 33
            else:
                self.app.renderer.camera.change_scale(0.05)

        def wheel_mouse_backward(self):
            button = self.app.renderer.check_buttons_intersection(pygame.mouse.get_pos())
            if button is not None and button["type"] == "graph choose":
                max_height_of_choose_graph_button = 0
                for button in self.app.events_handler.buttons:
                    if button["type"] == "graph choose":
                        max_height_of_choose_graph_button = max(button["button"].position[1] + button["button"].height,
                                                                max_height_of_choose_graph_button)
                if max_height_of_choose_graph_button > self.app.display.get_height():
                    for button in self.app.events_handler.buttons:
                        if button["type"] == "graph choose":
                            button["button"].height_shift -= 33
            else:
                self.app.renderer.camera.change_scale(-0.1)

        def mouse_movement(self):
            # ## ### RIGHT MOUSE BUTTON PRESSED AND MOVED
            # ## Move vertex if mouse change pos
            if self.app.store.current_vertex is not None:
                mouse_position = pygame.mouse.get_pos()
                for vertex in self.app.store.current_subgraph_vertexes:
                    vertex.move_shift_finish = mouse_position
                    vertex.recalculate_position(1 / self.app.renderer.camera.scale)
                    vertex.move_shift_start = vertex.move_shift_finish

            # ## Move camera if mouse change pos
            if self.app.renderer.camera.move_state is True:
                mouse_position = pygame.mouse.get_pos()
                self.app.renderer.camera.move_shift_finish = mouse_position
                self.app.renderer.camera.recalculate_position()
                self.app.renderer.camera.move_shift_start = self.app.renderer.camera.move_shift_finish
                self.selection_area = False

            if self.selection_area:
                mouse_position = list(pygame.mouse.get_pos())
                self.app.store.subgraph_area["x2"] = mouse_position[0]
                self.app.store.subgraph_area["y2"] = mouse_position[1]
                # ## vertexes
                for vertex in self.app.store.current_subgraph_vertexes:
                    vertex.active = False
                self.app.store.current_subgraph_vertexes = self.app.renderer.get_vertexes_by_area(
                    self.app.store.subgraph_area)

                for vertex in self.app.store.current_subgraph_vertexes:
                    vertex.active = True
                # ## edges
                for edge in self.app.store.current_subgraph_edges:
                    edge.active = False
                self.app.store.current_subgraph_edges = self.app.renderer.get_edges_by_area(
                    self.app.store.subgraph_area)
                for edge in self.app.store.current_subgraph_edges:
                    edge.active = True
            else:
                self.app.store.reset_subgraph_area()

    def check_events(self):
        self.console_event_thread.start()
        while True:
            try:
                event = self.display_handler.run()
                if event:
                    self.command("render")
            except Exception as _:
                pass
                # print("check_events:", ex)
            self.app.clock.tick(self.fps)

    def command(self, command_get):
        parsed = list()
        action = None
        # parse command
        for command in self.commands_list:
            if command_get[:len(command["identifier"])] == command["identifier"]:
                if command["have_args"] is True:
                    parsed = command_get[len(command["identifier"]):].split(" ")
                action = command["action"]
                # while '' in parsed:
                if '' in parsed:
                    parsed.remove('')
                # ## found needed command
                break
        if action is not None:
            action(parsed)
        return
