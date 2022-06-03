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
        print("current graph:" +
              self.events_handler.app.store.current_graph.identifier
              if self.events_handler.app.store.current_graph is not None else ";")


class CommandGraphDelete(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        self.events_handler.app.store.delete_graph(args[0])
        print(f"graph {args[0]} deleted")


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
        self.events_handler.app.store.export_graph(args[0])
        print(f"graph {args[0]} exported")


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
        if len(args) > 0:
            for graph in self.events_handler.app.store.graphs:
                if graph.identifier == str(args[0]):
                    graph.reset_graph_color()
                    print(f"graph {args[0]} color reseted")
                    break
        else:
            if self.events_handler.app.store.current_graph is not None:
                self.events_handler.app.store.current_graph.reset_graph_color()
                print(f"current graph color reseted")


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


class CommandEdgeChangeOrientedState(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        self.events_handler.app.store.current_graph.change_edge_oriented_state(args[0])
        print(args[0], " oriented state changed")


#################
### LAB TASKS ###
#################
class CommandIncidenceMatrix(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        if self.events_handler.app.store.current_graph is not None:
            graph = self.events_handler.app.store.current_graph
            matrix = self.events_handler.app.graph_calculator.get_incidence_matrix(graph)
            print("  ", ' '.join([vertex.identifier for vertex in graph.vertexes]))
            for row in matrix:
                print(graph.edges[matrix.index(row)].identifier, '  '.join(row))
        else:
            print("no graph selected")


class CommandGraphCheckComplete(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        if self.events_handler.app.store.current_graph is not None:
            graph = self.events_handler.app.store.current_graph
            print(f"graph {graph.identifier} complete: ",
                  self.events_handler.app.graph_calculator.check_is_the_graph_complete(graph))
        else:
            print("no graph selected")


class CommandGraphMakeComplete(Command):
    def __init__(self, events_handler):
        super().__init__(events_handler)

    def run(self, args):
        if self.events_handler.app.store.current_graph is not None:
            graph = self.events_handler.app.store.current_graph
            if not self.events_handler.app.graph_calculator.check_is_the_graph_complete(graph):
                self.events_handler.app.graph_calculator.graph_make_complete(graph)
                print(f"graph {graph.identifier} is complete now")
            else:
                print(f"graph already {graph.identifier} complete")
        else:
            print("no graph selected")


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
