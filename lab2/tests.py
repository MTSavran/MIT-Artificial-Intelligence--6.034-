# MIT 6.034 Lab 2: Search

from tester import make_test, get_tests

from lab2 import (generic_dfs, generic_bfs, generic_hill_climbing,
                  generic_best_first, generic_beam, generic_branch_and_bound,
                  generic_branch_and_bound_with_heuristic,
                  generic_branch_and_bound_with_extended_set, generic_a_star,
                  is_admissible, is_consistent, a_star,
                  TEST_GENERIC_BEAM, TEST_HEURISTICS)

from read_graphs import get_graphs
all_graphs = get_graphs()
GRAPH_0 = all_graphs['GRAPH_0']
GRAPH_1 = all_graphs['GRAPH_1']
GRAPH_2 = all_graphs['GRAPH_2']
GRAPH_3 = all_graphs['GRAPH_3']
GRAPH_FOR_HEURISTICS = all_graphs['GRAPH_FOR_HEURISTICS']

##########################################################################
### OFFLINE TESTS (HARDCODED ANSWERS)

#### PART 1: Helper Functions #########################################

make_test(type = 'FUNCTION',  #TEST 1
          getargs = [GRAPH_1, ['a', 'c', 'b', 'd']],
          testanswer = lambda val, original_val=None: val == 11,
          expected_val = 11,
          name = 'path_length')

make_test(type = 'FUNCTION',  #TEST 2
          getargs = [GRAPH_2, ['D', 'C', 'A', 'D', 'E', 'G', 'F']],
          testanswer = lambda val, original_val=None: val == 53,
          expected_val = 53,
          name = 'path_length')

make_test(type = 'FUNCTION',  #TEST 3
          getargs = [GRAPH_1, ['a']],
          testanswer = lambda val, original_val=None: val == 0,
          expected_val = 0,
          name = 'path_length')


make_test(type = 'FUNCTION',  #TEST 4
          getargs = [['node1', 'node3', 'node2']],
          testanswer = lambda val, original_val=None: val == False,
          expected_val = False,
          name = 'has_loops')

make_test(type = 'FUNCTION',  #TEST 5
          getargs = [['d', 'a', 'c', 'a', 'b']],
          testanswer = lambda val, original_val=None: val == True,
          expected_val = True,
          name = 'has_loops')

make_test(type = 'FUNCTION',  #TEST 6
          getargs = [list('SBCA')],
          testanswer = lambda val, original_val=None: val == False,
          expected_val = False,
          name = 'has_loops')

make_test(type = 'FUNCTION',  #TEST 7
          getargs = [['X']],
          testanswer = lambda val, original_val=None: val == False,
          expected_val = False,
          name = 'has_loops')


extensions_test1_answer = [['n2', 'n1'], ['n2', 'n3']]
make_test(type = 'FUNCTION',  #TEST 8
          getargs = [GRAPH_0, ['n2']],
          testanswer = lambda val, original_val=None: val == extensions_test1_answer,
          expected_val = extensions_test1_answer,
          name = 'extensions')

extensions_test2_answer = [['n2', 'n3', 'n4']]
make_test(type = 'FUNCTION',  #TEST 9
          getargs = [GRAPH_0, ['n2', 'n3']],
          testanswer = lambda val, original_val=None: val == extensions_test2_answer,
          expected_val = extensions_test2_answer,
          name = 'extensions')

extensions_test3_answer = [['S', 'A', 'C', 'E', 'D'],
                           ['S', 'A', 'C', 'E', 'F'],
                           ['S', 'A', 'C', 'E', 'G']]
make_test(type = 'FUNCTION',  #TEST 10
          getargs = [GRAPH_2, ['S', 'A', 'C', 'E']],
          testanswer = lambda val, original_val=None: val == extensions_test3_answer,
          expected_val = extensions_test3_answer,
          name = 'extensions')


sortby_test1_answer = ['c', 'a', 'b', 'd']
make_test(type = 'FUNCTION',  #TEST 11
          getargs = [GRAPH_1, 'c', ['d', 'a', 'b', 'c']],
          testanswer = lambda val, original_val=None: val == sortby_test1_answer,
          expected_val = sortby_test1_answer,
          name = 'sort_by_heuristic')

