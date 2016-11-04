# MIT 6.034 Lab 5: k-Nearest Neighbors and Identification Trees

from tester import make_test, get_tests
from data import *
from lab5 import euclidean_distance, manhattan_distance, hamming_distance, cosine_distance
import random

def random_list(length, minval=-100, maxval=100):
    return [ random.randint(minval,maxval) for x in xrange(length) ]

def approx_equal(a, b, epsilon=0.001):
    return abs(a-b) <= epsilon

def compare_list_contents(list1, list2):
    try:
        assert len(list1) == len(list2)
        list1_copy = list1[:]
        for item in list2:
            list1_copy.remove(item)
        return True
    except Exception:
        return False

################################################################################
############################# IDENTIFICATION TREES #############################
################################################################################

_ft_tt = feature_test("tree_type") #lazy alias

#id_tree_classify_point
#leaf-node tree -> classification
def id_tree_classify_point_0_getargs() :  #TEST 1
    return [{"name":"Saphira", "color":"sapphire-blue"},
            IDTNode(feature_test("species")).set_node_classification("dragon")]
def id_tree_classify_point_0_testanswer(val, original_val = None) :
    return val == "dragon"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = id_tree_classify_point_0_getargs,
          testanswer = id_tree_classify_point_0_testanswer,
          expected_val = "dragon",
          name = 'id_tree_classify_point')

#leaf-node tree with no data (degenerate case) -> classification
def id_tree_classify_point_1_getargs() :  #TEST 2
    return [{"name":"Saphira", "color":"sapphire-blue"},
            IDTNode(feature_test("gender")).set_node_classification("female")]
def id_tree_classify_point_1_testanswer(val, original_val = None) :
    return val == "female"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = id_tree_classify_point_1_getargs,
          testanswer = id_tree_classify_point_1_testanswer,
          expected_val = "female",
          name = 'id_tree_classify_point')

#stump -> apply classifier
#classify a point using the bottom section of the angels tree from 2012 Q2
def id_tree_classify_point_2_getargs() :  #TEST 3
    return [{"name":"test-point", "Height":10},
            get_angel_tree()._children["Human"]._children["Copper"]]
def id_tree_classify_point_2_testanswer(val, original_val = None) :
    return val == "Angel"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = id_tree_classify_point_2_getargs,
          testanswer = id_tree_classify_point_2_testanswer,
          expected_val = "Angel",
          name = 'id_tree_classify_point')

#multi-level tree, with non-binary tests
#from 2014 Q2, page 5
def id_tree_classify_point_3_getargs() :  #TEST 4
    return [deepcopy(tree_test_point), get_tree_tree()]
def id_tree_classify_point_3_testanswer(val, original_val = None) :
    return val == "Maple"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = id_tree_classify_point_3_getargs,
          testanswer = id_tree_classify_point_3_testanswer,
          expected_val = "Maple",
          name = 'id_tree_classify_point')

#many-level tree
#numeric ID tree from 2013 Q2
def id_tree_classify_point_4_getargs() :  #TEST 5
    return [{"class":'A', "X":2.1, "Y":1.1}, get_numeric_tree()]
def id_tree_classify_point_4_testanswer(val, original_val = None) :
    return val == "B"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = id_tree_classify_point_4_getargs,
          testanswer = id_tree_classify_point_4_testanswer,
          expected_val = "B",
          name = 'id_tree_classify_point')


##split_on_classifier
#one point -> {feature: [point]}
def split_on_classifier_0_getargs() :  #TEST 6
    return [[{'animal':'hippo','color':'blue'}], feature_test('animal')]
def split_on_classifier_0_testanswer(val, original_val = None) :
    return val == {'hippo': [{'animal': 'hippo', 'color': 'blue'}]}
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = split_on_classifier_0_getargs,
          testanswer = split_on_classifier_0_testanswer,
          expected_val = str({'hippo': [{'animal': 'hippo', 'color': 'blue'}]}),
          name = 'split_on_classifier')

#tree_data, has_leaves -> {Yes: (6 points)}
def split_on_classifier_1_getargs() :  #TEST 7
    return [deepcopy(tree_data), feature_test("has_leaves")]
def split_on_classifier_1_testanswer(val, original_val = None) :
    try:
        assert len(val) == 1
        return sorted(val['Yes']) == sorted(tree_data)
    except Exception:
        return False
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = split_on_classifier_1_getargs,
          testanswer = split_on_classifier_1_testanswer,
          expected_val = "{'Yes': (list of 6 points)}",
          name = 'split_on_classifier')

#tree_data, tree_type -> two classes
def split_on_classifier_2_getargs() :  #TEST 8
    return [deepcopy(tree_data), _ft_tt]
def split_on_classifier_2_testanswer(val, original_val = None) :
    try:
        assert len(val) == 2
        assert sorted(val['Oak']) == sorted(tree_data[:3])
        assert sorted(val['Maple']) == sorted(tree_data[3:])
        return True
    except Exception:
        return False
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = split_on_classifier_2_getargs,
          testanswer = split_on_classifier_2_testanswer,
          expected_val = "{'Oak': (list of 3 points), 'Maple': (list of 3 points)}",
          name = 'split_on_classifier')

#angel_data, Height > 7 -> two classes
def split_on_classifier_3_getargs() :  #TEST 9
    return [deepcopy(angel_data), threshold_test("Height", 7)]
def split_on_classifier_3_testanswer(val, original_val = None) :
    try:
        assert len(val) == 2
        assert sorted(val['No']) == sorted(angel_data[:4])
        assert sorted(val['Yes']) == sorted(angel_data[4:])
        return True
    except Exception:
        return False
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = split_on_classifier_3_getargs,
          testanswer = split_on_classifier_3_testanswer,
          expected_val = "{'Yes': (list of 2 points), 'No': (list of 4 points)}",
          name = 'split_on_classifier')

#tree_data, bark_texture -> 3 classes
def split_on_classifier_4_getargs() :  #TEST 10
    return [deepcopy(tree_data), feature_test("bark_texture")]
def split_on_classifier_4_testanswer(val, original_val = None) :
    try:
        assert len(val) == 3
        assert sorted(val['Smooth']) == sorted(tree_data[4:6])
        assert sorted(val['Glossy']) == sorted(tree_data[0:1])
        assert sorted(val['Furrowed']) == sorted(tree_data[1:4])
        return True
    except Exception:
        return False
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = split_on_classifier_4_getargs,
          testanswer = split_on_classifier_4_testanswer,
          expected_val = "{'Smooth': (list of 1 point), 'Glossy': (list of 3 points), 'Furrowed': (list of 2 points)}",
          name = 'split_on_classifier')

#numeric_data, X+Y < 4.5 (custom test) -> 2 classes
def split_on_classifier_5_getargs() :  #TEST 11
    return [deepcopy(numeric_data), Classifier("X+Y < 4.5", lambda p:p['X']+p['Y']<4.5)]
def split_on_classifier_5_testanswer(val, original_val = None) :
    try:
        assert len(val) == 2
        assert sorted(val[True]) == sorted(numeric_data[0:4]+numeric_data[5:8])
        assert sorted(val[False]) == sorted([numeric_data[4], numeric_data[8]])
        return True
    except Exception:
        return False
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = split_on_classifier_5_getargs,
          testanswer = split_on_classifier_5_testanswer,
          expected_val = "{True: (list of 7 points), False: (list of 2 points)}",
          name = 'split_on_classifier')


