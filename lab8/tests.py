# MIT 6.034 Lab 8: Bayesian Inference

from tester import make_test, get_tests
from nets import *

lab_number = 8 #for tester.py

def get_ancestors_0_getargs() :  #TEST 1
    return [net_basic.copy(), 'A']
get_ancestors_0_expected = set()
def get_ancestors_0_testanswer(val, original_val = None) :
    return val == get_ancestors_0_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_ancestors_0_getargs,
          testanswer = get_ancestors_0_testanswer,
          expected_val = str(get_ancestors_0_expected),
          name = 'get_ancestors')

def get_ancestors_1_getargs() :  #TEST 2
    return [net_basic.copy(), 'C']
get_ancestors_1_expected = set('AB')
def get_ancestors_1_testanswer(val, original_val = None) :
    return val == get_ancestors_1_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_ancestors_1_getargs,
          testanswer = get_ancestors_1_testanswer,
          expected_val = str(get_ancestors_1_expected),
          name = 'get_ancestors')

def get_ancestors_2_getargs() :  #TEST 3
    return [net_dsep.copy(), 'F']
get_ancestors_2_expected = set('ABCD')
def get_ancestors_2_testanswer(val, original_val = None) :
    return val == get_ancestors_2_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_ancestors_2_getargs,
          testanswer = get_ancestors_2_testanswer,
          expected_val = str(get_ancestors_2_expected),
          name = 'get_ancestors')

def get_ancestors_3_getargs() :  #TEST 4
    return [net_dsep.copy(), 'E']
get_ancestors_3_expected = set('ABC')
def get_ancestors_3_testanswer(val, original_val = None) :
    return val == get_ancestors_3_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_ancestors_3_getargs,
          testanswer = get_ancestors_3_testanswer,
          expected_val = str(get_ancestors_3_expected),
          name = 'get_ancestors')


def get_descendants_0_getargs() :  #TEST 5
    return [net_basic.copy(), 'A']
get_descendants_0_expected = set('C')
def get_descendants_0_testanswer(val, original_val = None) :
    return val == get_descendants_0_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_descendants_0_getargs,
          testanswer = get_descendants_0_testanswer,
          expected_val = str(get_descendants_0_expected),
          name = 'get_descendants')

def get_descendants_1_getargs() :  #TEST 6
    return [net_dsep.copy(), 'D']
get_descendants_1_expected = set('FG')
def get_descendants_1_testanswer(val, original_val = None) :
    return val == get_descendants_1_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_descendants_1_getargs,
          testanswer = get_descendants_1_testanswer,
          expected_val = str(get_descendants_1_expected),
          name = 'get_descendants')

def get_descendants_2_getargs() :  #TEST 7
    return [net_dsep.copy(), 'B']
get_descendants_2_expected = set('CDEFG')
def get_descendants_2_testanswer(val, original_val = None) :
    return val == get_descendants_2_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_descendants_2_getargs,
          testanswer = get_descendants_2_testanswer,
          expected_val = str(get_descendants_2_expected),
          name = 'get_descendants')

def get_descendants_3_getargs() :  #TEST 8
    return [net_dsep.copy(), 'E']
get_descendants_3_expected = set()
def get_descendants_3_testanswer(val, original_val = None) :
    return val == get_descendants_3_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_descendants_3_getargs,
          testanswer = get_descendants_3_testanswer,
          expected_val = str(get_descendants_3_expected),
          name = 'get_descendants')

def get_descendants_4_getargs() :  #TEST 9
    return [net_disjoint.copy(), 'A']
get_descendants_4_expected = set()
def get_descendants_4_testanswer(val, original_val = None) :
    return val == get_descendants_4_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_descendants_4_getargs,
          testanswer = get_descendants_4_testanswer,
          expected_val = str(get_descendants_4_expected),
          name = 'get_descendants')


def get_nondescendants_0_getargs() :  #TEST 10
    return [net_basic.copy(), 'A']
get_nondescendants_0_expected = set('B')
def get_nondescendants_0_testanswer(val, original_val = None) :
    return val == get_nondescendants_0_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_nondescendants_0_getargs,
          testanswer = get_nondescendants_0_testanswer,
          expected_val = str(get_nondescendants_0_expected),
          name = 'get_nondescendants')

def get_nondescendants_1_getargs() :  #TEST 11
    return [net_basic.copy(), 'C']
get_nondescendants_1_expected = set('AB')
def get_nondescendants_1_testanswer(val, original_val = None) :
    return val == get_nondescendants_1_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_nondescendants_1_getargs,
          testanswer = get_nondescendants_1_testanswer,
          expected_val = str(get_nondescendants_1_expected),
          name = 'get_nondescendants')

def get_nondescendants_2_getargs() :  #TEST 12
    return [net_dsep.copy(), 'F']
get_nondescendants_2_expected = set('ABCDE')
def get_nondescendants_2_testanswer(val, original_val = None) :
    return val == get_nondescendants_2_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_nondescendants_2_getargs,
          testanswer = get_nondescendants_2_testanswer,
          expected_val = str(get_nondescendants_2_expected),
          name = 'get_nondescendants')