sortby_test2_answer = ['H', 'D', 'F', 'C', 'C', 'A', 'B']
make_test(type = 'FUNCTION',  #TEST 12
          getargs = [GRAPH_2, 'G', ['D', 'C', 'B', 'H', 'A', 'F', 'C']],
          testanswer = lambda val, original_val=None: val == sortby_test2_answer,
          expected_val = sortby_test2_answer,
          name = 'sort_by_heuristic')

sortby_test3_answer = ['G', 'X', 'Y', 'F']
make_test(type = 'FUNCTION',  #TEST 13
          getargs = [GRAPH_2, 'G', ['X', 'Y', 'G', 'F']],
          testanswer = lambda val, original_val=None: val == sortby_test3_answer,
          expected_val = sortby_test3_answer,
          name = 'sort_by_heuristic')


#### PART 2: Generic Search #######################################

search_args = {"dfs": generic_dfs,
               "bfs": generic_bfs,
               "hill_climbing": generic_hill_climbing,
               "best_first": generic_best_first,
               "beam": generic_beam,
               "branch_and_bound": generic_branch_and_bound,
               "branch_and_bound_with_heuristic": generic_branch_and_bound_with_heuristic,
               "branch_and_bound_with_extended_set": generic_branch_and_bound_with_extended_set,
               "a_star": generic_a_star}

# Tests 14-31
search_tests = [['dfs', GRAPH_1, 'a', 'd', 'abcd'],
                ['dfs', GRAPH_2, 'S', 'G', 'SACDEFG'],
                ['bfs', GRAPH_1, 'a', 'd', 'abd'],
                ['bfs', GRAPH_2, 'S', 'G', 'SACEG'],
#                ['hill_climbing', GRAPH_1, 'a', 'd', 'abcd'], #depends on lexicographic tie-breaking
                ['hill_climbing', GRAPH_2, 'S', 'G', 'SADHFG'],
#                ['best_first', GRAPH_1, 'a', 'd', 'abcd'], #depends on lexicographic tie-breaking
                ['best_first', GRAPH_2, 'S', 'G', 'SADEG'],
#                ['beam', GRAPH_1, 'a', 'd', 2, 'abd'], #depends on lexicographic tie-breaking
                ['beam', GRAPH_2, 'S', 'G', 2, 'SBYCEG'],
                ['beam', GRAPH_2, 'S', 'G', 1, 'SADHFG'],
                ['beam', GRAPH_2, 'S', 'G', 3, 'SADEG'],
                ['branch_and_bound', GRAPH_1, 'a', 'd', 'acd'],
                ['branch_and_bound', GRAPH_2, 'S', 'G', 'SBCEG'],
                ['branch_and_bound', GRAPH_3, 's', 'g', 'sxwg'],
                ['branch_and_bound_with_heuristic', GRAPH_1, 'a', 'd', 'acd'],
                ['branch_and_bound_with_heuristic', GRAPH_2, 'S', 'G', 'SBCEG'],
                ['branch_and_bound_with_heuristic', GRAPH_3, 's', 'g', 'szwg'],
                ['branch_and_bound_with_extended_set', GRAPH_1, 'a', 'd', 'acd'],
                ['branch_and_bound_with_extended_set', GRAPH_2, 'S', 'G', 'SBCEG'],
                ['branch_and_bound_with_extended_set', GRAPH_3, 's', 'g', 'sxwg'],
                ['a_star', GRAPH_1, 'a', 'd', 'acd'],
                ['a_star', GRAPH_2, 'S', 'G', 'SBCEG'],
                ['a_star', GRAPH_3, 's', 'g', 'sywg']]

def str_to_list(string):
    return [char for char in string]

for arg_list in search_tests:
    if arg_list[0] != 'beam':
        (lambda method, graph, startNode, endNode, answer_string :
         make_test(type = 'NESTED_FUNCTION',
                   getargs = [search_args[method], [graph, startNode, endNode]],
                   testanswer = (lambda val, original_val=None:
                                 val == str_to_list(answer_string)),
                   expected_val = str_to_list(answer_string),
                   name = 'generic_search')
         )(*arg_list[:5])

