# MIT 6.034 Lab 2: Search
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from search import Edge, UndirectedGraph, do_nothing_fn, make_generic_search
import read_graphs

all_graphs = read_graphs.get_graphs()
GRAPH_0 = all_graphs['GRAPH_0']
GRAPH_1 = all_graphs['GRAPH_1']
GRAPH_2 = all_graphs['GRAPH_2']
GRAPH_3 = all_graphs['GRAPH_3']
GRAPH_FOR_HEURISTICS = all_graphs['GRAPH_FOR_HEURISTICS']


#### PART 1: Helper Functions ##################################################

def path_length(graph, path):
    """Returns the total length (sum of edge weights) of a path defined by a
    list of nodes coercing an edge-linked traversal through a graph.
    (That is, the list of nodes defines a path through the graph.)
    A path with fewer than 2 nodes should have length of 0.
    You can assume that all edges along the path have a valid numeric weight."""
    if len(path) == 1: return 0
    
    total = 0
    for i in range(1, len(path)):
        currentNode = path[i]
        prevNode = path[i-1]
        edge = graph.get_edge(prevNode, currentNode)
        total += edge.length

    return total


def has_loops(path):
    """Returns True if this path has a loop in it, i.e. if it
    visits a node more than once. Returns False otherwise."""
    visited = {}
    for i in path:
        visited[i] = 0 
    if len(visited) != len(path):
        return True
    return False


def extensions(graph, path):
    """Returns a list of paths. Each path in the list should be a one-node
    extension of the input path, where an extension is defined as a path formed
    by adding a neighbor node (of the final node in the path) to the path.
    Returned paths should not have loops, i.e. should not visit the same node
    twice. The returned paths should be sorted in lexicographic order."""

    neighbors = graph.get_neighbors(path[-1])
    paths = []
    for neighbor in neighbors:
        path_1 = path[:]
        if neighbor not in path_1:
            path_1.append(neighbor)
            paths.append(path_1)
    return sorted(paths)

def sort_by_heuristic(graph, goalNode, nodes):
    """Given a list of nodes, sorts them best-to-worst based on the heuristic
    from each node to the goal node. Here, and in general for this lab, we
    consider a lower heuristic to be "better" because it represents a shorter
    potential path to the goal. Break ties lexicographically by node name."""
    l = []
    for i in nodes:
        l.append((i,graph.get_heuristic_value(i,goalNode)))
    lis = sorted(l, key=lambda tup: tup[0])
    cips = sorted(lis, key=lambda tup: tup[1])
    answer = []
    for i in cips:
        answer.append(i[0])
    return answer


# You can ignore the following line.  It allows generic_search (PART 2) to
# access the extensions and has_loops functions that you just defined in PART 1.
generic_search = make_generic_search(extensions, has_loops)  # DO NOT CHANGE


#### PART 2: Generic Search ####################################################

# Note: If you would prefer to get some practice with implementing search
# algorithms before working on Generic Search, you are welcome to do PART 3
# before PART 2.

# Define your custom path-sorting functions here.
# Each path-sorting function should be in this form:

# def my_sorting_fn(graph, goalNode, paths):
#     # YOUR CODE HERE
#     return sorted_paths


def hillsort(graph,goalNode,paths):
    paths = sorted(paths)
    paths = sorted(paths, key=lambda path: graph.get_heuristic_value(path[len(path)-1], goalNode))
    return paths

def bestsort(graph,goalNode,paths):
    paths = sorted(paths)
    paths = sorted(paths, key=lambda path: graph.get_heuristic_value(path[len(path)-1], goalNode))
    return paths

def branchsort(graph,goalNode,paths):
    agenda = sorted(paths, key=lambda path:
                        path_length(graph, path))
    return agenda

def alphabetical(graph,goalNode,paths):
    newPaths = sorted(paths)
    return newPaths

def heuristicpath_sort(graph, goalNode, paths):
    agenda = sorted(paths, key=lambda path: path_length(graph,path) + graph.get_heuristic_value(path[-1], goalNode))
    return agenda

generic_dfs = [do_nothing_fn, True, do_nothing_fn, False]

generic_bfs = [do_nothing_fn, False, do_nothing_fn, False]

generic_hill_climbing = [hillsort, True, do_nothing_fn, False]

generic_best_first = [do_nothing_fn, True, bestsort, False]

generic_branch_and_bound = [alphabetical, False, branchsort, False]
# generic_branch_and_bound = [None, False, None, False]

