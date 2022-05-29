import pygame


class GraphRenderer:
    def __init__(self, display=None, clock=None, graph=None):
        self.display = display
        self.clock = clock
        self.graph = graph
        self.setting = self.Settings()

    # settings are not available yet
    class Settings:
        def __init__(self):
            self.background_start_pos_x = 0
            self.background_start_pos_y = 0
            self.background_width = 500
            self.background_height = 500
            self.edges_width = 1
            self.vertexes_radius = 5
            self.graph_scale = 1

    def set_graph(self, graph):
        self.graph = graph

    def set_display(self, display):
        self.display = display

    def set_clock(self, clock):
        self.clock = clock

    def render_background(self):
        white = (255, 255, 255)
        self.display.fill(white)

    def render_edges(self):
        pass

    def render_vertexes(self):
        pass

    def render(self):
        if self.display is None:
            raise Exception("No display in graph renderer")
        if self.graph is None:
            raise Exception("No graph in graph renderer")
        if self.clock is None:
            raise Exception("No clock in graph renderer")

        self.render_background()
        self.render_edges()
        self.render_vertexes()

        pygame.display.flip()