def get_nondescendants_3_getargs() :  #TEST 13
    return [net_dsep.copy(), 'E']
get_nondescendants_3_expected = set('ABCDFG')
def get_nondescendants_3_testanswer(val, original_val = None) :
    return val == get_nondescendants_3_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_nondescendants_3_getargs,
          testanswer = get_nondescendants_3_testanswer,
          expected_val = str(get_nondescendants_3_expected),
          name = 'get_nondescendants')

def get_nondescendants_4_getargs() :  #TEST 14
    return [net_dsep.copy(), 'D']
get_nondescendants_4_expected = set('ABCE')
def get_nondescendants_4_testanswer(val, original_val = None) :
    return val == get_nondescendants_4_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_nondescendants_4_getargs,
          testanswer = get_nondescendants_4_testanswer,
          expected_val = str(get_nondescendants_4_expected),
          name = 'get_nondescendants')

def get_nondescendants_5_getargs() :  #TEST 15
    return [net_disjoint.copy(), 'A']
get_nondescendants_5_expected = set('B')
def get_nondescendants_5_testanswer(val, original_val = None) :
    return val == get_nondescendants_5_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_nondescendants_5_getargs,
          testanswer = get_nondescendants_5_testanswer,
          expected_val = str(get_nondescendants_5_expected),
          name = 'get_nondescendants')



simplify_givens_0_input_givens = dict(D=True, E=False, C=True, A=False)
def simplify_givens_0_getargs() :  #TEST 16
    return [net_dsep.copy(), 'F', simplify_givens_0_input_givens]
simplify_givens_0_expected = dict(D=True)
def simplify_givens_0_testanswer(val, original_val = None) :
    return (val == simplify_givens_0_expected
            and simplify_givens_0_input_givens == dict(D=True, E=False, C=True, A=False))
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = simplify_givens_0_getargs,
          testanswer = simplify_givens_0_testanswer,
          expected_val = (str(simplify_givens_0_expected)
                          + "  (with input givens unchanged)"),
          name = 'simplify_givens')

def simplify_givens_0g_getargs() :  #TEST 17
    return [net_dsep.copy(), 'F', dict(D=True, E=False, G=True, C=True, A=False)]
simplify_givens_0g_expected = dict(D=True, E=False, G=True, C=True, A=False)
def simplify_givens_0g_testanswer(val, original_val = None) :
    return val == simplify_givens_0g_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = simplify_givens_0g_getargs,
          testanswer = simplify_givens_0g_testanswer,
          expected_val = str(simplify_givens_0g_expected),
          name = 'simplify_givens')

def simplify_givens_1_getargs() :  #TEST 18
    return [net_dsep.copy(), 'F', dict(E=False, G=True, C=True)]
simplify_givens_1_expected = dict(E=False, G=True, C=True)
def simplify_givens_1_testanswer(val, original_val = None) :
    return val == simplify_givens_1_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = simplify_givens_1_getargs,
          testanswer = simplify_givens_1_testanswer,
          expected_val = str(simplify_givens_1_expected),
          name = 'simplify_givens')

def simplify_givens_2_getargs() :  #TEST 19
    return [net_dsep.copy(), 'C', dict(A=True, E=False, G=True, D=True)]
simplify_givens_2_expected = dict(A=True, E=False, G=True, D=True)
def simplify_givens_2_testanswer(val, original_val = None) :
    return val == simplify_givens_2_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = simplify_givens_2_getargs,
          testanswer = simplify_givens_2_testanswer,
          expected_val = str(simplify_givens_2_expected),
          name = 'simplify_givens')

def simplify_givens_3_getargs() :  #TEST 20
    return [net_dsep.copy(), 'C', dict(A=True, E=False, G=True, B=False, D=True)]
simplify_givens_3_expected = dict(A=True, E=False, G=True, B=False, D=True)
def simplify_givens_3_testanswer(val, original_val = None) :
    return val == simplify_givens_3_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = simplify_givens_3_getargs,
          testanswer = simplify_givens_3_testanswer,
          expected_val = str(simplify_givens_3_expected),
          name = 'simplify_givens')

def simplify_givens_4_getargs() :  #TEST 21
    return [net_racoon.copy(), 'D', dict(B=True, T=True)]
simplify_givens_4_expected = dict(B=True, T=True)
def simplify_givens_4_testanswer(val, original_val = None) :
    return val == simplify_givens_4_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = simplify_givens_4_getargs,
          testanswer = simplify_givens_4_testanswer,
          expected_val = str(simplify_givens_4_expected),
          name = 'simplify_givens')


def probability_lookup_0_getargs() :  #TEST 22
    return [net_racoon.copy(), {'B':True}]
probability_lookup_0_expected = 0.1
def probability_lookup_0_testanswer(val, original_val = None) :
    return approx_equal(val, probability_lookup_0_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_lookup_0_getargs,
          testanswer = probability_lookup_0_testanswer,
          expected_val = str(probability_lookup_0_expected),
          name = 'probability_lookup')

