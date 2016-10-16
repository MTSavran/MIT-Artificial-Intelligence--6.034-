# MIT 6.034 Lab 2: Search

def distinct(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

class Edge:
    def __init__(self, startNode, endNode, length):
        self.startNode = startNode
        self.endNode = endNode
        self.length = length

    def reverse(self):
        return Edge(self.endNode, self.startNode, self.length)

    def copy(self):
        return Edge(self.startNode, self.endNode, self.length)

    def __eq__(self, other):
        return (self.startNode == other.startNode
                and self.endNode == other.endNode
                and self.length == other.length)

    def __str__(self):
        return "Edge<"+",".join([self.startNode, self.endNode, str(self.length)])+">"

    __repr__ = __str__


class UndirectedGraph:
    def __init__(self, nodes=[], edges=[], heuristic_dict={}):
        self.nodes = nodes[:]
        self.edges = edges[:]
        self.heuristic_dict = heuristic_dict.copy()

    def is_valid_path(self, path) :
        # all nodes are nodes in the path, and consecutive nodes are neighbors
        return all([x in self.nodes for x in path]) and all([self.get_edge(a,b) for (a,b) in zip(path, path[1:])])

    def get_edges(self, startNode=None, endNode=None):
        """ Return a list of all the edges in the graph.  If start or end are
        provided, restricts to edges that start/end at particular nodes. """

        pred1 =  lambda node: (startNode is None) or (node == startNode)
        pred2 =  lambda node: (endNode is None)   or (node == endNode)

        return filter(
            lambda e: e is not None,
            [e if pred1(e.startNode) and pred2(e.endNode) else
             e.reverse() if pred2(e.startNode) and pred1(e.endNode)
             else None
             for e in self.edges
        ])

    def get_neighbors(self, node):
        "Returns an alphabetical list of neighboring nodes. Each node appears at most once."
        return sorted(distinct(map(lambda e: e.endNode, self.get_edges(node))))

    def get_neighboring_edges(self, startNode):
        "Returns a list of neighboring edges."
        return self.get_edges(startNode)

    def get_edge(self, startNode, endNode):
        """ Returns the edge that directly connects startNode to endNode
        (or None if there is no such edge) """
        edges = self.get_edges(startNode, endNode)
        if len(edges) == 0:
            return None
        else:
            return edges[0]

    def is_neighbor(self, startNode, endNode):
        "Returns True if there is an edge connecting startNode to endNode, else False"
        return any([endNode == e.endNode for e in self.get_edges(startNode)])

    # CREATE AND MODIFY THE GRAPH

    def join(self, startNode, endNode, edgeLength=None):
        # check whether edge already exists
        if self.is_neighbor(startNode, endNode):
            print "UndirectedGraph.join: Error adding edge to graph"
            return self
        self.edges.append(Edge(startNode, endNode, edgeLength))
        for node in [startNode, endNode]:
            if node not in self.nodes:
                print "UndirectedGraph.join: Adding", node, "to list of nodes"
                self.nodes.append(startNode)
        return self

    # HEURISTIC
    def get_heuristic_value(self, startNode, goalNode) :
       return self.heuristic_dict.get(goalNode, {}).get(startNode, 0)
    def set_heuristic(self, heuristicDict) :
        self.heuristic_dict = heuristicDict
        return self

    def copy(self):
        return UndirectedGraph(self.nodes[:],
                               [e.copy() for e in self.edges],
                               self.heuristic_dict.copy())

    def __str__(self):
        return "\n\t".join(["Graph<",
                            "nodes: " + str(self.nodes),
                            "edges: " + str(self.edges),
                            "heuristic: " + str(self.heuristic_dict)]) + "\n>"
    __repr__ = __str__

# Change to True for an example of graph creation:
if False:
    g = UndirectedGraph()
    g.nodes = ["A","B","C","D","E"]
    g.join("A","B",5)
    print g.get_neighboring_edges("B")


def do_nothing_fn(graph, goalNode, paths):
    return paths

def make_generic_search(extensions_fn, has_loops_fn): #hack to avoid circular imports

    def generic_search(sort_new_paths_fn = do_nothing_fn,
                       add_paths_to_front_of_agenda = True,
                       sort_agenda_fn = do_nothing_fn,
                       use_extended_set = False):

        # To prevent tester from throwing unexpected errors
        args = [sort_new_paths_fn, add_paths_to_front_of_agenda,
                sort_agenda_fn, use_extended_set]
        if args == [None, None, None, None]:
            raise NotImplementedError("To implement, call with non-None arguments")
        elif None in args:
            raise TypeError("'None' is not a valid argument for generic_search")

        # Make search algorithm with arguments specified above
        def search_algorithm(graph, start, goal, beam_width=None):
            agenda = [[start]]
            extended_set = set()

            while(agenda):
                path = agenda.pop(0)
                lastNode = path[-1]

                if(lastNode == goal):
                    return path
                elif use_extended_set and lastNode in extended_set:
                    continue
                else:
                    extended_set.add(lastNode)
                    new_paths_unsorted = [path for path in extensions_fn(graph, path)
                                          if not has_loops_fn(path)]
                    new_paths = sort_new_paths_fn(graph, goal, new_paths_unsorted)
                    if add_paths_to_front_of_agenda:
                        agenda = new_paths + agenda
                    else:
                        agenda = agenda + new_paths

                    if beam_width == None:
                        agenda = sort_agenda_fn(graph, goal, agenda)
                    else:
                        agenda = sort_agenda_fn(graph, goal, agenda, beam_width)

            # no path found
            return None

        return search_algorithm

    return generic_search
