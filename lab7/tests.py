# MIT 6.034 Lab 7: Support Vector Machines

from tester import make_test, get_tests
from svm_data import *
from random import random, randint

lab_number = 7 #for tester.py

def randnum(max_val=100):
    "Generates a random float 0 < n < max_val"
    return random() * randint(1, int(max_val))


## dot_product
def dot_product_0_getargs() :  #TEST 1
    return [(3, -7), [2.5, 10]]
def dot_product_0_testanswer(val, original_val = None) :
    return approx_equal(val, -62.5)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = dot_product_0_getargs,
          testanswer = dot_product_0_testanswer,
          expected_val = "-62.5",
          name = 'dot_product')

def dot_product_1_getargs() :  #TEST 2
    return [[4], (5,)]
def dot_product_1_testanswer(val, original_val = None) :
    return val == 20
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = dot_product_1_getargs,
          testanswer = dot_product_1_testanswer,
          expected_val = "20",
          name = 'dot_product')

def dot_product_2_getargs() :  #TEST 3
    return [(1,2,3,4,2), (1, 10, 1000, 100, 10000)]
def dot_product_2_testanswer(val, original_val = None) :
    return val == 23421
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = dot_product_2_getargs,
          testanswer = dot_product_2_testanswer,
          expected_val = "23421",
          name = 'dot_product')


## norm
def norm_0_getargs() :  #TEST 4
    return [(-3, 4)]
def norm_0_testanswer(val, original_val = None) :
    return val == 5
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = norm_0_getargs,
          testanswer = norm_0_testanswer,
          expected_val = "5",
          name = 'norm')

def norm_1_getargs() :  #TEST 5
    return [(17.2,)]
def norm_1_testanswer(val, original_val = None) :
    return approx_equal(val, 17.2)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = norm_1_getargs,
          testanswer = norm_1_testanswer,
          expected_val = "17.2",
          name = 'norm')

def norm_2_getargs() :  #TEST 6
    return [[6, 2, 11, -2, 2]]
def norm_2_testanswer(val, original_val = None) :
    return val == 13
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = norm_2_getargs,
          testanswer = norm_2_testanswer,
          expected_val = "13",
          name = 'norm')


## positiveness
def positiveness_0_getargs() :  #TEST 7
    return [svm_basic.copy(), Point('p', (0, 0))]
def positiveness_0_testanswer(val, original_val = None) :
    return val == 3
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = positiveness_0_getargs,
          testanswer = positiveness_0_testanswer,
          expected_val = "3",
          name = 'positiveness')

def positiveness_1_getargs() :  #TEST 8
    return [SVM([2, 5, -1, 1, 0, -0.1], 0.01),
            Point('v', [3, -2, -7, -10, 99, 8])]
def positiveness_1_testanswer(val, original_val = None) :
    return approx_equal(val, -7.79)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = positiveness_1_getargs,
          testanswer = positiveness_1_testanswer,
          expected_val = "-7.79",
          name = 'positiveness')

def positiveness_2_getargs() :  #TEST 9
    return [svm_untrained.copy(), ptD]
def positiveness_2_testanswer(val, original_val = None) :
    return val == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = positiveness_2_getargs,
          testanswer = positiveness_2_testanswer,
          expected_val = "0",
          name = 'positiveness')


## classify
#point doesn't have classification
def classify_0_getargs() :  #TEST 10
    return [svm_basic.copy(), Point('test_point', (0, 0))]
def classify_0_testanswer(val, original_val = None) :
    return val == 1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = classify_0_getargs,
          testanswer = classify_0_testanswer,
          expected_val = "+1",
          name = 'classify')

#point has classification; misclassified
def classify_1_getargs() :  #TEST 11
    return [svm_untrained.copy(), ptF]
def classify_1_testanswer(val, original_val = None) :
    return val == -1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = classify_1_getargs,
          testanswer = classify_1_testanswer,
          expected_val = "-1",
          name = 'classify')