def probability_lookup_1_getargs() :  #TEST 23
    return [net_racoon.copy(), {'D':True}, {'B':True, 'R':False}]
probability_lookup_1_expected = 0.8
def probability_lookup_1_testanswer(val, original_val = None) :
    return approx_equal(val, probability_lookup_1_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_lookup_1_getargs,
          testanswer = probability_lookup_1_testanswer,
          expected_val = str(probability_lookup_1_expected),
          name = 'probability_lookup')

#implicitly uses infer_missing
def probability_lookup_2_getargs() :  #TEST 24
    return [net_racoon.copy(), {'D':False}, {'B':True, 'R':False}]
probability_lookup_2_expected = 0.2
def probability_lookup_2_testanswer(val, original_val = None) :
    return approx_equal(val, probability_lookup_2_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_lookup_2_getargs,
          testanswer = probability_lookup_2_testanswer,
          expected_val = str(probability_lookup_2_expected),
          name = 'probability_lookup')

def probability_lookup_3_getargs() :  #TEST 25
    return [net_racoon.copy(), {'D':True}, {'B':True}]
probability_lookup_3_expected = LookupError
def probability_lookup_3_testanswer(val, original_val = None) :
    return val == probability_lookup_3_expected
make_test(type = 'FUNCTION_EXPECTING_EXCEPTION',
          getargs = probability_lookup_3_getargs,
          testanswer = probability_lookup_3_testanswer,
          expected_val = str(probability_lookup_3_expected),
          name = 'probability_lookup')

#requires removing non-descendants
def probability_lookup_4_getargs() :  #TEST 26
    return [net_racoon.copy(), {'D':False}, {'B':True, 'R':False, 'T':True}]
probability_lookup_4_expected = 0.2
def probability_lookup_4_testanswer(val, original_val = None) :
    return approx_equal(val, probability_lookup_4_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_lookup_4_getargs,
          testanswer = probability_lookup_4_testanswer,
          expected_val = (str(probability_lookup_4_expected)
                          + '  (Hint: Did you simplify the givens?)'),
          name = 'probability_lookup')

def probability_lookup_5_getargs() :  #TEST 27
    return [net_basic_probs.copy(), {'A':True}, {'B':True, 'C':False}]
probability_lookup_5_expected = LookupError
def probability_lookup_5_testanswer(val, original_val = None) :
    return val == probability_lookup_5_expected
make_test(type = 'FUNCTION_EXPECTING_EXCEPTION',
          getargs = probability_lookup_5_getargs,
          testanswer = probability_lookup_5_testanswer,
          expected_val = str(probability_lookup_5_expected),
          name = 'probability_lookup')


def probability_joint_0_getargs() :  #TEST 28
    return [net_racoon.copy(), {v:True for v in 'BRDTC'}]
probability_joint_0_expected = 0.0288
def probability_joint_0_testanswer(val, original_val = None) :
    return approx_equal(val, probability_joint_0_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_joint_0_getargs,
          testanswer = probability_joint_0_testanswer,
          expected_val = str(probability_joint_0_expected),
          name = 'probability_joint')

def probability_joint_1_getargs() :  #TEST 29
    return [net_racoon.copy(), {v:False for v in 'BRDTC'}]
probability_joint_1_expected = 0.43663455
def probability_joint_1_testanswer(val, original_val = None) :
    return approx_equal(val, probability_joint_1_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_joint_1_getargs,
          testanswer = probability_joint_1_testanswer,
          expected_val = str(probability_joint_1_expected),
          name = 'probability_joint')

def probability_joint_2_getargs() :  #TEST 30
    return [net_racoon.copy(), dict(B=False, R=False, D=True, T=False, C=True)]
probability_joint_2_expected = 0.003564
def probability_joint_2_testanswer(val, original_val = None) :
    return approx_equal(val, probability_joint_2_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_joint_2_getargs,
          testanswer = probability_joint_2_testanswer,
          expected_val = str(probability_joint_2_expected),
          name = 'probability_joint')


def probability_marginal_0_getargs() :  #TEST 31
    return [net_racoon.copy(), {'B':False}]
probability_marginal_0_expected = 0.9
def probability_marginal_0_testanswer(val, original_val = None) :
    return approx_equal(val, probability_marginal_0_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_marginal_0_getargs,
          testanswer = probability_marginal_0_testanswer,
          expected_val = str(probability_marginal_0_expected),
          name = 'probability_marginal')

def probability_marginal_1_getargs() :  #TEST 32
    return [net_racoon.copy(), {'D':False}]
probability_marginal_1_expected = 0.6405
def probability_marginal_1_testanswer(val, original_val = None) :
    return approx_equal(val, probability_marginal_1_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_marginal_1_getargs,
          testanswer = probability_marginal_1_testanswer,
          expected_val = str(probability_marginal_1_expected),
          name = 'probability_marginal')

