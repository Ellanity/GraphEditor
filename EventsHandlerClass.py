import pygame
import threading
from Commands import *


class EventsHandler:
    def __init__(self, app):
        self.app = app
        self.console_event_thread = self.EventThread("Console event thread", 1, self, "console handler")
        self.console_event_thread.setDaemon(True)
        self.commands_list = list()
        self.__init_commands__()

    def __init_commands__(self):
        self.commands_list = [
            # ## common
            {"identifier": "render", "have_args": False, "action": CommandRender(self).run},
            # ## graph
            {"identifier": "graph create", "have_args": True, "action": CommandGraphCreate(self).run},
            {"identifier": "graph choose", "have_args": True, "action": CommandGraphChoose(self).run},
            {"identifier": "graph delete", "have_args": True, "action": CommandGraphDelete(self).run},
            {"identifier": "graph save", "have_args":  False, "action": CommandGraphSave(self).run},
            {"identifier": "graph print in store", "have_args": False, "action": CommandGraphPrintInStore(self).run},
            {"identifier": "graph print current", "have_args":  False, "action": CommandGraphPrintCurrent(self).run},
            {"identifier": "graph export", "have_args": True, "action": CommandGraphExport(self).run},
            {"identifier": "graph import", "have_args": True, "action": CommandGraphImport(self).run},
            # ## vertex
            {"identifier": "vertex create", "have_args": True, "action": CommandVertexCreate(self).run},
            {"identifier": "vertex delete", "have_args": True, "action": CommandVertexDelete(self).run},
            {"identifier": "vertex paint", "have_args": True, "action": CommandVertexPaint(self).run},
            {"identifier": "vertex rename", "have_args": True, "action": CommandVertexRename(self).run},
            # ## edge
            {"identifier": "edge create", "have_args": True, "action": CommandEdgeCreate(self).run},
            {"identifier": "edge delete", "have_args": True, "action": CommandEdgeDelete(self).run},
            {"identifier": "edge paint", "have_args":  True, "action": CommandEdgePaint(self).run},
            {"identifier": "edge change oriented state", "have_args": True, "action": CommandEdgeChangeOrientedState(self).run},
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
                        # self.event_handler.event(self.event)
                    self.event_handler.app.clock.tick(10)
                except Exception as ex:
                    print(ex)

    def check_events(self):
        self.console_event_thread.start()
        while True:
            try:
                self.display_handler()
                self.command("render")
            except Exception as _:
                pass
            self.app.clock.tick(35)

    def command(self, command_get):
        parsed = list()
        action = None
        # parse command
        for command in self.commands_list:
            if command_get[:len(command["identifier"])] == command["identifier"]:
                if command["have_args"] is True:
                    for arg in command_get[len(command["identifier"]):].split(" "):
                        parsed.append(arg)

                action = command["action"]
                if '' in parsed:
                    parsed.remove('')
                # ## found needed command
                break
        if action is not None:
            action(parsed)
        return

    def display_handler(self):
        pygame.display.update()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.app.stop()

            # ## ### RIGHT MOUSE BUTTON CLICK
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # ## camera disable movement
                self.app.renderer.camera.move_state = False
                self.app.renderer.camera.reset_shift()
                # ## vertex disable movement
                if self.app.store.current_vertex is not None:
                    self.app.store.current_vertex.change_the_active_state()
                    self.app.store.current_vertex.reset_shift()
                self.app.store.current_vertex = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = list(pygame.mouse.get_pos())
                # ## check button
                if self.app.renderer.info_intersection(mouse_position):
                    self.app.renderer.change_theme()
                # ## if no button, check vertex
                else:
                    self.app.store.current_vertex = self.app.renderer.get_vertex_by_position(position=mouse_position)
                if self.app.store.current_vertex is not None:
                    self.app.store.current_vertex.change_the_active_state()
                    move_shift_start = mouse_position
                    self.app.store.current_vertex.move_shift_start = move_shift_start
                # ## if no vertex check camera movement
                else:
                    self.app.renderer.camera.move_state = True
                    self.app.renderer.camera.move_shift_start = mouse_position

            # ## ### LEFT MOUSE BUTTON CLICK
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if self.app.store.current_vertex_info is not None:
                    self.app.store.current_vertex_info.show_info = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                # ## check vertex
                mouse_position = list(pygame.mouse.get_pos())
                self.app.store.current_vertex_info = self.app.renderer.get_vertex_by_position(position=mouse_position)
                if self.app.store.current_vertex_info is not None:
                    self.app.store.current_vertex_info.show_info = True

            # ## ### MOUSE WHEEL FORWARD
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                self.app.renderer.camera.change_scale(0.1)
            # ## ### MOUSE WHEEL BACKWARD
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                self.app.renderer.camera.change_scale(-0.1)

        # ## ### RIGHT MOUSE BUTTON PRESS
        if pygame.mouse.get_pressed()[0]:
            pass  # pygame.mouse.get_pos()

        # ## ### RIGHT MOUSE BUTTON PRESSED AND MOVED
        # ## Move vertex if mouse change pos
        if self.app.store.current_vertex is not None:
            mouse_position = pygame.mouse.get_pos()
            self.app.store.current_vertex.move_shift_finish = mouse_position
            self.app.store.current_vertex.recalculate_position(1/self.app.renderer.camera.scale)
            self.app.store.current_vertex.move_shift_start = self.app.store.current_vertex.move_shift_finish

        # ## Move camera if mouse change pos
        if self.app.renderer.camera.move_state is True:
            mouse_position = pygame.mouse.get_pos()
            self.app.renderer.camera.move_shift_finish = mouse_position
            self.app.renderer.camera.recalculate_position()
            self.app.renderer.camera.move_shift_start = self.app.renderer.camera.move_shift_finish