#point has classification; classified correctly
def classify_2_getargs() :  #TEST 12
    return [svm_basic.copy(), ptD]
def classify_2_testanswer(val, original_val = None) :
    return val == -1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = classify_2_getargs,
          testanswer = classify_2_testanswer,
          expected_val = "-1",
          name = 'classify')

# point on boundary
def classify_3_getargs() :  #TEST 13
    return [svm_basic.copy(), Point('x', [1.5, randnum()])]
def classify_3_testanswer(val, original_val = None) :
    return val == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = classify_3_getargs,
          testanswer = classify_3_testanswer,
          expected_val = "0",
          name = 'classify')

#point within margin, not on boundary
def classify_4_getargs() :  #TEST 14
    return [svm_basic.copy(), Point('x', [1.6, randnum()])]
def classify_4_testanswer(val, original_val = None) :
    return val == -1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = classify_4_getargs,
          testanswer = classify_4_testanswer,
          expected_val = "-1",
          name = 'classify')


## margin_width
# w=[-3,4], so norm=5 -> 0.4
def margin_width_0_getargs() :  #TEST 15
    return [SVM((-3, 4), -13.78)]
def margin_width_0_testanswer(val, original_val = None) :
    return approx_equal(val, 0.4)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = margin_width_0_getargs,
          testanswer = margin_width_0_testanswer,
          expected_val = "0.4",
          name = 'margin_width')

# w=[1,0], point on boundary, point misclassified -> 2 (ignore points)
def margin_width_1_getargs() :  #TEST 16
    return [svm_untrained.copy()]
def margin_width_1_testanswer(val, original_val = None) :
    return val == 2
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = margin_width_1_getargs,
          testanswer = margin_width_1_testanswer,
          expected_val = "2",
          name = 'margin_width')

# 1D
def margin_width_2_getargs() :  #TEST 17
    return [SVM([0.25], 0)]
def margin_width_2_testanswer(val, original_val = None) :
    return val == 8
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = margin_width_2_getargs,
          testanswer = margin_width_2_testanswer,
          expected_val = "8",
          name = 'margin_width')

# higher number of dimensions
def margin_width_3_getargs() :  #TEST 18
    return [SVM([0, -5, 0, 12], 1)]
def margin_width_3_testanswer(val, original_val = None) :
    return approx_equal(val, 0.15384615, 0.000001)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = margin_width_3_getargs,
          testanswer = margin_width_3_testanswer,
          expected_val = "~0.15384615",
          name = 'margin_width')


## check_gutter_constraint
# pass -> empty set
def check_gutter_constraint_0_getargs() :  #TEST 19
    return [svm_basic.copy()]
def check_gutter_constraint_0_testanswer(val, original_val = None) :
    return val == set()
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_gutter_constraint_0_getargs,
          testanswer = check_gutter_constraint_0_testanswer,
          expected_val = set(),
          name = 'check_gutter_constraint')

# fail gutter constraint equation
def check_gutter_constraint_1_getargs() :  #TEST 20
    return [svm_basic.copy().set_boundary([2, 0], 3)]
check_gutter_constraint_1_expected = set([ptA, ptB, ptD])
def check_gutter_constraint_1_testanswer(val, original_val = None) :
    return equality_by_string(val, check_gutter_constraint_1_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_gutter_constraint_1_getargs,
          testanswer = check_gutter_constraint_1_testanswer,
          expected_val = check_gutter_constraint_1_expected,
          name = 'check_gutter_constraint')

# fail with point in gutter
def check_gutter_constraint_2_getargs() :  #TEST 21
    svm = svm_basic.copy()
    svm.training_points.append(ptL)
    return [svm]
check_gutter_constraint_2_expected = set([ptL])
def check_gutter_constraint_2_testanswer(val, original_val = None) :
    return equality_by_string(val, check_gutter_constraint_2_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_gutter_constraint_2_getargs,
          testanswer = check_gutter_constraint_2_testanswer,
          expected_val = check_gutter_constraint_2_expected,
          name = 'check_gutter_constraint')