# generic_branch_and_bound_with_heuristic = [do_nothing_fn, False, None, None]
generic_branch_and_bound_with_heuristic = [hillsort, False, heuristicpath_sort, False]

generic_branch_and_bound_with_extended_set = [hillsort, False, branchsort, True]

generic_a_star = [hillsort, False, heuristicpath_sort, True]

# Here is an example of how to call generic_search (uncomment to run):
# my_dfs_fn = generic_search(*generic_dfs)
# my_dfs_path = my_dfs_fn(GRAPH_1, 'a', 'd')
# print my_dfs_path

# dfs = generic_search(*generic_dfs)(GRAPH_0, 'n1', 'n3')

# Or, combining the first two steps:
#my_dfs_path = generic_search(*generic_dfs)(GRAPH_2, 'S', 'G')
#print my_dfs_path


### OPTIONAL: Generic Beam Search
# If you want to run local tests for generic_beam, change TEST_GENERIC_BEAM to True:
TEST_GENERIC_BEAM = False

# The sort_agenda_fn for beam search takes fourth argument, beam_width:
# def my_beam_sorting_fn(graph, goalNode, paths, beam_width):
#     # YOUR CODE HERE
#     return sorted_beam_agenda

generic_beam = [None, None, None, None]

# Uncomment this to test your generic_beam search:
#print generic_search(*generic_beam)(GRAPH_2, 'S', 'G', beam_width=2)


#### PART 3: Search Algorithms #################################################

# Note: It's possible to implement the following algorithms by calling
# generic_search with the arguments you defined in PART 2.  But you're also
# welcome to code them without using generic_search if you would prefer to
# implement the algorithms by yourself.

def dfs(graph, startNode, goalNode):
    return generic_search(*generic_dfs)(graph, startNode, goalNode)

def bfs(graph, startNode, goalNode):
    # q = [[startNode]]
    # while q[0][-1] != goalNode:
    #     cur = q[0][-1]
    #     curpath = q[0]
    #     for v in graph.get_neighbors(cur):
    #         if v not in curpath:
    #             q.append(curpath+[v])
    #     q = q[1:]
    # return q[0]
    pathList = [(startNode,)]
    if startNode == goalNode:
      return [startNode]
    while len(pathList) > 0:
        #print pathList
        #print [ graph.get_heuristic(path[-1],goal) for path in pathList ]
        newPaths = []
        while len(pathList) > 0:
            pathToExtend = pathList[0]
            pathList.remove(pathList[0])
            nodeToExtend = pathToExtend[-1]
            newNodes = graph.get_neighbors(nodeToExtend)
            if len(pathToExtend) > 1:
                newNodes = [ node for node in newNodes if node not in pathToExtend]
            if goalNode in newNodes:
                goalPath = pathToExtend + (goalNode,)
                #print "goalPath", goalPath
                return list(goalPath)
            newPaths += [ pathToExtend + (node,) for node in newNodes ]
        pathList.extend(newPaths)
        
        # #print "newPathsList" + str(newPaths)
        # quickSort(graph,goal,newPaths,1)
        # #print "newPathsList sorted by len" + str(newPaths)
    return None

# graph = {"A":["B","C","E"], "E":["R","F"], "F":["G"], "R":["G"]}
# graph2 = {"A":["B"], "B":["C"]}
# print bfs(graph2,"A","C")

# level = {}
# for u in graph:
#     level[u] = -1
#     for v in graph[u]:
#         level[v] = -1
# print level



def hill_climbing(graph, startNode, goalNode):
    agenda = [[startNode]]
     
    while len(agenda) > 0:
        # Remove the first path from the queue
        currentPath = agenda.pop(0)
 
        # If the first path in queue terminates at goal node, exit
        terminalNode = currentPath[len(currentPath)-1]
        if terminalNode == goalNode: return currentPath
 
        # Create new paths by extending the first path to all the neighbors
        #   of the terminal node
        newPaths = []
        neighbors = graph.get_neighbors(terminalNode)
        for n in neighbors:
            # Reject all new paths with loops
            if n not in currentPath:
                newPath = currentPath[:]
                newPath.append(n)
                newPaths.append(newPath)
 
        # Sort the new paths, if any, by the estimated distances between
        #   terminal nodes and the goal
        newPaths = sorted(newPaths, key=lambda path:
                          graph.get_heuristic_value(path[len(path)-1], goalNode))
        newPaths.reverse()
 
        # Add new paths, if any, to the front of the queue
        for np in newPaths:
            agenda.insert(0, np)
             
    return []


