import pygame
import threading


class EventsHandler:
    def __init__(self, app):
        self.app = app
        self.console_event_thread = self.EventThread("Console event thread", 1, self, "console handler")
        self.console_event_thread.setDaemon(True)

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
                        self.event_handler.event(self.event)
                    self.event_handler.app.clock.tick(10)
                except Exception as ex:
                    print(ex)

    def events(self):
        self.console_event_thread.start()
        while True:
            try:
                self.display_handler()
                self.event("render")
            except Exception as _:
                pass
            self.app.clock.tick(35)

    def display_handler(self):
        pygame.display.update()
        for event in pygame.event.get():
            # ## MAIN COMMANDS
            if event.type == pygame.QUIT:
                self.app.stop_program()
            # ## ADDITIONAL COMMANDS
            # right mouse button click
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # camera disable movement
                self.app.renderer.camera.move_state = False
                self.app.renderer.camera.reset_shift()
                # vertex disable movement
                if self.app.store.current_vertex is not None:
                    self.app.store.current_vertex.change_the_active_state()
                    self.app.store.current_vertex.reset_shift()
                self.app.store.current_vertex = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pygame.mouse.get_pos()
                # ## check button
                if self.app.renderer.info_intersection(mouse_position):
                    self.app.renderer.change_theme()
                # ## if no button, check vertex
                else:
                    self.app.store.current_vertex = self.app.renderer.get_vertex_by_position(position=mouse_position)
                if self.app.store.current_vertex is not None:
                    self.app.store.current_vertex.change_the_active_state()
                    self.app.store.current_vertex.move_shift_start = mouse_position
                # ## if no vertex check camera movement
                else:
                    self.app.renderer.camera.move_state = True
                    self.app.renderer.camera.move_shift_start = mouse_position

        # right mouse button press
        if pygame.mouse.get_pressed()[0]:
            pass  # pygame.mouse.get_pos()

        # ## Move vertex if mouse change pos
        if self.app.store.current_vertex is not None:
            mouse_position = pygame.mouse.get_pos()
            self.app.store.current_vertex.move_shift_finish = mouse_position
            self.app.store.current_vertex.recalculate_position()
            self.app.store.current_vertex.move_shift_start = self.app.store.current_vertex.move_shift_finish

        # ## Move camera if mouse change pos
        if self.app.renderer.camera.move_state is True:
            mouse_position = pygame.mouse.get_pos()
            self.app.renderer.camera.move_shift_finish = mouse_position
            self.app.renderer.camera.recalculate_position()
            self.app.renderer.camera.move_shift_start = self.app.renderer.camera.move_shift_finish

    # ## ### #### ##### WARNING! the api will have to be redone
    # it must be class Event with the main function for overload
    # every event must have its own instance of the class
    # thanks to this, users will be able to create their own types of events

    def event(self, event):
        # ## MAIN COMMANDS
        if event == "render":
            self.app.renderer.set_graph(self.app.store.current_graph)
            self.app.renderer.set_display(self.app.display)
            self.app.renderer.render()

        # ## GRAPHS
        if event[:13] == "create graph " and len(event) > 13:
            self.app.store.create_graph(event[13:])
            print(f"graph {event[13:]} created")
        if event[:13] == "choose graph " and len(event) > 13:
            self.app.store.set_current_graph(event[13:])
            print("current graph:" +
                  self.app.store.current_graph.identifier if self.app.store.current_graph is not None else ";")
        if event[:13] == "delete graph " and len(event) > 13:
            self.app.store.delete_graph(event[13:])
            print(f"graph {event[13:]} deleted")
        if event == "save graph":
            self.app.store.save_current_graph_in_store()
            print(self.app.store.current_graph.identifier if self.app.store.current_graph is not None else ";"
                  + "saved in store")
        if event == "print graphs in store":
            print("graphs in store: ",
                  "; ".join([(graph.identifier if graph is not None else "None") for graph in self.app.store.graphs])
                  + ';')
        if event == "print current graph":
            print("current graph: ",
                  self.app.store.current_graph.identifier if self.app.store.current_graph is not None else ";")

        if event[:13] == "export graph " and len(event) > 13:
            self.app.store.export_graph(event[13:])
            print(f"graph {event[13:]} exported")

        if event[:13] == "import graph " and len(event) > 13:
            self.app.store.import_graph(event[13:])
            print(f"graph {event[13:]} imported")

        # ## VERTEXES
        # example in cli: create vertex 1 2 50 100; 1 - id, 2 - content, 50 - x, 100 - y
        if event[:14] == "create vertex " and len(event) > 14:
            args = event[14:].split(" ")
            vertex_identifier = args[0]
            content = args[1]
            position = [int(args[i]) for i in range(2, len(args))]
            self.app.store.current_graph.add_vertex(identifier=vertex_identifier, content=content, position=position)

        if event[:14] == "rename vertex " and len(event) > 14:
            args = event[14:].split(" ")
            identifier = args[0]
            identifier_new = args[1]
            self.app.store.current_graph.rename_vertex(identifier=identifier, identifier_new=identifier_new)

        if event[:14] == "delete vertex " and len(event) > 14:
            self.app.store.current_graph.delete_vertex(event[14:])
            print(f"vertex {event[14:]} deleted")

        # paint vertex v1 1 2 3 | v1 - id, 1 2 3 - RGB
        if event[:13] == "paint vertex " and len(event) > 13:
            args = event[13:].split(" ")
            identifier = args[0]
            color = None
            if len(args) > 2:
                color = (int(args[1]), int(args[2]), int(args[3]))
            self.app.store.current_graph.paint_vertex(identifier=identifier, color=color)
            print(f"vertex {identifier} painted")

        # ## EDGES
        # example in cli: create vertex 1 v2 v3 False; 1 - id, v2, v3 - vertexes, False - oriented (default)
        if event[:12] == "create edge " and len(event) > 12:
            args = event[12:].split(" ")
            edge_identifier = args[0]
            vertex_identifier_first = args[1]
            vertex_identifier_second = args[2]
            oriented = True if args[3] == "True" else False
            self.app.store.current_graph.add_edge(identifier=edge_identifier,
                                                  vertex_identifier_first=vertex_identifier_first,
                                                  vertex_identifier_second=vertex_identifier_second,
                                                  oriented=oriented)

        if event[:28] == "edge change oriented state " and len(event) > 28:
            edge_identifier = event[28:]
            self.app.store.current_graph.change_edge_oriented_state(edge_identifier)
            print(edge_identifier, " oriented state changed")

        if event[:12] == "delete edge " and len(event) > 12:
            self.app.store.current_graph.delete_edge(event[12:])
            print(f"edge {event[12:]} deleted")

        if event[:11] == "paint edge " and len(event) > 11:
            args = event[11:].split(" ")
            identifier = args[0]
            color = None
            if len(args) > 2:
                color = (int(args[1]), int(args[2]), int(args[3]))
            self.app.store.current_graph.paint_edge(identifier=identifier, color=color)
            print(f"edge {identifier} painted")


        # ## ADDITIONAL COMMANDS
        if event == "command":
            pass