# fail both ways
def check_gutter_constraint_3_getargs() :  #TEST 22
    svm = svm_basic.copy().set_boundary([2, 0], -3)
    svm.training_points.append(ptLx)
    return [svm]
check_gutter_constraint_3_expected = set([ptA, ptB, ptD, ptLx])
def check_gutter_constraint_3_testanswer(val, original_val = None) :
    return equality_by_string(val, check_gutter_constraint_3_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_gutter_constraint_3_getargs,
          testanswer = check_gutter_constraint_3_testanswer,
          expected_val = check_gutter_constraint_3_expected,
          name = 'check_gutter_constraint')


## check_alpha_signs
# set should include: sv w alpha=0, sv w alpha<0, pt w alpha < 0, pt w alpha > 0
# set should not include: sv w alpha > 0, pt w alpha = 0
def check_alpha_signs_0_getargs() :  #TEST 23
    return [svm_alphas.copy()]
check_alpha_signs_0_expected = set([ptF, ptG, ptJ, ptH, ptD])
def check_alpha_signs_0_testanswer(val, original_val = None) :
    return equality_by_string(val, check_alpha_signs_0_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_alpha_signs_0_getargs,
          testanswer = check_alpha_signs_0_testanswer,
          expected_val = str(check_alpha_signs_0_expected),
          name = 'check_alpha_signs')

# return empty set
def check_alpha_signs_1_getargs() :  #TEST 24
    return [svm_basic.copy()]
def check_alpha_signs_1_testanswer(val, original_val = None) :
    return val == set()
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_alpha_signs_1_getargs,
          testanswer = check_alpha_signs_1_testanswer,
          expected_val = set(),
          name = 'check_alpha_signs')


## check_alpha_equations
# both equations hold -> True
def check_alpha_equations_0_getargs() :  #TEST 25
    return [svm_basic.copy()]
def check_alpha_equations_0_testanswer(val, original_val = None) :
    return val == True
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_alpha_equations_0_getargs,
          testanswer = check_alpha_equations_0_testanswer,
          expected_val = "True",
          name = 'check_alpha_equations')

# Eq 4 fails
def check_alpha_equations_1_getargs() :  #TEST 26
    return [svm_fail_eq4.copy()]
def check_alpha_equations_1_testanswer(val, original_val = None) :
    return val == False
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_alpha_equations_1_getargs,
          testanswer = check_alpha_equations_1_testanswer,
          expected_val = "False",
          name = 'check_alpha_equations')

# Eq 5 fails
def check_alpha_equations_2_getargs() :  #TEST 27
    return [svm_fail_eq5.copy()]
def check_alpha_equations_2_testanswer(val, original_val = None) :
    return val == False
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_alpha_equations_2_getargs,
          testanswer = check_alpha_equations_2_testanswer,
          expected_val = "False",
          name = 'check_alpha_equations')

# Eq 4 fails, but NOT gutter constraint
def check_alpha_equations_3_getargs() :  #TEST 28
    return [svm_fail_eq4_but_not_eq3.copy()]
def check_alpha_equations_3_testanswer(val, original_val = None) :
    return val == False
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_alpha_equations_3_getargs,
          testanswer = check_alpha_equations_3_testanswer,
          expected_val = "False",
          name = 'check_alpha_equations')

# Eq 5 fails, but NOT any other equations
def check_alpha_equations_4_getargs() :  #TEST 29
    return [svm_fail_eq4_only.copy()]
def check_alpha_equations_4_testanswer(val, original_val = None) :
    return val == False
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_alpha_equations_4_getargs,
          testanswer = check_alpha_equations_4_testanswer,
          expected_val = "False",
          name = 'check_alpha_equations')

# Fail gutter constraint, but pass equations 4-5
def check_alpha_equations_5_getargs() :  #TEST 30
    return [svm_fail_gutter_only.copy()]