#branch_disorder
#one point -> 0
def branch_disorder_0_getargs() :  #TEST 12
    return [[{'animal':'hippo','color':'blue'}], feature_test('animal')]
def branch_disorder_0_testanswer(val, original_val = None) :
    return val == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = branch_disorder_0_getargs,
          testanswer = branch_disorder_0_testanswer,
          expected_val = "0",
          name = 'branch_disorder')

#['+', '-', '-', '+'] -> 1
def branch_disorder_1_getargs() :  #TEST 13
    return [[{'sign':s} for s in ['+', '-', '-', '+']], feature_test('sign')]
def branch_disorder_1_testanswer(val, original_val = None) :
    return val == 1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = branch_disorder_1_getargs,
          testanswer = branch_disorder_1_testanswer,
          expected_val = "1",
          name = 'branch_disorder')

#['giraffe', 'giraffe', 'giraffe', 'giraffe'] -> 0
def branch_disorder_2_getargs() :  #TEST 14
    return [[{'species':'giraffe', 'name':name} for name in ['Willie','Gerald','Abigail','Geoffrey']],
             feature_test('species')]
def branch_disorder_2_testanswer(val, original_val = None) :
    return val == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = branch_disorder_2_getargs,
          testanswer = branch_disorder_2_testanswer,
          expected_val = "0",
          name = 'branch_disorder')

#['Oak', 'Oak', 'Maple'] -> ~0.9
def branch_disorder_3_getargs() :  #TEST 15
    return [deepcopy(tree_data_furrowed), feature_test('tree_type')]
def branch_disorder_3_testanswer(val, original_val = None) :
    return approx_equal(val, 0.9183)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = branch_disorder_3_getargs,
          testanswer = branch_disorder_3_testanswer,
          expected_val = "~0.9183",
          name = 'branch_disorder')

#[2, 2, 2, 5, 2, 2, 2, 2, 5, 2] -> ~0.72
def branch_disorder_4_getargs() :  #TEST 16
    return [[{'x':n} for n in [2, 2, 2, 5, 2, 2, 2, 2, 5, 2]], feature_test('x')]
def branch_disorder_4_testanswer(val, original_val = None) :
    return approx_equal(val, 0.7219)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = branch_disorder_4_getargs,
          testanswer = branch_disorder_4_testanswer,
          expected_val = "~0.7219",
          name = 'branch_disorder')

#['x', 'y', 'z'] -> ~1.585 (> 2 classes)
def branch_disorder_5_getargs() :  #TEST 17
    return [[{'class':n} for n in list('xyz')], feature_test('class')]
def branch_disorder_5_testanswer(val, original_val = None) :
    return approx_equal(val, 1.585)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = branch_disorder_5_getargs,
          testanswer = branch_disorder_5_testanswer,
          expected_val = "~1.585",
          name = 'branch_disorder')


#average_test_disorder
#[[1, 1, -1], [-1, 1, -1]] -> ~0.91829
def average_test_disorder_0_getargs() :  #TEST 18
    return [deepcopy(angel_data), feature_test("Material"), feature_test('Classification')]
def average_test_disorder_0_testanswer(val, original_val = None) :
    return approx_equal(val, 0.91829)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = average_test_disorder_0_getargs,
          testanswer = average_test_disorder_0_testanswer,
          expected_val = "~0.91829",
          name = 'average_test_disorder')

#[list('OOMMM'), ['O']] -> ~0.80913
def average_test_disorder_1_getargs() :  #TEST 19
    return [deepcopy(tree_data), feature_test("leaf_shape"), feature_test('tree_type')]
def average_test_disorder_1_testanswer(val, original_val = None) :
    return approx_equal(val, 0.80913)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = average_test_disorder_1_getargs,
          testanswer = average_test_disorder_1_testanswer,
          expected_val = "~0.80913",
          name = 'average_test_disorder')

#[["O"], list("OOM"), list("MM")] -> ~0.45915
def average_test_disorder_2_getargs() :  #TEST 20
    return [deepcopy(tree_data), feature_test("bark_texture"), feature_test('tree_type')]
def average_test_disorder_2_testanswer(val, original_val = None) :
    return approx_equal(val, 0.45915)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = average_test_disorder_2_getargs,
          testanswer = average_test_disorder_2_testanswer,
          expected_val = "~0.45915",
          name = 'average_test_disorder')

#[list('OOOMMM')] -> 1.0
def average_test_disorder_3_getargs() :  #TEST 21
    return [deepcopy(tree_data), feature_test("has_leaves"), feature_test('tree_type')]
def average_test_disorder_3_testanswer(val, original_val = None) :
    return val == 1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = average_test_disorder_3_getargs,
          testanswer = average_test_disorder_3_testanswer,
          expected_val = "1",
          name = 'average_test_disorder')

#[list('xxxxxxxxxxxxx')] -> 0.0
def average_test_disorder_4_getargs() :  #TEST 22
    return [[{'class':'x', 'value':0, 'name':str(i)} for i in range(14)],
            feature_test('value'), feature_test('class')]
def average_test_disorder_4_testanswer(val, original_val = None) :
    return val == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = average_test_disorder_4_getargs,
          testanswer = average_test_disorder_4_testanswer,
          expected_val = "0",
          name = 'average_test_disorder')


#find_best_classifier
#find_best_classifier(tree_data, tree_classifiers, "tree_type") -> bark_texture
def find_best_classifier_0_getargs() :  #TEST 23
    return [deepcopy(tree_data), deepcopy(tree_classifiers), feature_test("tree_type")]
def find_best_classifier_0_testanswer(val, original_val = None) :
    return val.name == "bark_texture"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = find_best_classifier_0_getargs,
          testanswer = find_best_classifier_0_testanswer,
          expected_val = "Classifier<bark_texture>",
          name = 'find_best_classifier')

#tree_data, "bark_texture" -> ?? (use diff attribute as target_classification)
def find_best_classifier_1_getargs() :  #TEST 24
    return [deepcopy(tree_data), deepcopy(tree_classifiers_reverse), feature_test("bark_texture")]
def find_best_classifier_1_testanswer(val, original_val = None) :
    return val.name == "tree_type"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = find_best_classifier_1_getargs,
          testanswer = find_best_classifier_1_testanswer,
          expected_val = "Classifier<tree_type>",
          name = 'find_best_classifier')

#subset of tree_data from bark_texture=furrowed -> orange_foliage
def find_best_classifier_2_getargs() :  #TEST 25
    return [deepcopy(tree_data_furrowed), deepcopy(tree_classifiers), _ft_tt]
def find_best_classifier_2_testanswer(val, original_val = None) :
    return val.name == "orange_foliage"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = find_best_classifier_2_getargs,
          testanswer = find_best_classifier_2_testanswer,
          expected_val = "Classifier<orange_foliage>",
          name = 'find_best_classifier')

#no good classifiers (eg tree_impossible) -> raise error
def find_best_classifier_3_getargs() :  #TEST 26
    return [deepcopy(tree_data_furrowed_pointy), deepcopy(tree_classifiers_impossible), _ft_tt]
def find_best_classifier_3_testanswer(val, original_val = None) :
    return val == NoGoodClassifiersError
make_test(type = 'FUNCTION_ENCODED_ARGS_EXPECTING_EXCEPTION',
          getargs = find_best_classifier_3_getargs,
          testanswer = find_best_classifier_3_testanswer,
          expected_val = "NoGoodClassifiersError",
          name = 'find_best_classifier')