bb_extended_set_tests = [["generic_branch_and_bound", False],
                         ["generic_branch_and_bound_with_heuristic", False],
                         ["generic_branch_and_bound_with_extended_set", True]]

def get_bb_extended_testanswer_fn(answer):
    def bb_extended_testanswer(val, original_val=None):
        if val == [None, None, None, None]:
            raise NotImplementedError
        return val[3] == answer
    return bb_extended_testanswer

for arg_list in bb_extended_set_tests:  #Tests 32-34
    (lambda method, answer :
     make_test(type = 'VALUE',
               getargs = method,
               testanswer = get_bb_extended_testanswer_fn(answer),
               expected_val = "Correct boolean value indicating whether search uses extended set",
               name = method)
     )(*arg_list)


#### PART 3: Search Algorithms #########################################

# no-path-found tests with nonexistent goal node: #Tests 35-38
for search_method in ['dfs', 'bfs', 'branch_and_bound',
                      'branch_and_bound_with_extended_set']:
    (lambda method :
        make_test(type = 'FUNCTION',
                  getargs = [GRAPH_1, 'a', 'z'],
                  testanswer = (lambda val, original_val=None: val == None),
                  expected_val = None,
                  name = method)
    )(search_method)

# no-path-found test for beam:
make_test(type = 'FUNCTION',  #TEST 39
          getargs = [GRAPH_2, 'C', 'G', 1],
          testanswer = (lambda val, original_val=None: val == None),
          expected_val = None,
          name = 'beam')

# Tests 40-60
for arg_list in search_tests:
    if arg_list[0] == 'beam':
        (lambda method, graph, startNode, endNode, beam_width, answer_string :
         make_test(type = 'FUNCTION',
                   getargs = [graph, startNode, endNode, beam_width],
                   testanswer = (lambda val, original_val=None:
                                 val == str_to_list(answer_string)),
                   expected_val = str_to_list(answer_string),
                   name = method)
         )(*arg_list[:6])
    else:
        (lambda method, graph, startNode, endNode, answer_string :
         make_test(type = 'FUNCTION',
                   getargs = [graph, startNode, endNode],
                   testanswer = (lambda val, original_val=None:
                                 val == str_to_list(answer_string)),
                   expected_val = str_to_list(answer_string),
                   name = method)
         )(*arg_list[:5])


#### PART 4: Heuristics ###################################################

make_test(type = 'FUNCTION',  #TEST 61
          getargs = [GRAPH_1, 'd'],
          testanswer = lambda val, original_val=None: val == True,
          expected_val = True,
          name = 'is_admissible')

make_test(type = 'FUNCTION',  #TEST 62
          getargs = [GRAPH_1, 'c'],
          testanswer = lambda val, original_val=None: val == True,
          expected_val = True,
          name = 'is_admissible')

make_test(type = 'FUNCTION',  #TEST 63
          getargs = [GRAPH_2, 'G'],
          testanswer = lambda val, original_val=None: val == True,
          expected_val = True,
          name = 'is_admissible')

make_test(type = 'FUNCTION',  #TEST 64
          getargs = [GRAPH_3, 'g'],
          testanswer = lambda val, original_val=None: val == False,
          expected_val = False,
          name = 'is_admissible')


make_test(type = 'FUNCTION',  #TEST 65
          getargs = [GRAPH_1, 'd'],
          testanswer = lambda val, original_val=None: val == True,
          expected_val = True,
          name = 'is_consistent')

make_test(type = 'FUNCTION',  #TEST 66
          getargs = [GRAPH_1, 'c'],
          testanswer = lambda val, original_val=None: val == True,
          expected_val = True,
          name = 'is_consistent')

make_test(type = 'FUNCTION',  #TEST 67
          getargs = [GRAPH_2, 'G'],
          testanswer = lambda val, original_val=None: val == False,
          expected_val = False,
          name = 'is_consistent')

make_test(type = 'FUNCTION',  #TEST 68
          getargs = [GRAPH_3, 'g'],
          testanswer = lambda val, original_val=None: val == False,
          expected_val = False,
          name = 'is_consistent')


#### PART 5: Multiple Choice ###################################################

ANSWER_1_getargs = "ANSWER_1"
def ANSWER_1_testanswer(val, original_val = None):  #TEST 69
    if val == '':
        raise NotImplementedError
    return str(val) == '2'