def check_alpha_equations_5_testanswer(val, original_val = None) :
    return val == True
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_alpha_equations_5_getargs,
          testanswer = check_alpha_equations_5_testanswer,
          expected_val = "True",
          name = 'check_alpha_equations')

# Fail check_alphas, but pass equations 4-5
def check_alpha_equations_6_getargs() :  #TEST 31
    return [svm_fail_alphas_only.copy()]
def check_alpha_equations_6_testanswer(val, original_val = None) :
    return val == True
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_alpha_equations_6_getargs,
          testanswer = check_alpha_equations_6_testanswer,
          expected_val = "True",
          name = 'check_alpha_equations')


## misclassified_training_points
def misclassified_training_points_0_getargs() :  #TEST 32
    return [svm_basic.copy()]
def misclassified_training_points_0_testanswer(val, original_val = None) :
    return val == set()
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = misclassified_training_points_0_getargs,
          testanswer = misclassified_training_points_0_testanswer,
          expected_val = set(),
          name = 'misclassified_training_points')

def misclassified_training_points_1_getargs() :  #TEST 33
    return [svm_untrained.copy()]
misclassified_training_points_1_expected = set([ptD, ptF])
def misclassified_training_points_1_testanswer(val, original_val = None) :
    return equality_by_string(val, misclassified_training_points_1_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = misclassified_training_points_1_getargs,
          testanswer = misclassified_training_points_1_testanswer,
          expected_val = str(misclassified_training_points_1_expected),
          name = 'misclassified_training_points')


## update_svm_from_alphas
update_svm_from_alphas_0_input = svm_update_recit_0.copy().set_boundary([], 0)
update_svm_from_alphas_0_input.support_vectors = []
def update_svm_from_alphas_0_getargs() :  #TEST 34
    return [update_svm_from_alphas_0_input]
def update_svm_from_alphas_0_testanswer(val, original_val = None) :
    return val == svm_update_recit_0 and val is update_svm_from_alphas_0_input
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = update_svm_from_alphas_0_getargs,
          testanswer = update_svm_from_alphas_0_testanswer,
          expected_val = 'Input ' + str(svm_update_recit_0),
          name = 'update_svm_from_alphas')

update_svm_from_alphas_1_input = svm_update_recit_1.copy().set_boundary([52, 19], 6)
update_svm_from_alphas_1_input.support_vectors = [Point('E', [3, 2], -1, 0)]
def update_svm_from_alphas_1_getargs() :  #TEST 35
    return [update_svm_from_alphas_1_input]
def update_svm_from_alphas_1_testanswer(val, original_val = None) :
    return val == svm_update_recit_1 and val is update_svm_from_alphas_1_input
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = update_svm_from_alphas_1_getargs,
          testanswer = update_svm_from_alphas_1_testanswer,
          expected_val = 'Input ' + str(svm_update_recit_1),
          name = 'update_svm_from_alphas')

update_svm_from_alphas_2_input = svm_update_recit_2.copy().set_boundary([1.0, 0.0], -1.5)
update_svm_from_alphas_2_input.support_vectors = [Point('B', [1, 1], 1, 1.0)]
def update_svm_from_alphas_2_getargs() :  #TEST 36
    return [update_svm_from_alphas_2_input]
def update_svm_from_alphas_2_testanswer(val, original_val = None) :
    return val == svm_update_recit_2 and val is update_svm_from_alphas_2_input
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = update_svm_from_alphas_2_getargs,
          testanswer = update_svm_from_alphas_2_testanswer,
          expected_val = 'Input ' + str(svm_update_recit_2),
          name = 'update_svm_from_alphas')

update_svm_from_alphas_3_input = svm_update_recit_1.copy()
def update_svm_from_alphas_3_getargs() :  #TEST 37
    return [update_svm_from_alphas_3_input]
def update_svm_from_alphas_3_testanswer(val, original_val = None) :
    return val == svm_update_recit_1 and val is update_svm_from_alphas_3_input
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = update_svm_from_alphas_3_getargs,
          testanswer = update_svm_from_alphas_3_testanswer,
          expected_val = 'Input ' + str(svm_update_recit_1),
          name = 'update_svm_from_alphas')