#best classifier has disorder > 1, but still useful -> choose anyway
def find_best_classifier_4_getargs() :  #TEST 27
    return [deepcopy(toy_data_2), deepcopy(toy_classifiers_2), feature_test("class")]
def find_best_classifier_4_testanswer(val, original_val = None) :
    return val.name == "flavor"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = find_best_classifier_4_getargs,
          testanswer = find_best_classifier_4_testanswer,
          expected_val = "Classifier<flavor>",
          name = 'find_best_classifier')

#tie-breaking: prefer earlier classifier even if alphabetically later
def find_best_classifier_5_getargs() :  #TEST 28
    return [deepcopy(toy_data_1), deepcopy(toy_classifiers_1), feature_test("class")]
def find_best_classifier_5_testanswer(val, original_val = None) :
    return val.name == "attr2"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = find_best_classifier_5_getargs,
          testanswer = find_best_classifier_5_testanswer,
          expected_val = "Classifier<attr2>",
          name = 'find_best_classifier')

#numeric tests
def find_best_classifier_6_getargs() :  #TEST 29
    return [deepcopy(numeric_data), deepcopy(numeric_classifiers), feature_test("class")]
def find_best_classifier_6_testanswer(val, original_val = None) :
    return val.name == "Y > 1"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = find_best_classifier_6_getargs,
          testanswer = find_best_classifier_6_testanswer,
          expected_val = "Classifier<Y > 1>",
          name = 'find_best_classifier')


#construct_greedy_id_tree
#homogeneous data -> instantiate node and add classification
def construct_greedy_id_tree_0_getargs() :  #TEST 30
    return [deepcopy(tree_data[0:1]), deepcopy(tree_classifiers), _ft_tt]
construct_greedy_id_tree_0_expected = IDTNode(_ft_tt).set_node_classification("Oak")
def construct_greedy_id_tree_0_testanswer(val, original_val = None) :
    return val == construct_greedy_id_tree_0_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = construct_greedy_id_tree_0_getargs,
          testanswer = construct_greedy_id_tree_0_testanswer,
          expected_val = "Single-node tree with Oak classification:" + str(construct_greedy_id_tree_0_expected),
          name = 'construct_greedy_id_tree')

#leaf node -> just add classification
def construct_greedy_id_tree_0t_getargs() :  #TEST 31
    tree = IDTNode(_ft_tt, "Glossy")
    return [deepcopy(tree_data[0:1]), deepcopy(tree_classifiers), _ft_tt, tree]
construct_greedy_id_tree_0t_expected = IDTNode(_ft_tt, "Glossy").set_node_classification("Oak")
def construct_greedy_id_tree_0t_testanswer(val, original_val = None) :
    return val == construct_greedy_id_tree_0t_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = construct_greedy_id_tree_0t_getargs,
          testanswer = construct_greedy_id_tree_0t_testanswer,
          expected_val = "Input tree, with Oak classification added:" + str(construct_greedy_id_tree_0t_expected),
          name = 'construct_greedy_id_tree')

#one-level tree -> add one classifier and its classifications
#tree_tree after bark_texture=furrowed -> add classifier orange_foliage, then add Oak and Maple at leaves
def construct_greedy_id_tree_1t_getargs() :  #TEST 32
    tree = IDTNode(_ft_tt, "Furrowed")
    return [deepcopy(tree_data_furrowed), deepcopy(tree_classifiers), _ft_tt, tree]
construct_greedy_id_tree_1t_expected = get_tree_tree()._children["Furrowed"]
def construct_greedy_id_tree_1t_testanswer(val, original_val = None) :
    return val == construct_greedy_id_tree_1t_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = construct_greedy_id_tree_1t_getargs,
          testanswer = construct_greedy_id_tree_1t_testanswer,
          expected_val = "Input tree, with orange_foliage classifier and leaf classifications added:" + str(construct_greedy_id_tree_1t_expected),
          name = 'construct_greedy_id_tree')

#same as above, but also instantiate new tree
def construct_greedy_id_tree_1_getargs() :  #TEST 33
    return [deepcopy(tree_data_furrowed), deepcopy(tree_classifiers), _ft_tt]
construct_greedy_id_tree_1_expected = get_tree_tree()._children["Furrowed"]
construct_greedy_id_tree_1_expected._parent_branch_name = None
def construct_greedy_id_tree_1_testanswer(val, original_val = None) :
    return val == construct_greedy_id_tree_1_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = construct_greedy_id_tree_1_getargs,
          testanswer = construct_greedy_id_tree_1_testanswer,
          expected_val = "Tree with depth 1:" + str(construct_greedy_id_tree_1_expected),
          name = 'construct_greedy_id_tree')

#tree_tree
def construct_greedy_id_tree_2_getargs() :  #TEST 34
    return [deepcopy(tree_data), deepcopy(tree_classifiers), _ft_tt]
def construct_greedy_id_tree_2_testanswer(val, original_val = None) :
    return val == get_tree_tree()
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = construct_greedy_id_tree_2_getargs,
          testanswer = construct_greedy_id_tree_2_testanswer,
          expected_val = "Greedy ID tree from 2014 Q2:" + str(get_tree_tree()),
          name = 'construct_greedy_id_tree')

#tree_tree_impossible (2014 Q2 without orange_foliage test)
def construct_greedy_id_tree_3_getargs() :  #TEST 35
    return [deepcopy(tree_data), deepcopy(tree_classifiers_impossible), _ft_tt]
def construct_greedy_id_tree_3_testanswer(val, original_val = None) :
    return val == get_tree_tree_impossible()
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = construct_greedy_id_tree_3_getargs,
          testanswer = construct_greedy_id_tree_3_testanswer,
          expected_val = "Greedy ID tree from 2014 Q2, but without orange_foliage test:" + str(get_tree_tree_impossible()),
          name = 'construct_greedy_id_tree')

#angel_tree
def construct_greedy_id_tree_4_getargs() :  #TEST 36
    return [deepcopy(angel_data), deepcopy(angel_classifiers), feature_test("Classification")]
def construct_greedy_id_tree_4_testanswer(val, original_val = None) :
    return val == get_angel_tree()
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = construct_greedy_id_tree_4_getargs,
          testanswer = construct_greedy_id_tree_4_testanswer,
          expected_val = "Greedy ID tree from 2012 Q2:" + str(get_angel_tree()),
          name = 'construct_greedy_id_tree')

#numeric_tree
def construct_greedy_id_tree_5_getargs() :  #TEST 37
    return [deepcopy(numeric_data), deepcopy(numeric_classifiers), feature_test("class")]
def construct_greedy_id_tree_5_testanswer(val, original_val = None) :
    return val == get_numeric_tree()
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = construct_greedy_id_tree_5_getargs,
          testanswer = construct_greedy_id_tree_5_testanswer,
          expected_val = "Greedy ID tree from 2013 Q2:" + str(get_numeric_tree()),
          name = 'construct_greedy_id_tree')

#ANSWER_1: bark_texture has the lowest disorder, ~0.46
ANSWER_1_getargs = 'ANSWER_1'  #TEST 38
def ANSWER_1_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 'bark_texture'
make_test(type = 'VALUE',
          getargs = ANSWER_1_getargs,
          testanswer = ANSWER_1_testanswer,
          expected_val = "the correct classifier name, as a string",
          name = ANSWER_1_getargs)

