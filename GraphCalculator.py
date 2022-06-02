import datetime
import random


class GraphCalculator:
    def __init__(self, app):
        self.app = app
        self.graph = None

    def set_graph(self, graph):
        self.graph = graph

    def get_incidence_matrix(self, graph):
        matrix = list()
        for edge in graph.edges:
            edge_row = list()
            for vertex in graph.vertexes:
                if str(edge.vertex_identifier_first) == str(vertex.identifier) \
                        or str(edge.vertex_identifier_second) == str(vertex.identifier):
                    edge_row.append("1")
                else:
                    edge_row.append("0")
            matrix.append(edge_row)
        return matrix

    def get_adjacency_matrix(self, graph):
        # incorrect
        matrix = [[0] * len(graph.vertexes) for i in range(len(graph.vertexes))]
        for edge in graph.edges:
            vertex_first = vertex_second = None
            for vertex in graph.vertexes:
                if edge.vertex_identifier_first == vertex.identifier:
                    vertex_first = vertex
                if edge.vertex_identifier_second == vertex.identifier:
                    vertex_second = vertex
            if vertex_first.identifier != vertex_second.identifier:
                if not edge.oriented:
                    matrix[graph.vertexes.index(vertex_first) - 1][graph.vertexes.index(vertex_second) - 1] = edge.weight
                matrix[graph.vertexes.index(vertex_second) - 1][graph.vertexes.index(vertex_first) - 1] = edge.weight
        return matrix

    def check_is_the_graph_complete(self, graph):
        for vertex in graph.vertexes:
            connected_vertexes = list()
            for edge in graph.edges:
                if edge.vertex_identifier_second == vertex.identifier \
                        and edge.vertex_identifier_first != vertex.identifier:
                    if edge.vertex_identifier_first not in connected_vertexes:
                        connected_vertexes.append(edge.vertex_identifier_first)
                if edge.vertex_identifier_first == vertex.identifier \
                        and edge.vertex_identifier_second != vertex.identifier:
                    if edge.vertex_identifier_second not in connected_vertexes:
                        connected_vertexes.append(edge.vertex_identifier_second)
            if len(connected_vertexes) != len(graph.vertexes) - 1:
                return False
        return True

    def graph_make_complete(self, graph):
        for vertex in graph.vertexes:
            connected_vertexes = list()
            for edge in graph.edges:
                if edge.oriented:
                    edge.change_the_orientation_state()
                if edge.vertex_identifier_second == vertex.identifier \
                        and edge.vertex_identifier_first != vertex.identifier:
                    if edge.vertex_identifier_first not in connected_vertexes:
                        connected_vertexes.append(edge.vertex_identifier_first)
                if edge.vertex_identifier_first == vertex.identifier \
                        and edge.vertex_identifier_second != vertex.identifier:
                    if edge.vertex_identifier_second not in connected_vertexes:
                        connected_vertexes.append(edge.vertex_identifier_second)
            if len(connected_vertexes) != len(graph.vertexes) - 1:
                for vertex_ in graph.vertexes:
                    if vertex_.identifier not in connected_vertexes and vertex_.identifier != vertex.identifier:
                        graph.add_edge((str(datetime.datetime.now()) + "-" + str(random.randint(0, 1000000000))),
                                       vertex.identifier, vertex_.identifier, False)

    def find_min_path(self, graph, vertex_first, vertex_second):
        pass