update_svm_from_alphas_4_input = svm_update_harvard_mit_n.copy().set_boundary([], 0)
update_svm_from_alphas_4_input.support_vectors = []
def update_svm_from_alphas_4_getargs() :  #TEST 38
    return [update_svm_from_alphas_4_input]
def update_svm_from_alphas_4_testanswer(val, original_val = None) :
    return val == svm_update_harvard_mit_n and val is update_svm_from_alphas_4_input
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = update_svm_from_alphas_4_getargs,
          testanswer = update_svm_from_alphas_4_testanswer,
          expected_val = 'Input ' + str(svm_update_harvard_mit_n),
          name = 'update_svm_from_alphas')


#ANSWER_1
ANSWER_1_getargs = 'ANSWER_1'  #TEST 39
def ANSWER_1_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 11
make_test(type = 'VALUE',
          getargs = ANSWER_1_getargs,
          testanswer = ANSWER_1_testanswer,
          expected_val = "correct number of iterations (int)",
          name = ANSWER_1_getargs)

#ANSWER_2
ANSWER_2_getargs = 'ANSWER_2'  #TEST 40
def ANSWER_2_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 6
make_test(type = 'VALUE',
          getargs = ANSWER_2_getargs,
          testanswer = ANSWER_2_testanswer,
          expected_val = "maximum number of SVs at once (int)",
          name = ANSWER_2_getargs)

#ANSWER_3
ANSWER_3_getargs = 'ANSWER_3'  #TEST 41
def ANSWER_3_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 3
make_test(type = 'VALUE',
          getargs = ANSWER_3_getargs,
          testanswer = ANSWER_3_testanswer,
          expected_val = "final number of SVs (int)",
          name = ANSWER_3_getargs)

#ANSWER_4
ANSWER_4_getargs = 'ANSWER_4'  #TEST 42
def ANSWER_4_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 2
make_test(type = 'VALUE',
          getargs = ANSWER_4_getargs,
          testanswer = ANSWER_4_testanswer,
          expected_val = "correct number of iterations (int)",
          name = ANSWER_4_getargs)

#ANSWER_5
ANSWER_5_getargs = 'ANSWER_5'  #TEST 43
def ANSWER_5_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return set(val) == set('AD')
make_test(type = 'VALUE',
          getargs = ANSWER_5_getargs,
          testanswer = ANSWER_5_testanswer,
          expected_val = "list of point names",
          name = ANSWER_5_getargs)

#ANSWER_6
ANSWER_6_getargs = 'ANSWER_6'  #TEST 44
def ANSWER_6_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return set(val) == set('ABD')
make_test(type = 'VALUE',
          getargs = ANSWER_6_getargs,
          testanswer = ANSWER_6_testanswer,
          expected_val = "list of point names",
          name = ANSWER_6_getargs)

#ANSWER_7
ANSWER_7_getargs = 'ANSWER_7'  #TEST 45
def ANSWER_7_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return set(val) == set('ABD')
make_test(type = 'VALUE',
          getargs = ANSWER_7_getargs,
          testanswer = ANSWER_7_testanswer,
          expected_val = "list of point names",
          name = ANSWER_7_getargs)

#ANSWER_8
ANSWER_8_getargs = 'ANSWER_8'  #TEST 46
def ANSWER_8_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == []
make_test(type = 'VALUE',
          getargs = ANSWER_8_getargs,
          testanswer = ANSWER_8_testanswer,
          expected_val = "list of point names",
          name = ANSWER_8_getargs)

#ANSWER_9
ANSWER_9_getargs = 'ANSWER_9'  #TEST 47
def ANSWER_9_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return set(val) == set('ABD')
make_test(type = 'VALUE',
          getargs = ANSWER_9_getargs,
          testanswer = ANSWER_9_testanswer,
          expected_val = "list of point names",
          name = ANSWER_9_getargs)