def probability_marginal_2_getargs() :  #TEST 33
    return [net_racoon.copy(), {'T':True, 'C':False}]
probability_marginal_2_expected = 0.20151845
def probability_marginal_2_testanswer(val, original_val = None) :
    return approx_equal(val, probability_marginal_2_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_marginal_2_getargs,
          testanswer = probability_marginal_2_testanswer,
          expected_val = str(probability_marginal_2_expected),
          name = 'probability_marginal')

def probability_marginal_3_getargs() :  #TEST 34
    return [net_racoon.copy(), dict(B=False, R=False, D=True, T=False, C=True)]
probability_marginal_3_expected = 0.003564
def probability_marginal_3_testanswer(val, original_val = None) :
    return approx_equal(val, probability_marginal_3_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_marginal_3_getargs,
          testanswer = probability_marginal_3_testanswer,
          expected_val = str(probability_marginal_3_expected),
          name = 'probability_marginal')

#non-boolean
def probability_marginal_4_getargs() :  #TEST 35
    return [net_basic_nonboolean2_probs.copy(), {'C':2}]
probability_marginal_4_expected = 0.382
def probability_marginal_4_testanswer(val, original_val = None) :
    return approx_equal(val, probability_marginal_4_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_marginal_4_getargs,
          testanswer = probability_marginal_4_testanswer,
          expected_val = str(probability_marginal_4_expected),
          name = 'probability_marginal')


def probability_conditional_0_getargs() :  #TEST 36
    return [net_racoon.copy(), {'D':True}, dict(B=True, R=False, T=False)]
probability_conditional_0_expected = 0.8
def probability_conditional_0_testanswer(val, original_val = None) :
    return approx_equal(val, probability_conditional_0_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_conditional_0_getargs,
          testanswer = probability_conditional_0_testanswer,
          expected_val = str(probability_conditional_0_expected),
          name = 'probability_conditional')

def probability_conditional_1_getargs() :  #TEST 37
    return [net_racoon.copy(), {'B':True, 'R':True}, {'D':False, 'T':False}]
probability_conditional_1_expected = 0.001/0.487945
def probability_conditional_1_testanswer(val, original_val = None) :
    return approx_equal(val, probability_conditional_1_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_conditional_1_getargs,
          testanswer = probability_conditional_1_testanswer,
          expected_val = str(probability_conditional_1_expected),
          name = 'probability_conditional')

#just calls probability_lookup
def probability_conditional_2_getargs() :  #TEST 38
    return [net_racoon.copy(), {'D':False}, {'B':True, 'R':False}]
probability_conditional_2_expected = 0.2
def probability_conditional_2_testanswer(val, original_val = None) :
    return approx_equal(val, probability_conditional_2_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_conditional_2_getargs,
          testanswer = probability_conditional_2_testanswer,
          expected_val = str(probability_conditional_2_expected),
          name = 'probability_conditional')

#no givens; just calls probability_marginal
def probability_conditional_3_getargs() :  #TEST 39
    return [net_racoon.copy(), dict(B=False, R=False, D=True, T=False, C=True)]
probability_conditional_3_expected = 0.003564
def probability_conditional_3_testanswer(val, original_val = None) :
    return approx_equal(val, probability_conditional_3_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_conditional_3_getargs,
          testanswer = probability_conditional_3_testanswer,
          expected_val = str(probability_conditional_3_expected),
          name = 'probability_conditional')

#empty givens; can just call probability_marginal
def probability_conditional_4_getargs() :  #TEST 40
    return [net_racoon.copy(), dict(B=False, R=False, D=True, T=False, C=True), {}]
probability_conditional_4_expected = 0.003564
def probability_conditional_4_testanswer(val, original_val = None) :
    return approx_equal(val, probability_conditional_4_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_conditional_4_getargs,
          testanswer = probability_conditional_4_testanswer,
          expected_val = str(probability_conditional_4_expected),
          name = 'probability_conditional')

#P(A|A) = 1, always
def probability_conditional_5_getargs() :  #TEST 41
    return [net_basic_probs.copy(), {'A':True}, {'A':True}]
probability_conditional_5_expected = 1.0
def probability_conditional_5_testanswer(val, original_val = None) :
    return approx_equal(val, probability_conditional_5_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_conditional_5_getargs,
          testanswer = probability_conditional_5_testanswer,
          expected_val = (str(probability_conditional_5_expected)
                          +  '  (Hint: What is P(A|A), in general?)'),
          name = 'probability_conditional')

#P(A=True|A=False) = 0, always
def probability_conditional_6_getargs() :  #TEST 42
    return [net_basic_probs.copy(), {'A':True}, {'A':False}]
probability_conditional_6_expected = 0.0
def probability_conditional_6_testanswer(val, original_val = None) :
    return approx_equal(val, probability_conditional_6_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_conditional_6_getargs,
          testanswer = probability_conditional_6_testanswer,
          expected_val = (str(probability_conditional_6_expected)
                          +  '  (Hint: What is P(A=True|A=False), in general?)'),
          name = 'probability_conditional')