#ANSWER_2: leaf_shape has the second lowest disorder, ~0.81
ANSWER_2_getargs = 'ANSWER_2'  #TEST 39
def ANSWER_2_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 'leaf_shape'
make_test(type = 'VALUE',
          getargs = ANSWER_2_getargs,
          testanswer = ANSWER_2_testanswer,
          expected_val = "the correct classifier name, as a string",
          name = ANSWER_2_getargs)

#ANSWER_3: orange_foliage is perfectly homogeneous (disorder = 0) for the
# branch bark_texture=Furrowed.
ANSWER_3_getargs = 'ANSWER_3'  #TEST 40
def ANSWER_3_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 'orange_foliage'
make_test(type = 'VALUE',
          getargs = ANSWER_3_getargs,
          testanswer = ANSWER_3_testanswer,
          expected_val = "the correct classifier name, as a string",
          name = ANSWER_3_getargs)

#ANSWER_4: Tree 1 misclassifies the last training point. Trees 2 and 3 each
# classify all seven training points correctly.
ANSWER_4_getargs = 'ANSWER_4'  #TEST 41
def ANSWER_4_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == [2,3]
make_test(type = 'VALUE',
          getargs = ANSWER_4_getargs,
          testanswer = ANSWER_4_testanswer,
          expected_val = "a list of ints, such as [1,2]",
          name = ANSWER_4_getargs)

#ANSWER_5: Initially, the feature test for C has the lowest disorder, so the
# greedy algorithm will pick C as the first classifier.
ANSWER_5_getargs = 'ANSWER_5'  #TEST 42
def ANSWER_5_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == [3]
make_test(type = 'VALUE',
          getargs = ANSWER_5_getargs,
          testanswer = ANSWER_5_testanswer,
          expected_val = "a list of ints, such as [1,2]",
          name = ANSWER_5_getargs)

#ANSWER_6: Tree 1 misclassifies XOR(1,1)=0, and Tree 3 may misclassify
# XOR(1,0)=1 or XOR(1,1)=0, depending on the value of the distractor feature C.
# Tree 2 computes XOR correctly.
ANSWER_6_getargs = 'ANSWER_6'  #TEST 43
def ANSWER_6_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == [2]
make_test(type = 'VALUE',
          getargs = ANSWER_6_getargs,
          testanswer = ANSWER_6_testanswer,
          expected_val = "a list of ints, such as [1,2]",
          name = ANSWER_6_getargs)

#ANSWER_7: Occam's Razor says that simpler trees are more likely to produce
# accurate results.
ANSWER_7_getargs = 'ANSWER_7'  #TEST 44
def ANSWER_7_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 2
make_test(type = 'VALUE',
          getargs = ANSWER_7_getargs,
          testanswer = ANSWER_7_testanswer,
          expected_val = "the integer 1, 2, or 3, representing the best answer",
          name = ANSWER_7_getargs)

#ANSWER_8: For example, ANSWER_2 != ANSWER_3
ANSWER_8_getargs = 'ANSWER_8'  #TEST 45
def ANSWER_8_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    try:
        return val[0] in 'nN'
    except:
        return False
make_test(type = 'VALUE',
          getargs = ANSWER_8_getargs,
          testanswer = ANSWER_8_testanswer,
          expected_val = "the string 'Yes' or 'No'",
          name = ANSWER_8_getargs)

#ANSWER_9: For example, Tree 2 was simpler than the greedy tree (Tree 3), yet
# both correctly classified the training data.
ANSWER_9_getargs = 'ANSWER_9'  #TEST 46
def ANSWER_9_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    try:
        return val[0] in 'nN'
    except:
        return False
make_test(type = 'VALUE',
          getargs = ANSWER_9_getargs,
          testanswer = ANSWER_9_testanswer,
          expected_val = "the string 'Yes' or 'No'",
          name = ANSWER_9_getargs)


################################################################################
############################# k-NEAREST NEIGHBORS ##############################
################################################################################

#BOUNDARY_ANS_1
BOUNDARY_ANS_1_getargs = 'BOUNDARY_ANS_1'  #TEST 47
def BOUNDARY_ANS_1_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 3
make_test(type = 'VALUE',
          getargs = BOUNDARY_ANS_1_getargs,
          testanswer = BOUNDARY_ANS_1_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = BOUNDARY_ANS_1_getargs)

#BOUNDARY_ANS_2
BOUNDARY_ANS_2_getargs = 'BOUNDARY_ANS_2'  #TEST 48
def BOUNDARY_ANS_2_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 4
make_test(type = 'VALUE',
          getargs = BOUNDARY_ANS_2_getargs,
          testanswer = BOUNDARY_ANS_2_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = BOUNDARY_ANS_2_getargs)

#BOUNDARY_ANS_3
BOUNDARY_ANS_3_getargs = 'BOUNDARY_ANS_3'  #TEST 49
def BOUNDARY_ANS_3_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 1
make_test(type = 'VALUE',
          getargs = BOUNDARY_ANS_3_getargs,
          testanswer = BOUNDARY_ANS_3_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = BOUNDARY_ANS_3_getargs)

#BOUNDARY_ANS_4
BOUNDARY_ANS_4_getargs = 'BOUNDARY_ANS_4'  #TEST 50
def BOUNDARY_ANS_4_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 2
make_test(type = 'VALUE',
          getargs = BOUNDARY_ANS_4_getargs,
          testanswer = BOUNDARY_ANS_4_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = BOUNDARY_ANS_4_getargs)

#BOUNDARY_ANS_5
BOUNDARY_ANS_5_getargs = 'BOUNDARY_ANS_5'  #TEST 51
def BOUNDARY_ANS_5_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 2
make_test(type = 'VALUE',
          getargs = BOUNDARY_ANS_5_getargs,
          testanswer = BOUNDARY_ANS_5_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = BOUNDARY_ANS_5_getargs)

#BOUNDARY_ANS_6: Valid ID tree boundaries, but not greedy disorder-minizing
BOUNDARY_ANS_6_getargs = 'BOUNDARY_ANS_6'  #TEST 52
def BOUNDARY_ANS_6_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 4
make_test(type = 'VALUE',
          getargs = BOUNDARY_ANS_6_getargs,
          testanswer = BOUNDARY_ANS_6_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = BOUNDARY_ANS_6_getargs)

#BOUNDARY_ANS_7
BOUNDARY_ANS_7_getargs = 'BOUNDARY_ANS_7'  #TEST 53
def BOUNDARY_ANS_7_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 1
make_test(type = 'VALUE',
          getargs = BOUNDARY_ANS_7_getargs,
          testanswer = BOUNDARY_ANS_7_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = BOUNDARY_ANS_7_getargs)

#BOUNDARY_ANS_8: Boundaries should never intersect training points!
BOUNDARY_ANS_8_getargs = 'BOUNDARY_ANS_8'  #TEST 54
def BOUNDARY_ANS_8_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 4
make_test(type = 'VALUE',
          getargs = BOUNDARY_ANS_8_getargs,
          testanswer = BOUNDARY_ANS_8_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = BOUNDARY_ANS_8_getargs)

#BOUNDARY_ANS_9: Don't draw kNN boundaries between neighboring points of the
# same class.  (If the three A's were all different classes, however, the
# boundaries would be correct.)
BOUNDARY_ANS_9_getargs = 'BOUNDARY_ANS_9'  #TEST 55
def BOUNDARY_ANS_9_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 4
make_test(type = 'VALUE',
          getargs = BOUNDARY_ANS_9_getargs,
          testanswer = BOUNDARY_ANS_9_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = BOUNDARY_ANS_9_getargs)