#ANSWER_10
ANSWER_10_getargs = 'ANSWER_10'  #TEST 48
def ANSWER_10_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return set(val) == set('ABD')
make_test(type = 'VALUE',
          getargs = ANSWER_10_getargs,
          testanswer = ANSWER_10_testanswer,
          expected_val = "list of point names",
          name = ANSWER_10_getargs)

#ANSWER_11
ANSWER_11_getargs = 'ANSWER_11'  #TEST 49
def ANSWER_11_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == False
make_test(type = 'VALUE',
          getargs = ANSWER_11_getargs,
          testanswer = ANSWER_11_testanswer,
          expected_val = "True or False",
          name = ANSWER_11_getargs)

#ANSWER_12
ANSWER_12_getargs = 'ANSWER_12'  #TEST 50
def ANSWER_12_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == True
make_test(type = 'VALUE',
          getargs = ANSWER_12_getargs,
          testanswer = ANSWER_12_testanswer,
          expected_val = "True or False",
          name = ANSWER_12_getargs)

#ANSWER_13
ANSWER_13_getargs = 'ANSWER_13'  #TEST 51
def ANSWER_13_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == False
make_test(type = 'VALUE',
          getargs = ANSWER_13_getargs,
          testanswer = ANSWER_13_testanswer,
          expected_val = "True or False",
          name = ANSWER_13_getargs)

#ANSWER_14
ANSWER_14_getargs = 'ANSWER_14'  #TEST 52
def ANSWER_14_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == False
make_test(type = 'VALUE',
          getargs = ANSWER_14_getargs,
          testanswer = ANSWER_14_testanswer,
          expected_val = "True or False",
          name = ANSWER_14_getargs)

#ANSWER_15
ANSWER_15_getargs = 'ANSWER_15'  #TEST 53
def ANSWER_15_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == False
make_test(type = 'VALUE',
          getargs = ANSWER_15_getargs,
          testanswer = ANSWER_15_testanswer,
          expected_val = "True or False",
          name = ANSWER_15_getargs)

#ANSWER_16
ANSWER_16_getargs = 'ANSWER_16'  #TEST 54
def ANSWER_16_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == True
make_test(type = 'VALUE',
          getargs = ANSWER_16_getargs,
          testanswer = ANSWER_16_testanswer,
          expected_val = "True or False",
          name = ANSWER_16_getargs)

#ANSWER_17
ANSWER_17_getargs = 'ANSWER_17'  #TEST 55
def ANSWER_17_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return set(val) == set([1,3,6,8])
make_test(type = 'VALUE',
          getargs = ANSWER_17_getargs,
          testanswer = ANSWER_17_testanswer,
          expected_val = "list of ints between 1-8",
          name = ANSWER_17_getargs)

#ANSWER_18
ANSWER_18_getargs = 'ANSWER_18'  #TEST 56
def ANSWER_18_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return set(val) == set([1,2,4,5,6,7,8])
make_test(type = 'VALUE',
          getargs = ANSWER_18_getargs,
          testanswer = ANSWER_18_testanswer,
          expected_val = "list of ints between 1-8",
          name = ANSWER_18_getargs)

#ANSWER_19
ANSWER_19_getargs = 'ANSWER_19'  #TEST 57
def ANSWER_19_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return set(val) == set([1,2,4,5,6,7,8])
make_test(type = 'VALUE',
          getargs = ANSWER_19_getargs,
          testanswer = ANSWER_19_testanswer,
          expected_val = "list of ints between 1-8",
          name = ANSWER_19_getargs)

#ANSWER_20
ANSWER_20_getargs = 'ANSWER_20'  #TEST 58
def ANSWER_20_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 6
make_test(type = 'VALUE',
          getargs = ANSWER_20_getargs,
          testanswer = ANSWER_20_testanswer,
          expected_val = "int between 1-6",
          name = ANSWER_20_getargs)