#P(A=a1|A=a2) = 0, always
def probability_conditional_6a_getargs() :  #TEST 43
    return [net_basic_nonboolean2_probs.copy(), {'C':2}, {'C':3}]
probability_conditional_6a_expected = 0.0
def probability_conditional_6a_testanswer(val, original_val = None) :
    return approx_equal(val, probability_conditional_6a_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_conditional_6a_getargs,
          testanswer = probability_conditional_6a_testanswer,
          expected_val = (str(probability_conditional_6a_expected)
                          +  '  (Hint: What is P(A=a1|A=a2), in general?)'),
          name = 'probability_conditional')

#P(AB|A=False) = 0, always
def probability_conditional_7_getargs() :  #TEST 44
    return [net_basic_probs.copy(), {'A':True, 'B':True}, {'A':False}]
probability_conditional_7_expected = 0.0
def probability_conditional_7_testanswer(val, original_val = None) :
    return approx_equal(val, probability_conditional_7_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_conditional_7_getargs,
          testanswer = probability_conditional_7_testanswer,
          expected_val = (str(probability_conditional_7_expected)
                          +  '  (Hint: What is P(A=True,B=True|A=False), in general?)'),
          name = 'probability_conditional')


def probability_0_getargs() :  #TEST 45
    return [net_racoon.copy(), {'B':False}]
probability_0_expected = 0.9
def probability_0_testanswer(val, original_val = None) :
    return approx_equal(val, probability_0_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_0_getargs,
          testanswer = probability_0_testanswer,
          expected_val = str(probability_0_expected),
          name = 'probability')

def probability_1_getargs() :  #TEST 46
    return [net_racoon.copy(), {'D':True}, dict(B=True, R=False, T=False)]
probability_1_expected = 0.8
def probability_1_testanswer(val, original_val = None) :
    return approx_equal(val, probability_1_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_1_getargs,
          testanswer = probability_1_testanswer,
          expected_val = str(probability_1_expected),
          name = 'probability')

def probability_2_getargs() :  #TEST 47
    return [net_racoon.copy(), {'D':False}]
probability_2_expected = 0.6405
def probability_2_testanswer(val, original_val = None) :
    return approx_equal(val, probability_2_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_2_getargs,
          testanswer = probability_2_testanswer,
          expected_val = str(probability_2_expected),
          name = 'probability')

def probability_3_getargs() :  #TEST 48
    return [net_racoon.copy(), {'T':True, 'C':False}]
probability_3_expected = 0.20151845
def probability_3_testanswer(val, original_val = None) :
    return approx_equal(val, probability_3_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_3_getargs,
          testanswer = probability_3_testanswer,
          expected_val = str(probability_3_expected),
          name = 'probability')

def probability_4_getargs() :  #TEST 49
    return [net_racoon.copy(), {'B':True, 'R':True}, {'D':False, 'T':False}]
probability_4_expected = 0.001/0.487945
def probability_4_testanswer(val, original_val = None) :
    return approx_equal(val, probability_4_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_4_getargs,
          testanswer = probability_4_testanswer,
          expected_val = str(probability_4_expected),
          name = 'probability')

def probability_5_getargs() :  #TEST 50
    return [net_racoon.copy(), {v:False for v in 'BRDTC'}]
probability_5_expected = 0.43663455
def probability_5_testanswer(val, original_val = None) :
    return approx_equal(val, probability_5_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_5_getargs,
          testanswer = probability_5_testanswer,
          expected_val = str(probability_5_expected),
          name = 'probability')

def probability_6_getargs() :  #TEST 51
    return [net_racoon.copy(), dict(B=False, R=False, D=True, T=False, C=True)]
probability_6_expected = 0.003564
def probability_6_testanswer(val, original_val = None) :
    return approx_equal(val, probability_6_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = probability_6_getargs,
          testanswer = probability_6_testanswer,
          expected_val = str(probability_6_expected),
          name = 'probability')


def number_of_parameters_0_getargs() :  #TEST 52
    return [net_basic.copy()]
number_of_parameters_0_expected = 6
def number_of_parameters_0_testanswer(val, original_val = None) :
    return val == number_of_parameters_0_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = number_of_parameters_0_getargs,
          testanswer = number_of_parameters_0_testanswer,
          expected_val = str(number_of_parameters_0_expected),
          name = 'number_of_parameters')

def number_of_parameters_1_getargs() :  #TEST 53
    return [net_racoon_no_probs.copy()]
number_of_parameters_1_expected = 10
def number_of_parameters_1_testanswer(val, original_val = None) :
    return val == number_of_parameters_1_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = number_of_parameters_1_getargs,
          testanswer = number_of_parameters_1_testanswer,
          expected_val = str(number_of_parameters_1_expected),
          name = 'number_of_parameters')

def number_of_parameters_2_getargs() :  #TEST 54
    return [net_dsep.copy()]