make_test(type = 'VALUE',
          getargs = ANSWER_1_getargs,
          testanswer = ANSWER_1_testanswer,
          expected_val = "correct value of ANSWER_1 ('1', '2', '3', or '4')",
          name = ANSWER_1_getargs)

ANSWER_2_getargs = "ANSWER_2"
def ANSWER_2_testanswer(val, original_val = None):  #TEST 70
    if val == '':
        raise NotImplementedError
    return str(val) == '4'
make_test(type = 'VALUE',
          getargs = ANSWER_2_getargs,
          testanswer = ANSWER_2_testanswer,
          expected_val = "correct value of ANSWER_2 ('1', '2', '3', or '4')",
          name = ANSWER_2_getargs)

ANSWER_3_getargs = "ANSWER_3"
def ANSWER_3_testanswer(val, original_val = None):  #TEST 71
    if val == '':
        raise NotImplementedError
    return str(val) == '1'
make_test(type = 'VALUE',
          getargs = ANSWER_3_getargs,
          testanswer = ANSWER_3_testanswer,
          expected_val = "correct value of ANSWER_3 ('1', '2', '3', or '4')",
          name = ANSWER_3_getargs)

ANSWER_4_getargs = "ANSWER_4"
def ANSWER_4_testanswer(val, original_val = None):  #TEST 72
    if val == '':
        raise NotImplementedError
    return str(val) == '3'
make_test(type = 'VALUE',
          getargs = ANSWER_4_getargs,
          testanswer = ANSWER_4_testanswer,
          expected_val = "correct value of ANSWER_4 ('1', '2', '3', or '4')",
          name = ANSWER_4_getargs)


#### Optional tests ############################################################

if TEST_GENERIC_BEAM:

    for arg_list in search_tests:
        if arg_list[0] == 'beam':
            (lambda method, graph, startNode, endNode, beam_width, answer_string :
             make_test(type = 'NESTED_FUNCTION',
                       getargs = [search_args[method],
                                  [graph, startNode, endNode, beam_width]],
                       testanswer = (lambda val, original_val=None:
                                     val == str_to_list(answer_string)),
                       expected_val = str_to_list(answer_string),
                       name = 'generic_search')
             )(*arg_list[:6])


if TEST_HEURISTICS:

    def test_heuristic(heuristic_dict, should_be_admissible, should_be_consistent,
                       should_be_optimal_a_star):
        if None in heuristic_dict['G'].values(): return False
        shortest_path = ['S', 'A', 'C', 'G']
        GRAPH_FOR_HEURISTICS.set_heuristic(heuristic_dict)
        return (should_be_admissible == is_admissible(GRAPH_FOR_HEURISTICS, 'G')
                and (should_be_consistent == None
                     or should_be_consistent == is_consistent(GRAPH_FOR_HEURISTICS, 'G'))
                and (should_be_optimal_a_star == None
                     or (should_be_optimal_a_star == (a_star(GRAPH_FOR_HEURISTICS, 'S', 'G')
                                                      == shortest_path))))

    make_test(type = 'VALUE',
              getargs = 'heuristic_1',
              testanswer = (lambda val, original_val=None:
                            test_heuristic(val, True, True, None)),
              expected_val = 'Correct numerical values for heuristic to fit specifications',
              name = 'heuristic_1')

    make_test(type = 'VALUE',
              getargs = 'heuristic_2',
              testanswer = (lambda val, original_val=None:
                            test_heuristic(val, True, False, None)),
              expected_val = 'Correct numerical values for heuristic to fit specifications',
              name = 'heuristic_2')

    make_test(type = 'VALUE',
              getargs = 'heuristic_3',
              testanswer = (lambda val, original_val=None:
                            test_heuristic(val, True, None, False)),
              expected_val = 'Correct numerical values for heuristic to fit specifications',
              name = 'heuristic_3')

    make_test(type = 'VALUE',
              getargs = 'heuristic_4',
              testanswer = (lambda val, original_val=None:
                            test_heuristic(val, True, False, True)),
              expected_val = 'Correct numerical values for heuristic to fit specifications',
              name = 'heuristic_4')