#BOUNDARY_ANS_10: The data isn't even separated -- the outer region contains
# both A and B points!
BOUNDARY_ANS_10_getargs = 'BOUNDARY_ANS_10'  #TEST 56
def BOUNDARY_ANS_10_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 4
make_test(type = 'VALUE',
          getargs = BOUNDARY_ANS_10_getargs,
          testanswer = BOUNDARY_ANS_10_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = BOUNDARY_ANS_10_getargs)

#BOUNDARY_ANS_11
BOUNDARY_ANS_11_getargs = 'BOUNDARY_ANS_11'  #TEST 57
def BOUNDARY_ANS_11_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 2
make_test(type = 'VALUE',
          getargs = BOUNDARY_ANS_11_getargs,
          testanswer = BOUNDARY_ANS_11_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = BOUNDARY_ANS_11_getargs)

#BOUNDARY_ANS_12
BOUNDARY_ANS_12_getargs = 'BOUNDARY_ANS_12'  #TEST 58
def BOUNDARY_ANS_12_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 1
make_test(type = 'VALUE',
          getargs = BOUNDARY_ANS_12_getargs,
          testanswer = BOUNDARY_ANS_12_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = BOUNDARY_ANS_12_getargs)

#BOUNDARY_ANS_13
BOUNDARY_ANS_13_getargs = 'BOUNDARY_ANS_13'  #TEST 59
def BOUNDARY_ANS_13_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 4
make_test(type = 'VALUE',
          getargs = BOUNDARY_ANS_13_getargs,
          testanswer = BOUNDARY_ANS_13_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = BOUNDARY_ANS_13_getargs)

#BOUNDARY_ANS_14
BOUNDARY_ANS_14_getargs = 'BOUNDARY_ANS_14'  #TEST 60
def BOUNDARY_ANS_14_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 4
make_test(type = 'VALUE',
          getargs = BOUNDARY_ANS_14_getargs,
          testanswer = BOUNDARY_ANS_14_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = BOUNDARY_ANS_14_getargs)


## dot_product
def dot_product_0_getargs() :  #TEST 61
    return [(3, -7), [2.5, 10]]
def dot_product_0_testanswer(val, original_val = None) :
    return val == -62.5
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = dot_product_0_getargs,
          testanswer = dot_product_0_testanswer,
          expected_val = "-62.5",
          name = 'dot_product')

def dot_product_1_getargs() :  #TEST 62
    return [[4], (5,)]
def dot_product_1_testanswer(val, original_val = None) :
    return val == 20
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = dot_product_1_getargs,
          testanswer = dot_product_1_testanswer,
          expected_val = "20",
          name = 'dot_product')

def dot_product_2_getargs() :  #TEST 63
    return [(1,2,3,4,2), (1, 10, 1000, 100, 10000)]
def dot_product_2_testanswer(val, original_val = None) :
    return val == 23421
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = dot_product_2_getargs,
          testanswer = dot_product_2_testanswer,
          expected_val = "23421",
          name = 'dot_product')


## norm
def norm_0_getargs() :  #TEST 64
    return [(-3, 4)]
def norm_0_testanswer(val, original_val = None) :
    return val == 5
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = norm_0_getargs,
          testanswer = norm_0_testanswer,
          expected_val = "5",
          name = 'norm')

def norm_1_getargs() :  #TEST 65
    return [(17.2,)]
def norm_1_testanswer(val, original_val = None) :
    return val == 17.2
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = norm_1_getargs,
          testanswer = norm_1_testanswer,
          expected_val = "17.2",
          name = 'norm')

def norm_2_getargs() :  #TEST 66
    return [[6, 2, 11, -2, 2]]
def norm_2_testanswer(val, original_val = None) :
    return val == 13
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = norm_2_getargs,
          testanswer = norm_2_testanswer,
          expected_val = "13",
          name = 'norm')


## euclidean_distance
def euclidean_distance_0_getargs() :  #TEST 67
    return [ Point((0,0)), Point((3,4)) ]
def euclidean_distance_0_testanswer(val, original_val = None) :
    return approx_equal(val, 5)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = euclidean_distance_0_getargs,
          testanswer = euclidean_distance_0_testanswer,
          expected_val = "5",
          name = 'euclidean_distance')

def euclidean_distance_1_getargs() :  #TEST 68
    return [ Point([-1,2,1], "A"), Point([-4,5,-2], "B") ]
def euclidean_distance_1_testanswer(val, original_val = None) :
    return approx_equal(val, 5.1962)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = euclidean_distance_1_getargs,
          testanswer = euclidean_distance_1_testanswer,
          expected_val = "~5.1962",
          name = 'euclidean_distance')

euclidean_distance_2_random_inputs = [random_list(1), random_list(1)]
def euclidean_distance_2_getargs() :  #TEST 69
    return [Point(rlist) for rlist in euclidean_distance_2_random_inputs]
def euclidean_distance_2_testanswer(val, original_val = None) :
    return approx_equal(val,sum(map(lambda(a,b):(a-b)**2,zip(*euclidean_distance_2_random_inputs)))**0.5)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = euclidean_distance_2_getargs,
          testanswer = euclidean_distance_2_testanswer,
          expected_val = '(this test uses randomly generated 1-dimensional Points)',
          name = 'euclidean_distance')

euclidean_distance_3_random_inputs = [random_list(5), random_list(5)]
def euclidean_distance_3_getargs() :  #TEST 70
    return [Point(rlist) for rlist in euclidean_distance_3_random_inputs]
def euclidean_distance_3_testanswer(val, original_val = None) :
    return approx_equal(val,sum(map(lambda(a,b):(a-b)**2,zip(*euclidean_distance_3_random_inputs)))**0.5)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = euclidean_distance_3_getargs,
          testanswer = euclidean_distance_3_testanswer,
          expected_val = '(this test uses randomly generated 5-dimensional Points)',
          name = 'euclidean_distance')


## manhattan_distance
def manhattan_distance_0_getargs() :  #TEST 71
    return [ Point((0,0)), Point((3,4)) ]
def manhattan_distance_0_testanswer(val, original_val = None) :
    return val == 7
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = manhattan_distance_0_getargs,
          testanswer = manhattan_distance_0_testanswer,
          expected_val = "7",
          name = 'manhattan_distance')

def manhattan_distance_1_getargs() :  #TEST 72
    return [ Point([-1,2,1], "A"), Point([-4,5,-2], "B") ]
def manhattan_distance_1_testanswer(val, original_val = None) :
    return val == 9
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = manhattan_distance_1_getargs,
          testanswer = manhattan_distance_1_testanswer,
          expected_val = "9",
          name = 'manhattan_distance')

manhattan_distance_2_random_inputs = [random_list(5), random_list(5)]
def manhattan_distance_2_getargs() :  #TEST 73
    return [Point(rlist) for rlist in manhattan_distance_2_random_inputs]
def manhattan_distance_2_testanswer(val, original_val = None) :
    return val==sum(map(lambda(a,b):abs(a-b),zip(*manhattan_distance_2_random_inputs)))
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = manhattan_distance_2_getargs,
          testanswer = manhattan_distance_2_testanswer,
          expected_val = '(this test uses randomly generated 5-dimensional Points)',
          name = 'manhattan_distance')


