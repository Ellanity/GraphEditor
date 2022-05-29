# Existing functions:
# - Work with store
# store.set_current_graph(graph_identifier)
# store.save_current_graph_in_store()
# store.create_graph(graph_identifier)
# store.export_graph(graph_identifier)
# store.import_graph(graph_identifier)
# store.delete_graph(graph_identifier)
# store.set_current_graph(graph_identifier)
# - Work with graphs
# store.graph[graph_identifier].add_vertex(vertex_identifier, content, position)
# store.graph[graph_identifier].add_edge(edge_identifier, vertex_identifier_first, vertex_identifier_second)
# store.graph[graph_identifier].delete_vertex(vertex_identifier):
# store.graph[graph_identifier].delete_edge(edge_identifier):
import pickle
from GraphEditorClass import GraphEditor


class Store:
    def __init__(self):
        self.graph_editor = GraphEditor()
        self.graphs = list()
        self.current_graph = None

    def create_graph(self, identifier):
        try:
            if len(self.get_graph_with_id(identifier)) != 0:
                raise Exception("Such graph already exists")
            graph = Graph()
            graph.set_identifier(identifier)
            self.graphs.append(graph)
        except Exception as ex:
            print(ex)

    def set_current_graph(self, identifier):
        graph_with_id = self.get_graph_with_id(identifier)
        if len(graph_with_id) != 0:
            self.current_graph = graph_with_id[0]

    def save_current_graph_in_store(self):
        if self.current_graph is None:
            raise Exception("Current graph is empty")
        self.delete_graph(self.current_graph.identifier)
        self.graphs.append(self.current_graph)

    def export_graph(self, identifier):
        graphs_to_save = [graph for graph in self.graphs if graph.identifier == identifier]
        for graph in graphs_to_save:
            with open(f'{identifier}-{graphs_to_save.index(graph)}.gepp', 'wb') as file:
                pickle.dump(graph, file)

    def import_graph(self, identifier):
        with open(f'{identifier}.gepp', 'rb') as file:
            graph_new = pickle.load(file)
            # check graph with same identifier
            if len([graph for graph in self.graphs if graph.identifier == identifier]) != 0:
                raise Exception("Such graph already exists, rename file with graph to import it")
            self.graphs.append(graph_new)

    def delete_graph(self, identifier):
        if identifier is None or "":
            raise Exception("The identifier of the graph being deleted is empty")
        for graph in self.graphs:
            if graph is None or graph.identifier == identifier:
                self.graphs.remove(graph)

    def get_graph_with_id(self, identifier):
        return [graph for graph in self.graphs if graph is not None and graph.identifier == identifier]


# For the program to work correctly,
# the graph must have an established
# standard structure
class Graph:
    def __init__(self):
        self.identifier = None
        self.vertexes = list()
        self.edges = list()

    def set_identifier(self, identifier):
        self.identifier = identifier
        if identifier is None:
            raise Exception("Graph identifier is empty")

    class Vertex:
        def __init__(self):
            self.identifier = None
            self.content = None
            self.position = None
            self.color = (0, 0, 0)

        def set_identifier(self, identifier):
            self.identifier = identifier

        def set_content(self, content):
            self.content = content

        def set_position(self, position):
            self.position = position

        def reset(self):
            self.identifier = None
            self.content = None
            self.position = None

    class Edge:
        def __init__(self):
            self.identifier = None
            self.vertex_identifier_first = None
            self.vertex_identifier_second = None
            self.oriented = False
            self.color = (0, 0, 0)

        def set_identifier(self, identifier):
            self.identifier = identifier

        def set_vertex_identifier_first(self, vertex_identifier):
            self.vertex_identifier_first = vertex_identifier

        def set_vertex_identifier_second(self, vertex_identifier):
            self.vertex_identifier_second = vertex_identifier

        def change_the_orientation_state(self):
            self.oriented = not self.oriented

        def reset(self):
            self.identifier = None
            self.vertex_identifier_first = None
            self.vertex_identifier_second = None
            self.oriented = False

    def add_edge(self, identifier, vertex_identifier_first, vertex_identifier_second, oriented=False):
        # not empty edge
        if identifier is None:
            raise Exception("New edge identifier is empty")
        if vertex_identifier_first is None:
            raise Exception("New edge vertex_identifier_first is empty")
        if vertex_identifier_second is None:
            raise Exception("New edge vertex_identifier_second is empty")
        # no edges with same identifier already in graph
        if len([edge for edge in self.edges if edge.identifier == identifier]) != 0:
            raise Exception("Edge with same identifier already in graph")

        vertex_first = self.get_vertex_by_identifier(vertex_identifier_first)
        vertex_second = self.get_vertex_by_identifier(vertex_identifier_second)
        if vertex_first is None or vertex_second is None:
            return

        edge = self.Edge()
        edge.set_identifier(identifier=identifier)
        edge.set_vertex_identifier_first(vertex_identifier=vertex_identifier_first)
        edge.set_vertex_identifier_second(vertex_identifier=vertex_identifier_second)
        if oriented:
            edge.change_the_orientation_state()
        self.edges.append(edge)

    def add_vertex(self, identifier, content, position):
        # not empty vertex
        if identifier is None:
            raise Exception("New vertex identifier is empty")
        if content is None:
            raise Exception("New vertex content is empty")
        if position is None:
            raise Exception("New vertex position is empty")

        # no vertexes with same identifier already in graph
        if len([vertex for vertex in self.vertexes if vertex.identifier == identifier]) != 0:
            raise Exception("Vertex with same identifier already in graph")

        vertex = self.Vertex()
        vertex.set_identifier(identifier=identifier)
        vertex.set_content(content=content)
        vertex.set_position(position=position)
        self.vertexes.append(vertex)

    def delete_edge(self, identifier):
        if identifier is None:
            raise Exception("The identifier of the edge being deleted is empty")
        for edge in self.edges:
            if edge.identifier == identifier:
                self.edges.remove(edge)

    def delete_vertex(self, identifier):
        if identifier is None:
            raise Exception("The identifier of the vertex being deleted is empty")
        for vertex in self.vertexes:
            if vertex.identifier == identifier:
                self.vertexes.remove(vertex)
        for edge in self.edges:
            if edge.vertex_identifier_first == identifier or \
                    edge.vertex_identifier_second == identifier:
                self.delete_edge(edge.identifier)

    def get_vertex_by_identifier(self, identifier):
        for vertex in self.vertexes:
            if vertex.identifier == identifier:
                return vertex
        return None

    def get_edge_by_identifier(self, identifier):
        for edge in self.edges:
            if edge.identifier == identifier:
                return edge
        return None