def best_first(graph, startNode, goalNode):
    return generic_search(*generic_best_first)(graph, startNode, goalNode)

def beam(graph, startNode, goalNode, beam_width):
    agenda = [([startNode], 0)] 
    levelCount = {0: 1} 
    levelToPaths = [[startNode]] 

    while len(agenda) > 0:
        # Remove the first path from the agenda
        currentPathTuple = agenda.pop(0)
        currentPath = currentPathTuple[0]
        currentLevel = currentPathTuple[1]
 
        # If the path terminates at the goal node, return it
        terminalNode = currentPath[len(currentPath)-1]
        if terminalNode == goalNode: return currentPath
 
        # Create new paths and append to appropriate array in levelToPaths
        neighbors = graph.get_neighbors(terminalNode)
        newPaths = []
        for n in neighbors:
            # Reject all new paths with loops
            if n not in currentPath:
                newPath = currentPath[:]
                newPath.append(n)
                newPaths.append(newPath)
 
                if len(levelToPaths)<=currentLevel+1:
                    newLevelPathList = [newPath]
                    levelToPaths.append(newLevelPathList)
                    levelCount[currentLevel+1] = 1
                else:
                    oldLevelPathList = levelToPaths[currentLevel+1]
                    newLevelPathList = oldLevelPathList[:]
                    newLevelPathList.append(newPath)
                     
                    levelToPaths[currentLevel+1] = newLevelPathList
                    levelCount[currentLevel+1] += 1
 
        # Go through each level and purge necessary paths
        for level in levelCount.keys():
            if levelCount[level] > beam_width:
                # Sort all paths by heuristic value,
                #   keep only lowest beam_width paths
                allPaths = levelToPaths[level]
                allPaths = sorted(allPaths, key=lambda path:
                                  graph.get_heuristic_value(path[len(path)-1], goalNode))
                newPathList = allPaths[0:beam_width]
                levelToPaths[level] = newPathList
                levelCount[level] = beam_width
 
                purgedPaths = allPaths[beam_width:]
                for pp in purgedPaths:
                    if pp in newPaths: newPaths.remove(pp)
                    if (pp, level) in agenda: agenda.remove((pp, level))
 
 
        # Add appropriate paths to agenda
        for np in newPaths:
            agenda.append((np, currentLevel+1))
 
    return None


def branch_and_bound(graph, startNode, goalNode):
    agenda = [[startNode]]
 
    while len(agenda) > 0:
        # Remove the first path from the queue
        currentPath = agenda.pop(0)
 
        # If the first path in queue terminates at goal node, exit
        terminalNode = currentPath[len(currentPath)-1]
        if terminalNode == goalNode: return currentPath
 
        # Create new paths by extending the first path to all the neighbors
        #   of the terminal node
        newPaths = []
        neighbors = graph.get_neighbors(terminalNode)
        for n in neighbors:
            # Reject all new paths with loops
            if n not in currentPath:
                newPath = currentPath[:]
                newPath.append(n)
                newPaths.append(newPath)
 
        # Add remaining new paths, if any, to the queue
        for np in newPaths:
            agenda.append(np)
 
        # Sort the entire queue by path length with least-cost paths in front
        agenda = sorted(agenda, key=lambda path:
                        path_length(graph, path))
 
         
    return None


def branch_and_bound_with_heuristic(graph, startNode, goalNode):
    return generic_search(*generic_branch_and_bound_with_heuristic)(graph, startNode, goalNode)

def branch_and_bound_with_extended_set(graph, startNode, goalNode):
    return generic_search(*generic_branch_and_bound_with_extended_set)(graph, startNode, goalNode)


def a_star(graph, startNode, goalNode):
    extended = set()
    q = [[startNode]]
    while q[0][-1] != goalNode:
        node = q[0][-1]
        path = q[0]
        if node not in extended:
            extended.add(node)
            for child in graph.get_neighbors(node):
                if child not in path:
                    q.append(path+[child])
        q = q[1:]
        q.sort(key = lambda x: path_length(graph, x) + graph.get_heuristic_value(x[-1], goalNode))
    return q[0]


#### PART 4: Heuristics ########################################################

def is_admissible(graph, goalNode):
    """Returns True if this graph's heuristic is admissible; else False.
    A heuristic is admissible if it is either always exactly correct or overly
    optimistic; it never over-estimates the cost to the goal."""
    for node in graph.nodes:
        if path_length(graph, a_star(graph,node,goalNode)) < graph.get_heuristic_value(node,goalNode):
            return False
    return True

