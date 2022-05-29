import pygame

BG_COLOR = (255, 255, 255)


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
            self.edges_width = 2
            self.vertexes_radius = 8
            self.graph_scale = 1

    def set_graph(self, graph):
        self.graph = graph

    def set_display(self, display):
        self.display = display

    def set_clock(self, clock):
        self.clock = clock

    def render_background(self):
        self.display.fill(BG_COLOR)

    def render_edges(self):
        for edge in self.graph.edges:
            vertex_first = self.graph.get_vertex_by_identifier(edge.vertex_identifier_first)
            vertex_second = self.graph.get_vertex_by_identifier(edge.vertex_identifier_second)
            # print(edge.identifier, vertex_first.position, vertex_second.position, edge.color )
            pygame.draw.aaline(self.display, edge.color, vertex_first.position, vertex_second.position)

        """
        pygame.draw.line(sc, WHITE, [10, 30], [290, 15], 3)
        pygame.draw.line(sc, WHITE, [10, 50], [290, 35])
        pygame.draw.aaline(sc, WHITE, [10, 70], [290, 55])
        -----------------------
        pi = 3.14
        pygame.draw.arc(sc, WHITE, (10, 50, 280, 100), 0, pi)
        pygame.draw.arc(sc, PINK, (50, 30, 200, 150), pi, 2*pi, 3)
        """

    def render_vertexes(self):
        for vertex in self.graph.vertexes:
            pygame.draw.circle(self.display, BG_COLOR,
                               (vertex.position[0], vertex.position[1]), self.setting.vertexes_radius)
            pygame.draw.circle(self.display, vertex.color,
                               (vertex.position[0], vertex.position[1]), self.setting.vertexes_radius, 1)

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