## hamming_distance
def hamming_distance_0_getargs() :  #TEST 74
    return [ Point((0,0)), Point((3,4)) ]
def hamming_distance_0_testanswer(val, original_val = None) :
    return val == 2
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = hamming_distance_0_getargs,
          testanswer = hamming_distance_0_testanswer,
          expected_val = "2",
          name = 'hamming_distance')

def hamming_distance_1_getargs() :  #TEST 75
    return [ Point([-4,2,1], "A"), Point([-4,5,1], "B") ]
def hamming_distance_1_testanswer(val, original_val = None) :
    return val == 1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = hamming_distance_1_getargs,
          testanswer = hamming_distance_1_testanswer,
          expected_val = "1",
          name = 'hamming_distance')

hamming_distance_2_random_inputs = [random_list(30,-1,1), random_list(30,-1,2)]
def hamming_distance_2_getargs() :  #TEST 76
    return [Point(rlist) for rlist in hamming_distance_2_random_inputs]
def hamming_distance_2_testanswer(val, original_val = None) :
    return val==sum(map(lambda(a,b):a!=b,zip(*hamming_distance_2_random_inputs)))
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = hamming_distance_2_getargs,
          testanswer = hamming_distance_2_testanswer,
          expected_val = '(this test uses randomly generated 30-dimensional Points)',
          name = 'hamming_distance')


## cosine_distance
def cosine_distance_0_getargs() :  #TEST 77
    return [ Point((0,2)), Point((3,4)) ]
def cosine_distance_0_testanswer(val, original_val = None) :
    return approx_equal(val, 0.2)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = cosine_distance_0_getargs,
          testanswer = cosine_distance_0_testanswer,
          expected_val = "0.2",
          name = 'cosine_distance')

def cosine_distance_1_getargs() :  #TEST 78
    return [ Point([-1,2,1], "A"), Point([-4,5,-2], "B") ]
def cosine_distance_1_testanswer(val, original_val = None) :
    return approx_equal(val, 0.2697)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = cosine_distance_1_getargs,
          testanswer = cosine_distance_1_testanswer,
          expected_val = "~ 0.2697",
          name = 'cosine_distance')

cosine_distance_2_random_inputs = [random_list(4), random_list(4)]
def cosine_distance_2_getargs() :  #TEST 79
    return [Point(rlist) for rlist in cosine_distance_2_random_inputs]
def cosine_distance_2_testanswer(val, original_val = None) :
    p=cosine_distance_2_random_inputs
    return approx_equal(val,1-1.*sum(map(lambda(a,b):a*b,zip(*p)))/reduce(lambda x,y:x*y,map(lambda v:sum(map(lambda i:i**2,v))**.5,p),1))
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = cosine_distance_2_getargs,
          testanswer = cosine_distance_2_testanswer,
          expected_val = '(this test uses randomly generated 4-dimensional Points)',
          name = 'cosine_distance')


#### CLASSIFYING POINTS

## get_k_closest_points
#euclidean_distance 1
def get_k_closest_points_00_getargs() :  #TEST 80
    return [deepcopy(knn_tree_test_point), deepcopy(knn_tree_data), 1, euclidean_distance]
get_k_closest_points_00_expected = [Point((20, 30), "Maple")]
def get_k_closest_points_00_testanswer(val, original_val = None) :
    return compare_list_contents(val, get_k_closest_points_00_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_k_closest_points_00_getargs,
          testanswer = get_k_closest_points_00_testanswer,
          expected_val = str(get_k_closest_points_00_expected),
          name = 'get_k_closest_points')

#euclidean_distance 3
def get_k_closest_points_0_getargs() :  #TEST 81
    return [deepcopy(knn_tree_test_point), deepcopy(knn_tree_data), 3, euclidean_distance]
get_k_closest_points_0_expected = [Point((20, 30), "Maple"), Point((25, 40), "Maple"), Point((20, 40), "Oak")]
def get_k_closest_points_0_testanswer(val, original_val = None) :
    return compare_list_contents(val, get_k_closest_points_0_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_k_closest_points_0_getargs,
          testanswer = get_k_closest_points_0_testanswer,
          expected_val = str(get_k_closest_points_0_expected),
          name = 'get_k_closest_points')

#euclidean_distance 5
def get_k_closest_points_1_getargs() :  #TEST 82
    return [deepcopy(knn_tree_test_point), deepcopy(knn_tree_data), 5, euclidean_distance]
get_k_closest_points_1_expected = [Point((20, 30), "Maple"), Point((25, 40), "Maple"), Point((20, 40), "Oak"), Point((30, 20), "Oak"), Point((40, 30), "Oak")]
def get_k_closest_points_1_testanswer(val, original_val = None) :
    return compare_list_contents(val, get_k_closest_points_1_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_k_closest_points_1_getargs,
          testanswer = get_k_closest_points_1_testanswer,
          expected_val = str(get_k_closest_points_1_expected),
          name = 'get_k_closest_points')

#manhattan_distance 3
def get_k_closest_points_2_getargs() :  #TEST 83
    return [deepcopy(knn_tree_test_point), deepcopy(knn_tree_data), 3, manhattan_distance]
get_k_closest_points_2_expected = [Point((20, 30), "Maple"), Point((25, 40), "Maple"), Point((20, 40), "Oak")]
def get_k_closest_points_2_testanswer(val, original_val = None) :
    return compare_list_contents(val, get_k_closest_points_2_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_k_closest_points_2_getargs,
          testanswer = get_k_closest_points_2_testanswer,
          expected_val = str(get_k_closest_points_2_expected),
          name = 'get_k_closest_points')

#manhattan_distance 5
def get_k_closest_points_3_getargs() :  #TEST 84
    return [deepcopy(knn_tree_test_point), deepcopy(knn_tree_data), 5, manhattan_distance]
get_k_closest_points_3_expected = [Point((20, 30), "Maple"), Point((25, 40), "Maple"), Point((20, 40), "Oak"), Point((30, 20), "Oak"), Point((40, 30), "Oak")]
def get_k_closest_points_3_testanswer(val, original_val = None) :
    return compare_list_contents(val, get_k_closest_points_3_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_k_closest_points_3_getargs,
          testanswer = get_k_closest_points_3_testanswer,
          expected_val = str(get_k_closest_points_3_expected),
          name = 'get_k_closest_points')

#hamming_distance 1
def get_k_closest_points_4_getargs() :  #TEST 85
    return [deepcopy(knn_tree_test_point), deepcopy(knn_tree_data), 1, hamming_distance]
get_k_closest_points_4_expected = [Point((25, 40), "Maple")]
def get_k_closest_points_4_testanswer(val, original_val = None) :
    return compare_list_contents(val, get_k_closest_points_4_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_k_closest_points_4_getargs,
          testanswer = get_k_closest_points_4_testanswer,
          expected_val = str(get_k_closest_points_4_expected),
          name = 'get_k_closest_points')

#This test checks that you prioritize shortest distance over tie-breaking
def get_k_closest_points_4a_getargs() :  #TEST 86
    data = [Point((1,3),"A"), Point((1,3),"A"), Point((2,3),"B")]
    return [Point((3,3)), data, 2, euclidean_distance]