def is_consistent(graph, goalNode):
    """Returns True if this graph's heuristic is consistent; else False.
    A consistent heuristic satisfies the following property for all
    nodes v in the graph:
        Suppose v is a node in the graph, and N is a neighbor of v,
        then, heuristic(v) <= heuristic(N) + edge_weight(v, N)
    In other words, moving from one node to a neighboring node never unfairly
    decreases the heuristic.
    This is equivalent to the heuristic satisfying the triangle inequality."""
    for e in graph.edges:
        diff = abs(graph.get_heuristic_value(e.startNode, goalNode) -
                   graph.get_heuristic_value(e.endNode, goalNode))
        if e.length < diff: return False
    return True


### OPTIONAL: Picking Heuristics
# If you want to run local tests on your heuristics, change TEST_HEURISTICS to True:
TEST_HEURISTICS = False

# heuristic_1: admissible and consistent

[h1_S, h1_A, h1_B, h1_C, h1_G] = [None, None, None, None, None]

heuristic_1 = {'G': {}}
heuristic_1['G']['S'] = h1_S
heuristic_1['G']['A'] = h1_A
heuristic_1['G']['B'] = h1_B
heuristic_1['G']['C'] = h1_C
heuristic_1['G']['G'] = h1_G


# heuristic_2: admissible but NOT consistent

[h2_S, h2_A, h2_B, h2_C, h2_G] = [None, None, None, None, None]

heuristic_2 = {'G': {}}
heuristic_2['G']['S'] = h2_S
heuristic_2['G']['A'] = h2_A
heuristic_2['G']['B'] = h2_B
heuristic_2['G']['C'] = h2_C
heuristic_2['G']['G'] = h2_G


# heuristic_3: admissible but A* returns non-optimal path to G

[h3_S, h3_A, h3_B, h3_C, h3_G] = [None, None, None, None, None]

heuristic_3 = {'G': {}}
heuristic_3['G']['S'] = h3_S
heuristic_3['G']['A'] = h3_A
heuristic_3['G']['B'] = h3_B
heuristic_3['G']['C'] = h3_C
heuristic_3['G']['G'] = h3_G


# heuristic_4: admissible but not consistent, yet A* finds optimal path

[h4_S, h4_A, h4_B, h4_C, h4_G] = [None, None, None, None, None]

heuristic_4 = {'G': {}}
heuristic_4['G']['S'] = h4_S
heuristic_4['G']['A'] = h4_A
heuristic_4['G']['B'] = h4_B
heuristic_4['G']['C'] = h4_C
heuristic_4['G']['G'] = h4_G


##### PART 5: Multiple Choice ##################################################

ANSWER_1 = '2'

ANSWER_2 = '4'

ANSWER_3 = '1'

ANSWER_4 = '3'


#### SURVEY ####################################################################

NAME = "Mehmet Tugrul Savran"
COLLABORATORS = "None"
HOW_MANY_HOURS_THIS_LAB_TOOK = "4"
WHAT_I_FOUND_INTERESTING = "Everyting"
WHAT_I_FOUND_BORING = "Nothing"
SUGGESTIONS = "None"


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the online tester. DO NOT CHANGE!

generic_dfs_sort_new_paths_fn = generic_dfs[0]
generic_bfs_sort_new_paths_fn = generic_bfs[0]
generic_hill_climbing_sort_new_paths_fn = generic_hill_climbing[0]
generic_best_first_sort_new_paths_fn = generic_best_first[0]
generic_branch_and_bound_sort_new_paths_fn = generic_branch_and_bound[0]
generic_branch_and_bound_with_heuristic_sort_new_paths_fn = generic_branch_and_bound_with_heuristic[0]
generic_branch_and_bound_with_extended_set_sort_new_paths_fn = generic_branch_and_bound_with_extended_set[0]
generic_a_star_sort_new_paths_fn = generic_a_star[0]

generic_dfs_sort_agenda_fn = generic_dfs[2]
generic_bfs_sort_agenda_fn = generic_bfs[2]
generic_hill_climbing_sort_agenda_fn = generic_hill_climbing[2]
generic_best_first_sort_agenda_fn = generic_best_first[2]
generic_branch_and_bound_sort_agenda_fn = generic_branch_and_bound[2]
generic_branch_and_bound_with_heuristic_sort_agenda_fn = generic_branch_and_bound_with_heuristic[2]
generic_branch_and_bound_with_extended_set_sort_agenda_fn = generic_branch_and_bound_with_extended_set[2]
generic_a_star_sort_agenda_fn = generic_a_star[2]