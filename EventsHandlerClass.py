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
                if self.purpose == "console handler":
                    self.event = input()
                    self.event_handler.event_implementation(self.event)
                self.event_handler.app.clock.tick(10)

    def events(self):
        self.console_event_thread.start()
        while True:
            try:
                self.display_handler()
                self.event_implementation("render")
            except Exception as ex:
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
        if event[:13] == "choose graph " and len(event) > 13:
            self.app.store.set_current_graph(event[13:])
            print("current graph:", self.app.store.current_graph.identifier)
        if event[:13] == "delete graph " and len(event) > 13:
            self.app.store.delete_graph(event[13:])
        if event == "save graph":
            self.app.store.save_current_graph_in_store()
        if event == "print graphs in store":
            print("; ".join([graph.identifier for graph in self.app.store.graphs if graph is not None]) + ";")
        if event == "print current graph":
            print(self.app.store.current_graph.identifier if self.app.store.current_graph is not None else ";")

        # VERTEXES
        if event[:13] == "create vertex " and len(event) > 13:
            args = event[13:].split(" ")
            self.app.store.current_graph.create_vertex(args[0], args[1], args[2])

        # ADDITIONAL COMMANDS
        if event == "command":
            pass
