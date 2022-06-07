import datetime
import random

import pygame
import threading
from Handler.Commands import *


class EventsHandler:
    def __init__(self, app):
        self.app = app
        self.fps = 20
        self.console_event_thread = self.EventThread("Console event thread", 1, self, "console handler")
        self.console_event_thread.setDaemon(True)
        self.commands_list = list()
        self.display_handler = self.DisplayHandler(self.app)
        self.__init_commands__()

    def __init_commands__(self):
        self.commands_list = [
            # ## common
            {"identifier": "render", "have_args": False, "action": CommandRender(self).run},
            # ## graph
            {"identifier": "graph create", "have_args": True, "action": CommandGraphCreate(self).run},
            {"identifier": "graph choose", "have_args": True, "action": CommandGraphChoose(self).run},
            {"identifier": "graph delete", "have_args": True, "action": CommandGraphDelete(self).run},
            {"identifier": "graph print in store", "have_args": False, "action": CommandGraphPrintInStore(self).run},
            {"identifier": "graph print current", "have_args":  False, "action": CommandGraphPrintCurrent(self).run},
            {"identifier": "graph export", "have_args": True, "action": CommandGraphExport(self).run},
            {"identifier": "graph import", "have_args": True, "action": CommandGraphImport(self).run},
            {"identifier": "graph rename", "have_args": True, "action": CommandGraphRename(self).run},
            {"identifier": "graph reset color", "have_args": True, "action": CommandGraphResetColor(self).run},
            # ## vertex
            {"identifier": "vertex create", "have_args": True, "action": CommandVertexCreate(self).run},
            {"identifier": "vertex delete", "have_args": True, "action": CommandVertexDelete(self).run},
            {"identifier": "vertex paint", "have_args": True, "action": CommandVertexPaint(self).run},
            {"identifier": "vertex content", "have_args": True, "action": CommandVertexContent(self).run},
            {"identifier": "vertex rename", "have_args": True, "action": CommandVertexRename(self).run},
            # ## edge
            {"identifier": "edge create", "have_args": True, "action": CommandEdgeCreate(self).run},
            {"identifier": "edge delete", "have_args": True, "action": CommandEdgeDelete(self).run},
            {"identifier": "edge paint", "have_args":  True, "action": CommandEdgePaint(self).run},
            {"identifier": "edge rename", "have_args":  True, "action": CommandEdgeRename(self).run},
            {"identifier": "edge change oriented state", "have_args": True, "action": CommandEdgeChangeOrientedState(self).run},

            # ## additional (event for lab)
            {"identifier": "incidence matrix", "have_args": False, "action": CommandIncidenceMatrix(self).run},
            {"identifier": "find min path", "have_args": True, "action": CommandFindMinPath(self).run},
            {"identifier": "graph check complete", "have_args": False, "action": CommandGraphCheckComplete(self).run},
            {"identifier": "graph make complete", "have_args": False, "action": CommandGraphMakeComplete(self).run},
            {"identifier": "graph make circle", "have_args": False, "action": CommandGraphMakeCircle(self).run},
            {"identifier": "graph rename all vertexes", "have_args": False, "action": CommandVertexRenameAll(self).run},
            {"identifier": "graph rename all edges", "have_args": False, "action": CommandEdgeRenameAll(self).run},
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
                    if self.purpose == "console handler":
                        self.event = input()
                        self.event_handler.command(self.event)
                    self.event_handler.app.clock.tick(10)
                except Exception as ex:
                    print(ex)

    class DisplayHandler:
        def __init__(self, app):
            self.app = app
            self.selection_subgraph = False
            self.selection_area = False
            self.display_full_screen = False
            self.display_sizes = (self.app.display.get_width(), self.app.display.get_height())
            # input text
            self.input_action = False
            self.input_text = ""
            #
            self.double_click_timer = 0
            self.double_click_pos = [0, 0]

        def run(self):
            pygame.display.update()
            self.reset_event_bools()
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
                        # print("first click")
                        self.double_click_timer = 0.001
                        self.double_click_pos = pygame.mouse.get_pos()
                        self.right_mouse_down()
                    else:
                        # print("second click")
                        if self.double_click_timer > 0.25 or pygame.mouse.get_pos() != self.double_click_pos:
                            self.right_mouse_down()
                        else:
                            self.right_mouse_double_click()
                            # print("doubleclick", self.double_click_timer, self.double_click_pos)
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
                    for vertex in self.app.store.current_subgraph_vertexes:
                        vertex.active = False
                    self.app.store.current_subgraph_vertexes.clear()
                    self.app.store.subgraph_area["started"] = True

        def keyboard_down(self, event):
            # ## ### VERTEX RENAME
            # get input
            if self.input_action:
                if self.app.store.vertex_to_rename is None or event.key == pygame.K_RETURN:
                    self.input_action = False
                    self.input_text = ""
                    self.app.store.vertex_to_rename = None
                else:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.key == pygame.K_i and self.app.store.current_vertex != self.app.store.vertex_to_rename:
                        self.app.store.vertex_to_rename = self.app.store.current_vertex
                        self.input_text = ""
                    elif event.key != pygame.K_RETURN:
                        # if len(self.input_text) < 50:
                        self.input_text += event.unicode

                    self.app.store.current_graph.rename_vertex(identifier=self.app.store.vertex_to_rename.identifier,
                                                               identifier_new=self.input_text)
            # restart input
            if not self.input_action:
                self.input_text = ""
                self.app.store.vertex_to_rename = None
            # start input
            if event.key == pygame.K_i and len(self.app.store.current_subgraph_vertexes) == 1:
                self.input_action = True
                if self.app.store.vertex_to_rename != self.app.store.current_subgraph_vertexes[0]:
                    self.input_text = ""
                self.app.store.vertex_to_rename = self.app.store.current_subgraph_vertexes[0]
            # ## ### DISPLAY SIZE
            if event.key == pygame.K_F11 or event.key == pygame.K_ESCAPE:
                if not self.display_full_screen and event.key == pygame.K_F11:
                    self.app.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    self.display_full_screen = True
                else:
                    self.app.display = pygame.display.set_mode(self.display_sizes, pygame.RESIZABLE)
                    self.app.display = pygame.display.set_mode(self.display_sizes, pygame.RESIZABLE)
                    self.display_full_screen = False

        def right_mouse_down(self):

            mouse_position = list(pygame.mouse.get_pos())
            # ## check button
            button = self.app.renderer.check_buttons_intersection(mouse_position)
            if button is not None:
                button.click()
            # ## if no button, check vertex
            else:
                self.app.store.current_vertex = self.app.renderer.get_vertex_by_position(position=mouse_position)
            if self.app.store.current_vertex is not None:
                # check if we choosing subgraph
                if not self.selection_subgraph:
                    for vertex in self.app.store.current_subgraph_vertexes:
                        vertex.active = False
                    self.app.store.current_subgraph_vertexes.clear()
                # append current vertex in subgraph
                if self.app.store.current_vertex not in self.app.store.current_subgraph_vertexes:
                    self.app.store.current_subgraph_vertexes.append(self.app.store.current_vertex)
                    self.app.store.current_vertex.active = True
                # set start shift for all vertexes in subgraph
                for vertex in self.app.store.current_subgraph_vertexes:
                    vertex.move_shift_start = mouse_position
            # check edge
            elif self.app.store.current_edge is not None:
                print(self.app.store.current_edge.identifier)
            # ## if no vertex and edge check camera movement
            else:
                self.app.renderer.camera.move_state = True
                self.app.renderer.camera.move_shift_start = mouse_position
                self.app.store.reset_subgraph_area()

        def right_mouse_double_click(self):

            mouse_position = list(pygame.mouse.get_pos())
            # ## check button
            button = self.app.renderer.check_buttons_intersection(mouse_position)
            vertex = None
            edge = None
            if button is not None:
                button.click()
                return
            # ## check vertex and edge
            else:
                vertex = self.app.renderer.get_vertex_by_position(position=mouse_position)
                edge = self.app.renderer.get_edge_by_position(position=mouse_position)
            if vertex is not None or edge is not None:
                return
            # ## if it's empty space => create vertex
            if self.app.store.current_graph is not None:
                new_vertex_name = ("vertex_" + str(datetime.datetime.now()) + "-" + str(random.randint(0, 1000000000))).replace(" ", "_")
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
                for vertex in self.app.store.current_subgraph_vertexes:
                    vertex.active = False
                self.app.store.current_subgraph_vertexes.clear()
            for vertex in self.app.store.current_subgraph_vertexes:
                vertex.reset_shift()
            self.app.store.current_graph.calculate_graph_borders()
            self.app.store.current_vertex = None

        def left_mouse_down(self):
            # ## check vertex
            mouse_position = list(pygame.mouse.get_pos())
            self.app.store.current_vertex_info = self.app.renderer.get_vertex_by_position(position=mouse_position)
            if self.app.store.current_vertex_info is not None:
                self.app.store.current_vertex_info.show_info = True
            else:
                self.app.store.current_edge_info = self.app.renderer.get_edge_by_position(position=mouse_position)
                if self.app.store.current_edge_info is not None:
                    self.app.store.current_edge_info.show_info = True

        def left_mouse_up(self):
            if self.app.store.current_vertex_info is not None:
                self.app.store.current_vertex_info.show_info = False
            if self.app.store.current_edge_info is not None:
                self.app.store.current_edge_info.show_info = False

        def wheel_mouse_forward(self):
            self.app.renderer.camera.change_scale(0.05)

        def wheel_mouse_backward(self):
            self.app.renderer.camera.change_scale(-0.1)

        def mouse_movement(self):
            # ## ### RIGHT MOUSE BUTTON PRESSED AND MOVED
            # ## Move vertex if mouse change pos
            if self.app.store.current_vertex is not None:
                mouse_position = pygame.mouse.get_pos()
                for vertex in self.app.store.current_subgraph_vertexes:
                    vertex.move_shift_finish = mouse_position
                    vertex.recalculate_position(1/self.app.renderer.camera.scale)
                    vertex.move_shift_start = vertex.move_shift_finish

            # ## Move camera if mouse change pos
            if self.app.renderer.camera.move_state is True:
                mouse_position = pygame.mouse.get_pos()
                self.app.renderer.camera.move_shift_finish = mouse_position
                self.app.renderer.camera.recalculate_position()
                self.app.renderer.camera.move_shift_start = self.app.renderer.camera.move_shift_finish
                self.selection_area = False

            if self.selection_area:
                for vertex in self.app.store.current_subgraph_vertexes:
                    vertex.active = False
                mouse_position = list(pygame.mouse.get_pos())
                self.app.store.subgraph_area["x2"] = mouse_position[0]
                self.app.store.subgraph_area["y2"] = mouse_position[1]
                self.app.store.current_subgraph_vertexes = \
                    [vertex for vertex in self.app.renderer.get_vertexes_by_area(self.app.store.subgraph_area)]
                for vertex in self.app.store.current_subgraph_vertexes:
                    vertex.active = True
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