number_of_parameters_2_expected = 14
def number_of_parameters_2_testanswer(val, original_val = None) :
    return val == number_of_parameters_2_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = number_of_parameters_2_getargs,
          testanswer = number_of_parameters_2_testanswer,
          expected_val = str(number_of_parameters_2_expected),
          name = 'number_of_parameters')

# 2 params for A, 1 for B, 3*2*(5-1)=24 for C
def number_of_parameters_3_getargs() :  #TEST 55
    return [net_basic_nonboolean.copy()]
number_of_parameters_3_expected = 27
def number_of_parameters_3_testanswer(val, original_val = None) :
    return val == number_of_parameters_3_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = number_of_parameters_3_getargs,
          testanswer = number_of_parameters_3_testanswer,
          expected_val = (str(number_of_parameters_3_expected)
                          +"  (Hint: What happens if variables are non-boolean?)"),
          name = 'number_of_parameters')


def independent_0_getargs() :  #TEST 56
    return [net_racoon.copy(), 'B', 'R']
independent_0_expected = True
def independent_0_testanswer(val, original_val = None) :
    return val == independent_0_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = independent_0_getargs,
          testanswer = independent_0_testanswer,
          expected_val = str(independent_0_expected),
          name = 'is_independent')

def independent_1_getargs() :  #TEST 57
    return [net_racoon.copy(), 'B', 'R', {'D':True}]
independent_1_expected = False
def independent_1_testanswer(val, original_val = None) :
    return val == independent_1_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = independent_1_getargs,
          testanswer = independent_1_testanswer,
          expected_val = str(independent_1_expected),
          name = 'is_independent')

def independent_2_getargs() :  #TEST 58
    return [net_racoon.copy(), 'D', 'T', {'B':True, 'R':False}]
independent_2_expected = True
def independent_2_testanswer(val, original_val = None) :
    return val == independent_2_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = independent_2_getargs,
          testanswer = independent_2_testanswer,
          expected_val = str(independent_2_expected),
          name = 'is_independent')

def independent_3_getargs() :  #TEST 59
    return [net_basic_probs.copy(), 'A', 'B', {}]
independent_3_expected = True
def independent_3_testanswer(val, original_val = None) :
    return val == independent_3_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = independent_3_getargs,
          testanswer = independent_3_testanswer,
          expected_val = str(independent_3_expected),
          name = 'is_independent')

def independent_4_getargs() :  #TEST 60
    return [net_basic_probs.copy(), 'B', 'C', {'A':False}]
independent_4_expected = True
def independent_4_testanswer(val, original_val = None) :
    return val == independent_4_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = independent_4_getargs,
          testanswer = independent_4_testanswer,
          expected_val = str(independent_4_expected),
          name = 'is_independent')

def independent_5_getargs() :  #TEST 61
    return [net_basic_probs.copy(), 'C', 'B', {'A':False}]
independent_5_expected = True
def independent_5_testanswer(val, original_val = None) :
    return val == independent_5_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = independent_5_getargs,
          testanswer = independent_5_testanswer,
          expected_val = str(independent_5_expected),
          name = 'is_independent')

def independent_6_getargs() :  #TEST 62
    return [net_basic_probs.copy(), 'B', 'C', {'A':True}]
independent_6_expected = False
def independent_6_testanswer(val, original_val = None) :
    return val == independent_6_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = independent_6_getargs,
          testanswer = independent_6_testanswer,
          expected_val = str(independent_6_expected),
          name = 'is_independent')

def independent_7_getargs() :  #TEST 63
    return [net_basic_probs.copy(), 'B', 'C']
independent_7_expected = False
def independent_7_testanswer(val, original_val = None) :
    return val == independent_7_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = independent_7_getargs,
          testanswer = independent_7_testanswer,
          expected_val = str(independent_7_expected),
          name = 'is_independent')

def independent_8_getargs() :  #TEST 64
    return [net_basic_nonboolean2_probs.copy(), 'B', 'C', {'A':False}]
independent_8_expected = False
def independent_8_testanswer(val, original_val = None) :
    return val == independent_8_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = independent_8_getargs,
          testanswer = independent_8_testanswer,
          expected_val = (str(independent_8_expected)
                          + '  (Hint: What if variables are non-boolean?)'),
          name = 'is_independent')

def independent_9_getargs() :  #TEST 65
    return [net_basic_nonboolean2_probs.copy(), 'C', 'B', {'A':False}]
independent_9_expected = False
def independent_9_testanswer(val, original_val = None) :
    return val == independent_9_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = independent_9_getargs,
          testanswer = independent_9_testanswer,
          expected_val = (str(independent_9_expected)
                          + '  (Hint: What if variables are non-boolean?)'),
          name = 'is_independent')


# is_structurally_independent

#print is_structurally_independent(net_dsep, 'A', 'B', {'D':True, 'F':True}) #False
def is_structurally_independent_0_getargs() :  #TEST 66
    return [net_dsep.copy(), 'A', 'B', {'D':True, 'F':True}]
