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
        matrix = [[0] * len(graph.vertexes) for _ in range(len(graph.vertexes))]
        for edge in graph.edges:
            vertex_first = vertex_second = None
            for vertex in graph.vertexes:
                if edge.vertex_identifier_first == vertex.identifier:
                    vertex_first = vertex
                if edge.vertex_identifier_second == vertex.identifier:
                    vertex_second = vertex
            if vertex_first.identifier != vertex_second.identifier:
                vfi = graph.vertexes.index(vertex_first)
                vsi = graph.vertexes.index(vertex_second)
                # print(vfi, vsi)
                if not edge.oriented:
                    # print(vfi, vsi)
                    matrix[vfi][vsi] = 1  # edge.weight
                matrix[vsi][vfi] = 1  # edge.weight
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

    def get_adjacency_list(self, graph):
        adjacency_list = list()
        for vertex in graph.vertexes:
            vertex_list = list()
            for edge in graph.edges:
                if edge.vertex_identifier_first == vertex.identifier:
                    vertex_list.append([edge.vertex_identifier_second, 1])
                elif edge.vertex_identifier_second == vertex.identifier:
                    vertex_list.append([edge.vertex_identifier_first, 1])
            adjacency_list.append(vertex_list)
        return adjacency_list

    def find_min_path(self, graph, vertex_first, vertex_second):
        if graph is None:
            return
        adjacency_matrix = self.get_adjacency_matrix(graph)
        # for row in adjacency_matrix:
        #     print(row)

        get_adjacency_list = self.get_adjacency_list(graph)

        g = get_adjacency_list
        # print(g)
        INF = 9999999
        n = len(graph.vertexes)
        d = [INF] * n  # d
        p = [0] * n # d
        s = graph.vertexes.index(graph.get_vertex_by_identifier(vertex_first))
        t = graph.vertexes.index(graph.get_vertex_by_identifier(vertex_second))
        u = [False] * n
        d[s] = 0

        for i in range(0, n):
            v = -1
            for j in range(0, n):
                if not u[j] and (v == -1 or d[j] < d[v]):
                    v = j
            if d[v] == INF:
                break
            u[v] = True
            # print(v, g[v])
            for j in range(0, len(g[v])):
                pre_to = g[v][j][0]
                to = graph.vertexes.index(graph.get_vertex_by_identifier(pre_to))
                len_ = int(g[v][j][1])
                if d[v] + len_ < d[to]:
                    d[to] = d[v] + len_
                    p[to] = v

        # print(d)

        path = list()
        v = t
        while v != s:
            v = p[v]
            path.append(v)

        path.append(s)
        path.reverse()
        print([graph.vertexes[vp].identifier for vp in path])

