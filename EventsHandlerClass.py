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
                        self.event_handler.event_implementation(self.event)
                    self.event_handler.app.clock.tick(10)
                except Exception as ex:
                    print(ex)

    def events(self):
        self.console_event_thread.start()
        while True:
            try:
                self.display_handler()
                self.event_implementation("render")
            except Exception as _:
                pass
            self.app.clock.tick(15)

    def display_handler(self):
        pygame.display.update()
        for event in pygame.event.get():
            # MAIN COMMANDS
            if event.type == pygame.QUIT:
                self.app.stop_program()
            # ADDITIONAL COMMANDS
            # right mouse button click
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pass  # print(event.pos())

        # right mouse button press
        if pygame.mouse.get_pressed()[0]:
            pass  # print(pygame.mouse.get_pos())

    def event_implementation(self, event):
        # MAIN COMMANDS
        if event == "render":
            self.app.renderer.set_graph(self.app.store.current_graph)
            self.app.renderer.set_display(self.app.display)
            self.app.renderer.set_clock(self.app.clock)
            self.app.renderer.render()

        # GRAPHS
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

        # VERTEXES
        # example in cli: create vertex 1 2 50 100; 1 - id, 2 - content, 50 - x, 100 - y
        if event[:14] == "create vertex " and len(event) > 14:
            args = event[14:].split(" ")
            vertex_identifier = args[0]
            content = args[1]
            position = [int(args[i]) for i in range(2, len(args))]
            self.app.store.current_graph.add_vertex(identifier=vertex_identifier, content=content, position=position)

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

        # ADDITIONAL COMMANDS
        if event == "command":
            pass