is_structurally_independent_0_expected = False
def is_structurally_independent_0_testanswer(val, original_val = None) :
    return val == is_structurally_independent_0_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_0_getargs,
          testanswer = is_structurally_independent_0_testanswer,
          expected_val = str(is_structurally_independent_0_expected),
          name = 'is_structurally_independent')

#print is_structurally_independent(net_dsep, 'A', 'B') #True
def is_structurally_independent_1_getargs() :  #TEST 67
    return [net_dsep.copy(), 'A', 'B']
is_structurally_independent_1_expected = True
def is_structurally_independent_1_testanswer(val, original_val = None) :
    return val == is_structurally_independent_1_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_1_getargs,
          testanswer = is_structurally_independent_1_testanswer,
          expected_val = str(is_structurally_independent_1_expected),
          name = 'is_structurally_independent')

#print is_structurally_independent(net_dsep, 'A', 'B', {'C':True}) #False
def is_structurally_independent_2_getargs() :  #TEST 68
    return [net_dsep.copy(), 'A', 'B', {'C':True}]
is_structurally_independent_2_expected = False
def is_structurally_independent_2_testanswer(val, original_val = None) :
    return val == is_structurally_independent_2_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_2_getargs,
          testanswer = is_structurally_independent_2_testanswer,
          expected_val = str(is_structurally_independent_2_expected),
          name = 'is_structurally_independent')

#print is_structurally_independent(net_dsep, 'A', 'B', {'C':False}) #False
def is_structurally_independent_3_getargs() :  #TEST 69
    return [net_dsep.copy(), 'A', 'B', {'C':False}]
is_structurally_independent_3_expected = False
def is_structurally_independent_3_testanswer(val, original_val = None) :
    return val == is_structurally_independent_3_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_3_getargs,
          testanswer = is_structurally_independent_3_testanswer,
          expected_val = str(is_structurally_independent_3_expected),
          name = 'is_structurally_independent')

#print is_structurally_independent(net_dsep, 'D', 'E', {'C':True}) #True
def is_structurally_independent_4_getargs() :  #TEST 70
    return [net_dsep.copy(), 'D', 'E', {'C':True}]
is_structurally_independent_4_expected = True
def is_structurally_independent_4_testanswer(val, original_val = None) :
    return val == is_structurally_independent_4_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_4_getargs,
          testanswer = is_structurally_independent_4_testanswer,
          expected_val = str(is_structurally_independent_4_expected),
          name = 'is_structurally_independent')

#print is_structurally_independent(net_dsep, 'D', 'E', {'C':False}) #True
def is_structurally_independent_5_getargs() :  #TEST 71
    return [net_dsep.copy(), 'D', 'E', {'C':False}]
is_structurally_independent_5_expected = True
def is_structurally_independent_5_testanswer(val, original_val = None) :
    return val == is_structurally_independent_5_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_5_getargs,
          testanswer = is_structurally_independent_5_testanswer,
          expected_val = str(is_structurally_independent_5_expected),
          name = 'is_structurally_independent')

#print is_structurally_independent(net_dsep, 'D', 'E', {}) #False
def is_structurally_independent_6_getargs() :  #TEST 72
    return [net_dsep.copy(), 'D', 'E', {}]
is_structurally_independent_6_expected = False
def is_structurally_independent_6_testanswer(val, original_val = None) :
    return val == is_structurally_independent_6_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_6_getargs,
          testanswer = is_structurally_independent_6_testanswer,
          expected_val = str(is_structurally_independent_6_expected),
          name = 'is_structurally_independent')

#print is_structurally_independent(net_dsep, 'D', 'E', {'A':False, 'B':True}) #False
def is_structurally_independent_7_getargs() :  #TEST 73
    return [net_dsep.copy(), 'D', 'E', {'A':False, 'B':True}]
is_structurally_independent_7_expected = False
def is_structurally_independent_7_testanswer(val, original_val = None) :
    return val == is_structurally_independent_7_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_7_getargs,
          testanswer = is_structurally_independent_7_testanswer,
          expected_val = str(is_structurally_independent_7_expected),
          name = 'is_structurally_independent')

#print is_structurally_independent(net_dsep, 'D', 'G', {'C':True}) #False
def is_structurally_independent_8_getargs() :  #TEST 74
    return [net_dsep.copy(), 'D', 'G', {'C':True}]
is_structurally_independent_8_expected = False
def is_structurally_independent_8_testanswer(val, original_val = None) :
    return val == is_structurally_independent_8_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_8_getargs,
          testanswer = is_structurally_independent_8_testanswer,
          expected_val = str(is_structurally_independent_8_expected),
          name = 'is_structurally_independent')

#print is_structurally_independent(net_dsep, 'A', 'B', {'C':True}) #False
def is_structurally_independent_9_getargs() :  #TEST 75
    return [net_dsep.copy(), 'A', 'B', {'C':True}]
is_structurally_independent_9_expected = False
def is_structurally_independent_9_testanswer(val, original_val = None) :
    return val == is_structurally_independent_9_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_9_getargs,
          testanswer = is_structurally_independent_9_testanswer,
          expected_val = str(is_structurally_independent_9_expected),
          name = 'is_structurally_independent')

