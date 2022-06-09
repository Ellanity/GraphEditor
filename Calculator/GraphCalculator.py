import datetime
import math
import random


class GraphCalculator:
    def __init__(self):
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
                if not edge.oriented:
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
                        new_edge_name = (str(datetime.datetime.now()) + "-" + str(random.randint(0, 1000000000))). \
                            replace(" ", "_")
                        graph.add_edge(new_edge_name, vertex.identifier, vertex_.identifier, False)

    def get_adjacency_list(self, graph):
        adjacency_list = list()
        for vertex in graph.vertexes:
            vertex_list = list()
            for edge in graph.edges:
                if edge.vertex_identifier_first == vertex.identifier:
                    vertex_list.append([edge.vertex_identifier_second, edge.weight])
                elif edge.vertex_identifier_second == vertex.identifier and not edge.oriented:
                    vertex_list.append([edge.vertex_identifier_first, edge.weight])
            adjacency_list.append(vertex_list)
        return adjacency_list

    def dfs(self, graph, vertex_first, vertex_second, visited):
        if vertex_first == vertex_second:
            return True
        visited.append(vertex_first)
        for edge in graph.edges:
            vertex_to_check = None
            if edge.vertex_identifier_first == vertex_first:
                vertex_to_check = edge.vertex_identifier_second
            if edge.vertex_identifier_second == vertex_first and not edge.oriented:
                vertex_to_check = edge.vertex_identifier_first
            if vertex_to_check is not None and vertex_to_check not in visited:
                if self.dfs(graph, vertex_to_check, vertex_second, visited):
                    return True
        return False

    def find_min_path(self, graph, vertex_first, vertex_second):
        if graph is None:
            return
        random_color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
        way_exist = self.dfs(graph, vertex_first, vertex_second, [])
        if not way_exist:
            graph.get_vertex_by_identifier(vertex_first).color = random_color
            return

        g = self.get_adjacency_list(graph)
        # print(g)
        INF = 9999999
        n = len(graph.vertexes)
        d = [INF] * n  # d [999, 999, ...] list of vertexes, every element index of vertex in graph.vertexes (distance)
        p = [0] * n  # list to restore the path
        s = graph.vertexes.index(graph.get_vertex_by_identifier(vertex_first))  # first vertex index
        t = graph.vertexes.index(graph.get_vertex_by_identifier(vertex_second))  # second vertex index
        u = [False] * n  # [False, False, ...] list with marked traversed vertices

        d[s] = 0  # dist to first vertex

        for i in range(0, n):
            v = -1
            for j in range(0, n):
                if not u[j] and (v == -1 or d[j] < d[v]):
                    v = j
            if d[v] == INF:
                break
            u[v] = True
            for j in range(0, len(g[v])):
                pre_to = g[v][j][0]
                to = graph.vertexes.index(graph.get_vertex_by_identifier(pre_to))
                len_ = int(g[v][j][1])
                if d[v] + len_ < d[to]:
                    d[to] = d[v] + len_
                    p[to] = v

        # print(d) # can see dist to every vertex from first

        # restore path to second vertex
        path = list()
        v = t
        while v != s:
            v = p[v]
            path.append(v)

        path.reverse()
        path.append(t)
        # print(path)
        vertexes_in_path = [graph.vertexes[vp].identifier for vp in path]
        print("->".join(vertexes_in_path))

        for vp in path:
            graph.vertexes[vp].color = random_color

        for edge in graph.edges:
            if (edge.vertex_identifier_first in vertexes_in_path) \
                    and (edge.vertex_identifier_second in vertexes_in_path) \
                    and (abs(vertexes_in_path.index(edge.vertex_identifier_first) -
                             vertexes_in_path.index(edge.vertex_identifier_second)) <= 1):
                edge.color = random_color

    def graph_make_circle(self, graph):
        if len(graph.borders) <= 0:
            graph.calculate_graph_borders()

        x_circle_diameter = graph.borders[1] - graph.borders[0] if graph.borders[0] < graph.borders[1] else graph.borders[0] - graph.borders[1]
        y_circle_diameter = graph.borders[3] - graph.borders[2] if graph.borders[2] < graph.borders[3] else graph.borders[2] - graph.borders[3]
        circle_radius = max(x_circle_diameter, y_circle_diameter) / 2

        x_circle_center = min(graph.borders[0], graph.borders[1]) + circle_radius
        y_circle_center = min(graph.borders[2], graph.borders[3]) + circle_radius

        # x = r * cos(t) + x_center ; y = r * sin(t) + y_center ; 0 ≤ t < 2pi
        pi = math.pi
        indentation_between_vertices_in_radians = (2 * pi) / len(graph.vertexes)
        for vertex in graph.vertexes:
            vertex_radian = indentation_between_vertices_in_radians * graph.vertexes.index(vertex)
            vertex.position[0] = circle_radius * math.cos(vertex_radian) + x_circle_center
            vertex.position[1] = circle_radius * math.sin(vertex_radian) + y_circle_center