get_k_closest_points_4a_expected = [Point((2,3),"B"), Point((1,3),"A")]
def get_k_closest_points_4a_testanswer(val, original_val = None) :
    return compare_list_contents(val, get_k_closest_points_4a_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_k_closest_points_4a_getargs,
          testanswer = get_k_closest_points_4a_testanswer,
          expected_val = str(get_k_closest_points_4a_expected),
          name = 'get_k_closest_points')

#hamming_distance 9
def get_k_closest_points_5_getargs() :  #TEST 87
    return [deepcopy(knn_tree_test_point), deepcopy(knn_tree_data), 9, hamming_distance]
get_k_closest_points_5_expected = [Point((10, 5), "Oak"), Point((20, 15), "Oak"), Point((20, 40), "Oak"), Point((30, 20), "Oak"), Point((40, 30), "Oak"), Point((5, 10), "Maple"), Point((10, 15), "Maple"), Point((20, 30), "Maple"), Point((25, 40), "Maple")]
def get_k_closest_points_5_testanswer(val, original_val = None) :
    return compare_list_contents(val, get_k_closest_points_5_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_k_closest_points_5_getargs,
          testanswer = get_k_closest_points_5_testanswer,
          expected_val = str(get_k_closest_points_5_expected),
          name = 'get_k_closest_points')

#cosine_distance 7
def get_k_closest_points_6_getargs() :  #TEST 88
    return [deepcopy(knn_tree_test_point), deepcopy(knn_tree_data), 7, cosine_distance]
get_k_closest_points_6_expected = [Point((10, 15), "Maple"), Point((20, 30), "Maple"), Point((25, 40), "Maple"), Point((5, 10), "Maple"), Point((20, 40), "Oak"), Point((20, 15), "Oak"), Point((40, 30), "Oak")]
def get_k_closest_points_6_testanswer(val, original_val = None) :
    return compare_list_contents(val, get_k_closest_points_6_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_k_closest_points_6_getargs,
          testanswer = get_k_closest_points_6_testanswer,
          expected_val = str(get_k_closest_points_6_expected),
          name = 'get_k_closest_points')

#cosine_distance 9
def get_k_closest_points_7_getargs() :  #TEST 89
    return [Point((25,32), "Maple"), deepcopy(knn_tree_data), 9, cosine_distance]
get_k_closest_points_7_expected = [Point((10, 5), "Oak"), Point((20, 15), "Oak"), Point((20, 40), "Oak"), Point((30, 20), "Oak"), Point((40, 30), "Oak"), Point((5, 10), "Maple"), Point((10, 15), "Maple"), Point((20, 30), "Maple"), Point((25, 40), "Maple")]
def get_k_closest_points_7_testanswer(val, original_val = None) :
    return compare_list_contents(val, get_k_closest_points_7_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_k_closest_points_7_getargs,
          testanswer = get_k_closest_points_7_testanswer,
          expected_val = str(get_k_closest_points_7_expected),
          name = 'get_k_closest_points')

#test with >2 classes, k = # points
def get_k_closest_points_8_getargs() :  #TEST 90
    return [Point([3], "D"), deepcopy(knn_toy_data), 5, euclidean_distance]
get_k_closest_points_8_expected = [Point([3], 'A'), Point([3], 'B'), Point([3], 'B'), Point([3], 'C'), Point([3], 'D')]
def get_k_closest_points_8_testanswer(val, original_val = None) :
    return compare_list_contents(val, get_k_closest_points_8_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_k_closest_points_8_getargs,
          testanswer = get_k_closest_points_8_testanswer,
          expected_val = str(get_k_closest_points_8_expected),
          name = 'get_k_closest_points')

#check lexicographic tie-breaking (all points equidistant from test point)
def get_k_closest_points_9_getargs() :  #TEST 91
    data = [Point([3,1,2],'a'), Point([2,3,1], 'b'), Point([2,1,3], 'c'), Point([1,3,2], 'd'), Point([3,2,1], 'e')]
    return [Point([2,2,2]), data, 2, euclidean_distance]
get_k_closest_points_9_expected = [Point([1,3,2], 'd'), Point([2,1,3], 'c')]
def get_k_closest_points_9_testanswer(val, original_val = None) :
    return compare_list_contents(val, get_k_closest_points_9_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_k_closest_points_9_getargs,
          testanswer = get_k_closest_points_9_testanswer,
          expected_val = str(get_k_closest_points_9_expected) + " (This test checks tie-breaking.)",
          name = 'get_k_closest_points')


## knn_classify_point
#euclidean_distance 3 Maple
def knn_classify_point_0_getargs() :  #TEST 92
    return [deepcopy(knn_tree_test_point), deepcopy(knn_tree_data), 3, euclidean_distance]
def knn_classify_point_0_testanswer(val, original_val = None) :
    return val == "Maple"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = knn_classify_point_0_getargs,
          testanswer = knn_classify_point_0_testanswer,
          expected_val = "Maple",
          name = 'knn_classify_point')

#euclidean_distance 5 Oak
def knn_classify_point_1_getargs() :  #TEST 93
    return [deepcopy(knn_tree_test_point), deepcopy(knn_tree_data), 5, euclidean_distance]
def knn_classify_point_1_testanswer(val, original_val = None) :
    return val == "Oak"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = knn_classify_point_1_getargs,
          testanswer = knn_classify_point_1_testanswer,
          expected_val = "Oak",
          name = 'knn_classify_point')

#manhattan_distance 3 Maple
def knn_classify_point_2_getargs() :  #TEST 94
    return [deepcopy(knn_tree_test_point), deepcopy(knn_tree_data), 3, manhattan_distance]
def knn_classify_point_2_testanswer(val, original_val = None) :
    return val == "Maple"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = knn_classify_point_2_getargs,
          testanswer = knn_classify_point_2_testanswer,
          expected_val = "Maple",
          name = 'knn_classify_point')

#manhattan_distance 5 Oak
def knn_classify_point_3_getargs() :  #TEST 95
    return [deepcopy(knn_tree_test_point), deepcopy(knn_tree_data), 5, manhattan_distance]
def knn_classify_point_3_testanswer(val, original_val = None) :
    return val == "Oak"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = knn_classify_point_3_getargs,
          testanswer = knn_classify_point_3_testanswer,
          expected_val = "Oak",
          name = 'knn_classify_point')

#hamming_distance 1 Maple
def knn_classify_point_4_getargs() :  #TEST 96
    return [deepcopy(knn_tree_test_point), deepcopy(knn_tree_data), 1, hamming_distance]
def knn_classify_point_4_testanswer(val, original_val = None) :
    return val == "Maple"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = knn_classify_point_4_getargs,
          testanswer = knn_classify_point_4_testanswer,
          expected_val = "Maple",
          name = 'knn_classify_point')

#hamming_distance 9 Oak
def knn_classify_point_5_getargs() :  #TEST 97
    return [deepcopy(knn_tree_test_point), deepcopy(knn_tree_data), 9, hamming_distance]
def knn_classify_point_5_testanswer(val, original_val = None) :
    return val == "Oak"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = knn_classify_point_5_getargs,
          testanswer = knn_classify_point_5_testanswer,
          expected_val = "Oak",
          name = 'knn_classify_point')

#cosine_distance 7 Maple
def knn_classify_point_6_getargs() :  #TEST 98
    return [deepcopy(knn_tree_test_point), deepcopy(knn_tree_data), 7, cosine_distance]
def knn_classify_point_6_testanswer(val, original_val = None) :
    return val == "Maple"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = knn_classify_point_6_getargs,
          testanswer = knn_classify_point_6_testanswer,
          expected_val = "Maple",
          name = 'knn_classify_point')

