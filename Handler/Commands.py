class Command:
    def __init__(self, events_handler=None):
        self.events_handler = events_handler
        self.event_finish_message = None

    def run(self, args):
        pass  # ## action must event do
        self.finish()  # ## can print message in console

    def finish(self):
        if self.event_finish_message is not None:
            print(str(self.event_finish_message))


##############
### RENDER ###
##############
class CommandRender(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        self.events_handler.app.renderer.set_display(self.events_handler.app.display)
        self.events_handler.app.renderer.set_graph(self.events_handler.app.store.current_graph)
        self.events_handler.app.renderer.set_selected_area(self.events_handler.app.store.subgraph_area)
        self.events_handler.app.renderer.render()
        

#############
### GRAPH ###
#############
class CommandGraphCreate(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        self.events_handler.app.store.create_graph(args[0])
        print(f"graph {args[0]} created")


class CommandGraphChoose(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        self.events_handler.app.store.set_current_graph(args[0])
        print("current graph: " +
              self.events_handler.app.store.current_graph.identifier
              if self.events_handler.app.store.current_graph is not None else ";")


class CommandGraphDelete(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        graph = args[0] if len(args) > 0 else None
        if graph is None and self.events_handler.app.store.current_graph is not None:
            graph = self.events_handler.app.store.current_graph.identifier
        if graph is not None:
            self.events_handler.app.store.delete_graph(graph)
            print(f"graph {graph} deleted")
        else:
            print(f"no graph selected")


class CommandGraphPrintInStore(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        print("graphs in store: ",
              "; ".join([(graph.identifier
                          if graph is not None else "None") for graph in self.events_handler.app.store.graphs]) + ';')


class CommandGraphPrintCurrent(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        print("current graph: ",
              self.events_handler.app.store.current_graph.identifier
              if self.events_handler.app.store.current_graph is not None else ";")


class CommandGraphExport(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        graph = args[0] if len(args) > 0 else None
        if graph is None and self.events_handler.app.store.current_graph is not None:
            graph = self.events_handler.app.store.current_graph.identifier
        if graph is not None:
            self.events_handler.app.store.export_graph(graph)
            print(f"graph {graph} exported")
        else:
            print(f"no graph selected")


class CommandGraphImport(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        self.events_handler.app.store.import_graph(args[0])
        print(f"graph {args[0]} imported")


class CommandGraphRename(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        self.events_handler.app.store.graph_rename(args[0], args[1])
        print(f"graph {args[0]}-{args[1]} renamed")


class CommandGraphResetColor(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        graph = args[0] if len(args) > 0 else None
        if graph is None and self.events_handler.app.store.current_graph is not None:
            graph = self.events_handler.app.store.current_graph.identifier
        if graph is not None:
            for graph_obj in self.events_handler.app.store.graphs:
                if graph_obj.identifier == graph:
                    graph_obj.reset_graph_color()
                    print(f"graph {graph} color reseted")
                    break
        else:
            print(f"no graph selected")


################
### VERTEXES ###
################

class CommandVertexCreate(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        vertex_identifier = args[0]
        content = args[1]
        position = [int(args[i]) for i in range(2, len(args))]
        self.events_handler.app.store.current_graph.add_vertex(identifier=vertex_identifier, content=content,
                                                               position=position)


class CommandVertexDelete(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        self.events_handler.app.store.current_graph.delete_vertex(args[0])
        print(f"vertex {args[0]} deleted")


class CommandVertexPaint(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        identifier = args[0]
        color = None
        if len(args) > 2:
            color = (int(args[1]), int(args[2]), int(args[3]))
        self.events_handler.app.store.current_graph.paint_vertex(identifier=identifier, color=color)
        print(f"vertex {identifier} painted")


class CommandVertexRename(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        identifier = args[0]
        identifier_new = args[1]
        self.events_handler.app.store.current_graph.rename_vertex(identifier=identifier, identifier_new=identifier_new)


class CommandVertexRenameAll(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        if self.events_handler.app.store.current_graph is not None:
            for vertex in self.events_handler.app.store.current_graph.vertexes:
                self.events_handler.app.store.current_graph.rename_vertex(identifier=vertex.identifier,
                                                                          identifier_new=vertex.identifier + "_")
            for vertex in self.events_handler.app.store.current_graph.vertexes:
                identifier_new = "v" + str(self.events_handler.app.store.current_graph.vertexes.index(vertex) + 1)
                self.events_handler.app.store.current_graph.rename_vertex(identifier=vertex.identifier,
                                                                          identifier_new=identifier_new)
            print("all vertex renamed")


class CommandVertexContent(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        identifier = args[0]
        content = args[1]
        self.events_handler.app.store.current_graph.set_vertex_content(identifier=identifier, content=content)
        print(f"content for vertex {identifier} seted content {content}")


#############
### EDGES ###
#############
class CommandEdgeCreate(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        edge_identifier = args[0]
        vertex_identifier_first = args[1]
        vertex_identifier_second = args[2]
        oriented = True if args[3] == "True" else False
        self.events_handler.app.store.current_graph.add_edge(
            identifier=edge_identifier,
            vertex_identifier_first=vertex_identifier_first,
            vertex_identifier_second=vertex_identifier_second,
            oriented=oriented)
        print(f"{edge_identifier} created")


class CommandEdgeDelete(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        self.events_handler.app.store.current_graph.delete_edge(args[0])
        print(f"edge {args[0]} deleted")


class CommandEdgePaint(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        identifier = args[0]
        color = None
        if len(args) > 2:
            color = (int(args[1]), int(args[2]), int(args[3]))
        self.events_handler.app.store.current_graph.paint_edge(identifier=identifier, color=color)
        print(f"edge {identifier} painted")


class CommandEdgeRename(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        self.events_handler.app.store.current_graph.rename_edge(identifier=args[0], identifier_new=args[1])
        print(f"edge {args[1]} renamed")


class CommandEdgeRenameAll(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        if self.events_handler.app.store.current_graph is not None:
            for edge in self.events_handler.app.store.current_graph.edges:
                self.events_handler.app.store.current_graph.rename_edge(identifier=edge.identifier,
                                                                        identifier_new=edge.identifier + "_")
            for edge in self.events_handler.app.store.current_graph.edges:
                identifier_new = "e" + str(self.events_handler.app.store.current_graph.edgees.index(edge) + 1)
                self.events_handler.app.store.current_graph.rename_edge(identifier=edge.identifier,
                                                                        identifier_new=identifier_new)
            print("all edges renamed")


class CommandEdgeChangeOrientedState(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        self.events_handler.app.store.current_graph.change_edge_oriented_state(args[0])
        print(args[0], " oriented state changed")


###################
### OTHER TASKS ###
###################
class CommandIncidenceMatrix(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        graph = args[0] if len(args) > 0 else None
        if graph is None and self.events_handler.app.store.current_graph is not None:
            graph = self.events_handler.app.store.current_graph.identifier
        if graph is not None:
            for graph_obj in self.events_handler.app.store.graphs:
                if graph_obj.identifier == graph:
                    matrix = self.events_handler.app.graph_calculator.get_incidence_matrix(graph_obj)
                    print("  ", ' '.join([vertex.identifier for vertex in graph_obj.vertexes]))
                    for row in matrix:
                        print(graph_obj.edges[matrix.index(row)].identifier, '  '.join(row))
                    break
        else:
            print(f"no graph selected")


class CommandGraphCheckComplete(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        graph = args[0] if len(args) > 0 else None
        if graph is None and self.events_handler.app.store.current_graph is not None:
            graph = self.events_handler.app.store.current_graph.identifier
        if graph is not None:
            for graph_obj in self.events_handler.app.store.graphs:
                if graph_obj.identifier == graph:
                    print(f"graph {graph} complete: ",
                          self.events_handler.app.graph_calculator.check_is_the_graph_complete(graph_obj))
                    break
        else:
            print(f"no graph selected")


class CommandGraphMakeComplete(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        graph = args[0] if len(args) > 0 else None
        if graph is None and self.events_handler.app.store.current_graph is not None:
            graph = self.events_handler.app.store.current_graph.identifier
        if graph is not None:
            for graph_obj in self.events_handler.app.store.graphs:
                if graph_obj.identifier == graph:
                    if not self.events_handler.app.graph_calculator.check_is_the_graph_complete(graph_obj):
                        self.events_handler.app.graph_calculator.graph_make_complete(graph_obj)
                        print(f"graph {graph} is complete now")
                    else:
                        print(f"graph {graph} already complete")
                    break
        else:
            print(f"no graph selected")


class CommandGraphMakeCircle(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        graph = args[0] if len(args) > 0 else None
        if graph is None and self.events_handler.app.store.current_graph is not None:
            graph = self.events_handler.app.store.current_graph.identifier
        if graph is not None:
            for graph_obj in self.events_handler.app.store.graphs:
                if graph_obj.identifier == graph:
                    # ## command body
                    self.events_handler.app.graph_calculator.graph_make_circle(graph_obj)
                    print(f"graph {graph} now is circle")
                    # ## finish
                    break
        else:
            print(f"no graph selected")


class CommandVertexFindByContent(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        if self.events_handler.app.store.current_graph is not None:
            graph = self.events_handler.app.store.current_graph
            vertex_found = False
            for vertex in graph.vertexes:
                if str(vertex.content) == str(args[0]):
                    vertex_found = True
                    self.events_handler.command(f"vertex paint {vertex.identifier} 255 0 255")
                    print(f"{vertex.identifier} have content: {args[0]}")
            if not vertex_found:
                print("no vertex with such content")
        else:
            print("no graph selected")


class CommandFindMinPath(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        if self.events_handler.app.store.current_graph is not None:
            graph = self.events_handler.app.store.current_graph
            print(f"finding min path from {args[0]} to {args[1]} in {graph.identifier}...")
            self.events_handler.app.graph_calculator.find_min_path(graph, vertex_first=args[0], vertex_second=args[1])
        else:
            print("no graph selected")