# What happens if var1 == var2?
#print is_structurally_independent(net_dsep, 'A', 'A') #False
def is_structurally_independent_10_getargs() :  #TEST 76
    return [net_dsep.copy(), 'A', 'A']
is_structurally_independent_10_expected = False
def is_structurally_independent_10_testanswer(val, original_val = None) :
    return val == is_structurally_independent_10_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_10_getargs,
          testanswer = is_structurally_independent_10_testanswer,
          expected_val = (str(is_structurally_independent_10_expected)
                          + "  (Hint: What happens if var1 == var2?)"),
          name = 'is_structurally_independent')

# Don't marry grandparents
#print is_structurally_independent(net_grandparents, 'GP1', 'GP2', {'C':True, 'P1':True, 'P2':True}) #True
def is_structurally_independent_11_getargs() :  #TEST 77
    return [net_grandparents.copy(), 'GP1', 'GP2', {'C':True, 'P1':True, 'P2':True}]
is_structurally_independent_11_expected = True
def is_structurally_independent_11_testanswer(val, original_val = None) :
    return val == is_structurally_independent_11_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_11_getargs,
          testanswer = is_structurally_independent_11_testanswer,
          expected_val = (str(is_structurally_independent_11_expected)
                          + "  (Hint: Don't marry grandparents, unless they're also parents)"),
          name = 'is_structurally_independent')

# Ignore numerical independence
#print is_independent(net_basic_probs, 'C', 'B', {'A':False}) #True (numerical indepencence)
#print is_structurally_independent(net_basic_probs, 'C', 'B', {'A':False}) #False
def is_structurally_independent_12_getargs() :  #TEST 78
    return [net_basic_probs.copy(), 'C', 'B', {'A':False}]
is_structurally_independent_12_expected = False
def is_structurally_independent_12_testanswer(val, original_val = None) :
    return val == is_structurally_independent_12_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_12_getargs,
          testanswer = is_structurally_independent_12_testanswer,
          expected_val = (str(is_structurally_independent_12_expected)
                          + "  (Hint: Only consider structural independence)"),
          name = 'is_structurally_independent')

# Only marry parents
#print is_structurally_independent(net_W, 'E', 'B', {'D':True, 'C':True, 'F':True}) #True
def is_structurally_independent_13_getargs() :  #TEST 79
    return [net_W, 'E', 'B', {'D':True, 'C':True, 'F':True}]
is_structurally_independent_13_expected = True
def is_structurally_independent_13_testanswer(val, original_val = None) :
    return val == is_structurally_independent_13_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_13_getargs,
          testanswer = is_structurally_independent_13_testanswer,
          expected_val = (str(is_structurally_independent_13_expected)
                          + "  (Hint: Only marry parents. Beware of creating new parents!)"),
          name = 'is_structurally_independent')

# Only marry parents
#print is_structurally_independent(net_W, 'E', 'G', {'D':True, 'C':True, 'F':True}) #True
def is_structurally_independent_14_getargs() :  #TEST 80
    return [net_W, 'E', 'G', {'D':True, 'C':True, 'F':True}]
is_structurally_independent_14_expected = True
def is_structurally_independent_14_testanswer(val, original_val = None) :
    return val == is_structurally_independent_14_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_14_getargs,
          testanswer = is_structurally_independent_14_testanswer,
          expected_val = (str(is_structurally_independent_14_expected)
                          + "  (Hint: Only marry parents. Beware of creating new parents!)"),
          name = 'is_structurally_independent')

# Only marry parents
#print is_structurally_independent(net_W, 'H', 'D', {'B':True, 'C':True, 'F':True, 'G':True}) #True
def is_structurally_independent_15_getargs() :  #TEST 81
    return [net_W, 'H', 'D', {'B':True, 'C':True, 'F':True, 'G':True}]
is_structurally_independent_15_expected = True
def is_structurally_independent_15_testanswer(val, original_val = None) :
    return val == is_structurally_independent_15_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_15_getargs,
          testanswer = is_structurally_independent_15_testanswer,
          expected_val = (str(is_structurally_independent_15_expected)
                          + "  (Hint: Only marry parents. Beware of creating new parents!)"),
          name = 'is_structurally_independent')

# Only marry parents
#print is_structurally_independent(net_W, 'A', 'D', {'B':True, 'C':True, 'F':True, 'G':True}) #True
def is_structurally_independent_16_getargs() :  #TEST 82
    return [net_W, 'A', 'D', {'B':True, 'C':True, 'F':True, 'G':True}]
is_structurally_independent_16_expected = True
def is_structurally_independent_16_testanswer(val, original_val = None) :
    return val == is_structurally_independent_16_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_structurally_independent_16_getargs,
          testanswer = is_structurally_independent_16_testanswer,
          expected_val = (str(is_structurally_independent_16_expected)
                          + "  (Hint: Only marry parents. Beware of creating new parents!)"),
          name = 'is_structurally_independent')