#cosine_distance 9 Oak
def knn_classify_point_7_getargs() :  #TEST 99
    return [Point((25,32), "Maple"), deepcopy(knn_tree_data), 9, cosine_distance]
def knn_classify_point_7_testanswer(val, original_val = None) :
    return val == "Oak"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = knn_classify_point_7_getargs,
          testanswer = knn_classify_point_7_testanswer,
          expected_val = "Oak",
          name = 'knn_classify_point')

#test with >2 classes
def knn_classify_point_8_getargs() :  #TEST 100
    return [Point([3], "D"), deepcopy(knn_toy_data), 5, euclidean_distance]
def knn_classify_point_8_testanswer(val, original_val = None) :
    return val == "B"
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = knn_classify_point_8_getargs,
          testanswer = knn_classify_point_8_testanswer,
          expected_val = "B",
          name = 'knn_classify_point')


## cross_validate
#euclidean_distance 7 0.333333333333
def cross_validate_0_getargs() :  #TEST 101
    return [deepcopy(knn_tree_data), 7, euclidean_distance]
def cross_validate_0_testanswer(val, original_val = None) :
    return approx_equal(val, 0.3333)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = cross_validate_0_getargs,
          testanswer = cross_validate_0_testanswer,
          expected_val = "~0.3333",
          name = 'cross_validate')

#manhattan_distance 3 0.111111111111
def cross_validate_1_getargs() :  #TEST 102
    return [deepcopy(knn_tree_data), 3, manhattan_distance]
def cross_validate_1_testanswer(val, original_val = None) :
    return approx_equal(val, 0.1111)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = cross_validate_1_getargs,
          testanswer = cross_validate_1_testanswer,
          expected_val = "~0.1111",
          name = 'cross_validate')

#hamming_distance 5 0.0
def cross_validate_2_getargs() :  #TEST 103
    return [deepcopy(knn_tree_data), 5, hamming_distance]
def cross_validate_2_testanswer(val, original_val = None) :
    return val == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = cross_validate_2_getargs,
          testanswer = cross_validate_2_testanswer,
          expected_val = "0",
          name = 'cross_validate')

#cosine_distance 1 0.777777777778
def cross_validate_3_getargs() :  #TEST 104
    return [deepcopy(knn_tree_data), 1, cosine_distance]
def cross_validate_3_testanswer(val, original_val = None) :
    return approx_equal(val, 0.77778)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = cross_validate_3_getargs,
          testanswer = cross_validate_3_testanswer,
          expected_val = "~0.77778",
          name = 'cross_validate')

#cosine_distance 4 0.888888888889
def cross_validate_4_getargs() :  #TEST 105
    return [deepcopy(knn_tree_data), 4, cosine_distance]
def cross_validate_4_testanswer(val, original_val = None) :
    return approx_equal(val, 0.88889)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = cross_validate_4_getargs,
          testanswer = cross_validate_4_testanswer,
          expected_val = "~0.88889",
          name = 'cross_validate')


## find_best_k_and_metric
#knn_tree_data -> k in [2,3,4,5,6], metric=cosine_distance (k=2 and k=6 depend on tie-breaking)
def find_best_k_and_metric_5_getargs() :  #TEST 106
    return [deepcopy(knn_tree_data)]
def find_best_k_and_metric_5_testanswer(val, original_val = None) :
    return len(val)==2 and (val[0] in [2,3,4,5,6]) and val[1]==cosine_distance
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = find_best_k_and_metric_5_getargs,
          testanswer = find_best_k_and_metric_5_testanswer,
          expected_val = "tuple (k, cosine_distance), where 2 <= k <= 6",
          name = 'find_best_k_and_metric')


#kNN_ANSWER_1
kNN_ANSWER_1_getargs = 'kNN_ANSWER_1'  #TEST 107
def kNN_ANSWER_1_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == "Overfitting" or val == "overfitting"
make_test(type = 'VALUE',
          getargs = kNN_ANSWER_1_getargs,
          testanswer = kNN_ANSWER_1_testanswer,
          expected_val = "correct answer as a string ('Overfitting' or 'Underfitting')",
          name = kNN_ANSWER_1_getargs)

#kNN_ANSWER_2
kNN_ANSWER_2_getargs = 'kNN_ANSWER_2'  #TEST 108
def kNN_ANSWER_2_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == "Underfitting" or val == "underfitting"
make_test(type = 'VALUE',
          getargs = kNN_ANSWER_2_getargs,
          testanswer = kNN_ANSWER_2_testanswer,
          expected_val = "correct answer as a string ('Overfitting' or 'Underfitting')",
          name = kNN_ANSWER_2_getargs)

#kNN_ANSWER_3
kNN_ANSWER_3_getargs = 'kNN_ANSWER_3'  #TEST 109
def kNN_ANSWER_3_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 4
make_test(type = 'VALUE',
          getargs = kNN_ANSWER_3_getargs,
          testanswer = kNN_ANSWER_3_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = kNN_ANSWER_3_getargs)

#kNN_ANSWER_4: Euclidean or cosine distance would probably work, but ratio seems
# more important in this case. The Manhattan distance answer is nonsense. Using
# Hamming distance with boolean values might work, but it would be easily fooled
# by coffee containing a small amount of sugar, or a type of soda that contains
# a small amount of caffeine.
kNN_ANSWER_4_getargs = 'kNN_ANSWER_4'  #TEST 110
def kNN_ANSWER_4_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 4
make_test(type = 'VALUE',
          getargs = kNN_ANSWER_4_getargs,
          testanswer = kNN_ANSWER_4_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = kNN_ANSWER_4_getargs)

#kNN_ANSWER_5: Cosine distance is useless for a point at the origin (water), so
# Euclidean distance is now the better answer.
kNN_ANSWER_5_getargs = 'kNN_ANSWER_5'  #TEST 111
def kNN_ANSWER_5_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 1
make_test(type = 'VALUE',
          getargs = kNN_ANSWER_5_getargs,
          testanswer = kNN_ANSWER_5_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = kNN_ANSWER_5_getargs)

#kNN_ANSWER_6: Hamming distance, because the features are non-numeric.  All the
# other answers are nonsense.
kNN_ANSWER_6_getargs = 'kNN_ANSWER_6'  #TEST 112
def kNN_ANSWER_6_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 3
make_test(type = 'VALUE',
          getargs = kNN_ANSWER_6_getargs,
          testanswer = kNN_ANSWER_6_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = kNN_ANSWER_6_getargs)

#kNN_ANSWER_7: One of the main advantages of ID trees is that they CAN ignore
# irrelevant features, because only the features with the least disorder are
# used in the tree.  In this case, the tree would consist of a single test,
# logo, which would fully determine the classification.
#
# 1: kNN does not require data to be graphed; Hamming distance would work
# 2: kNN has no problem with identical training points. They are difficult to
#      display visually, but the algorithm doesn't care.
# 4: This answer is completely garbage.
kNN_ANSWER_7_getargs = 'kNN_ANSWER_7'  #TEST 113
def kNN_ANSWER_7_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 3
make_test(type = 'VALUE',
          getargs = kNN_ANSWER_7_getargs,
          testanswer = kNN_ANSWER_7_testanswer,
          expected_val = "correct answer as an int (1, 2, 3, or 4)",
          name = kNN_ANSWER_7_getargs)
