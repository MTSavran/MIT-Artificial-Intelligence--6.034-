# MIT 6.034 Lab 9: Boosting (Adaboost)

from tester import make_test, get_tests
from utils import *

lab_number = 9 #for tester.py

F = Fraction #lazy alias

def initialize_2_getargs() :  #TEST 1
    return [["PointA"]]
initialize_2_expected = {"PointA":1}
def initialize_2_testanswer(val, original_val = None) :
    return val == initialize_2_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = initialize_2_getargs,
          testanswer = initialize_2_testanswer,
          expected_val = str(initialize_2_expected),
          name = 'initialize_weights')

def initialize_3_getargs() :  #TEST 2
    return [["-6","-5","-4","-3","-2","-1","0","1","2","3","4","5"]]
initialize_3_expected = {"-6":F(1,12),"-5":F(1,12),"-4":F(1,12),
                         "-3":F(1,12),"-2":F(1,12),"-1":F(1,12),
                         "0":F(1,12),"1":F(1,12),"2":F(1,12),
                         "3":F(1,12),"4":F(1,12),"5":F(1,12)}
def initialize_3_testanswer(val, original_val = None) :
    return val == initialize_3_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = initialize_3_getargs,
          testanswer = initialize_3_testanswer,
          expected_val = str(initialize_3_expected),
          name = 'initialize_weights')


# TEST 0 FOR CALCULATE_ERROR_RATE - ALL POINTS CORRECTLY CLASSIFIED
# only one classifier
def calculate_error_rates_0_getargs() :  #TEST 3
    return [{"0" : F(1,4), "1": F(1,4), "2": F(1,4), "3": F(1,4)}, {"classifier_0":[]}]
calculate_error_rates_0_expected = {"classifier_0" : 0}
def calculate_error_rates_0_testanswer(val, original_val = None) :
    return val == calculate_error_rates_0_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = calculate_error_rates_0_getargs,
          testanswer = calculate_error_rates_0_testanswer,
          expected_val = str(calculate_error_rates_0_expected),
          name = 'calculate_error_rates')

# TEST 2 FOR CALCULATE_ERROR_RATE - SOME POINTS MISCLASSIFIED
def calculate_error_rates_2_getargs() :  #TEST 4
    return [{"0" : F(1,8), "1": F(1,8), "2": F(1,8), "3": F(1,8), "4": F(1,2)},
             {"classifier_0":["0", "1", "4"], "classifier_1":["0", "1", "2", "3"]}]
calculate_error_rates_2_expected = {"classifier_0" : F(3,4), "classifier_1": F(1,2)}
def calculate_error_rates_2_testanswer(val, original_val = None) :
    return val == calculate_error_rates_2_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = calculate_error_rates_2_getargs,
          testanswer = calculate_error_rates_2_testanswer,
          expected_val = str(calculate_error_rates_2_expected),
          name = 'calculate_error_rates')


def pick_best_classifier_0_getargs() :  #TEST 5
    #have a perfect test!
    classifier_to_error_rate = {}
    classifier_to_error_rate["classifier_0"] = 0
    classifier_to_error_rate["classifier_1/10"] = F(1,10)
    classifier_to_error_rate["classifier_1/2"] = F(1,2)
    classifier_to_error_rate["classifier_9/10"] = F(9,10)
    return [classifier_to_error_rate]

pick_best_classifier_0_expected = "classifier_0"

def pick_best_classifier_0_testanswer(val, original_val = None) :
    return val == pick_best_classifier_0_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = pick_best_classifier_0_getargs,
          testanswer = pick_best_classifier_0_testanswer,
          expected_val = str(pick_best_classifier_0_expected),
          name = 'pick_best_classifier')

def pick_best_classifier_1_getargs() :  #TEST 6
    #have a pretty good test
    classifier_to_error_rate = {}
    classifier_to_error_rate["classifier_1/10"] = F(1,10)
    classifier_to_error_rate["classifier_1/2"] = F(1,2)
    classifier_to_error_rate["classifier_9/10"] = F(9,10)
    return [classifier_to_error_rate]

pick_best_classifier_1_expected = "classifier_1/10"

def pick_best_classifier_1_testanswer(val, original_val = None) :
    return val == pick_best_classifier_1_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = pick_best_classifier_1_getargs,
          testanswer = pick_best_classifier_1_testanswer,
          expected_val = str(pick_best_classifier_1_expected),
          name = 'pick_best_classifier')

def pick_best_classifier_2_getargs() :  #TEST 7
    #no good tests; raise error
    classifier_to_error_rate = {}
    classifier_to_error_rate["classifier_1/2"] = F(1,2)
    classifier_to_error_rate["classifier_6/10"] = F(6,10)
    classifier_to_error_rate["classifier_9/10"] = F(9,10)
    return [classifier_to_error_rate]

pick_best_classifier_2_expected = NoGoodClassifiersError

def pick_best_classifier_2_testanswer(val, original_val = None) :
    return val == pick_best_classifier_2_expected
make_test(type = 'FUNCTION_EXPECTING_EXCEPTION',
          getargs = pick_best_classifier_2_getargs,
          testanswer = pick_best_classifier_2_testanswer,
          expected_val = str(pick_best_classifier_2_expected),
          name = 'pick_best_classifier')

def pick_best_classifier_2a_getargs() :  #TEST 8
    #no good tests; raise error
    return [dict(cl1=F(1,2), cl2=F(1,2)), False]

pick_best_classifier_2a_expected = NoGoodClassifiersError

def pick_best_classifier_2a_testanswer(val, original_val = None) :
    return val == pick_best_classifier_2a_expected
make_test(type = 'FUNCTION_EXPECTING_EXCEPTION',
          getargs = pick_best_classifier_2a_getargs,
          testanswer = pick_best_classifier_2a_testanswer,
          expected_val = str(pick_best_classifier_2a_expected),
          name = 'pick_best_classifier')

def pick_best_classifier_2b_getargs() :  #TEST 9
    #lowest error rate is 1/2, but best test is 9/10
    classifier_to_error_rate = {}
    classifier_to_error_rate["classifier_1/2"] = F(1,2)
    classifier_to_error_rate["classifier_6/10"] = F(6,10)
    classifier_to_error_rate["classifier_9/10"] = F(9,10)
    return [classifier_to_error_rate, False]

pick_best_classifier_2b_expected = "classifier_9/10"

def pick_best_classifier_2b_testanswer(val, original_val = None) :
    return val == pick_best_classifier_2b_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = pick_best_classifier_2b_getargs,
          testanswer = pick_best_classifier_2b_testanswer,
          expected_val = str(pick_best_classifier_2b_expected),
          name = 'pick_best_classifier')

def pick_best_classifier_4_getargs() :  #TEST 10
    #have perfectly wrong test
    classifier_to_error_rate = {}
    classifier_to_error_rate["classifier_1/10"] = F(1,10)
    classifier_to_error_rate["classifier_6/10"] = F(6,10)
    classifier_to_error_rate["classifier_9/10"] = F(9,10)
    classifier_to_error_rate["classifier_1"] = 1
    return [classifier_to_error_rate, False]

pick_best_classifier_4_expected = "classifier_1"

def pick_best_classifier_4_testanswer(val, original_val = None) :
    return val == pick_best_classifier_4_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = pick_best_classifier_4_getargs,
          testanswer = pick_best_classifier_4_testanswer,
          expected_val = str(pick_best_classifier_4_expected),
          name = 'pick_best_classifier')

#check tie-breaking
def pick_best_classifier_5_getargs() :  #TEST 11
    return [dict(B=F(3,10), A=F(4,10), C=F(3,10))]
pick_best_classifier_5_expected = "B"
def pick_best_classifier_5_testanswer(val, original_val = None) :
    return val == pick_best_classifier_5_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = pick_best_classifier_5_getargs,
          testanswer = pick_best_classifier_5_testanswer,
          expected_val = str(pick_best_classifier_5_expected) \
              +' (Hint: This test checks tie-breaking.)',
          name = 'pick_best_classifier')

#check not comparing floats
def pick_best_classifier_6_getargs() :  #TEST 12
    return [dict(cl_1=F(2,3), cl_2=F(1,3)), False]
pick_best_classifier_6_expected = "cl_1"
def pick_best_classifier_6_testanswer(val, original_val = None) :
    return val == pick_best_classifier_6_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = pick_best_classifier_6_getargs,
          testanswer = pick_best_classifier_6_testanswer,
          expected_val = str(pick_best_classifier_6_expected) \
              +" (Hint: Make sure you're using Fractions, and not comparing floats!)",
          name = 'pick_best_classifier')


def calculate_voting_power_0_getargs() :  #TEST 13
    return [.001]
calculate_voting_power_0_expected = 3.453377389324277
def calculate_voting_power_0_testanswer(val, original_val = None) :
    return approx_equal(val, calculate_voting_power_0_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = calculate_voting_power_0_getargs,
          testanswer = calculate_voting_power_0_testanswer,
          expected_val = str(calculate_voting_power_0_expected),
          name = 'calculate_voting_power')


def calculate_voting_power_3_getargs() :  #TEST 14
    return [.3]
calculate_voting_power_3_expected = 0.42364893019360184
def calculate_voting_power_3_testanswer(val, original_val = None) :
    return approx_equal(val, calculate_voting_power_3_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = calculate_voting_power_3_getargs,
          testanswer = calculate_voting_power_3_testanswer,
          expected_val = str(calculate_voting_power_3_expected),
          name = 'calculate_voting_power')

def calculate_voting_power_4_getargs() :  #TEST 15
    return [.7]
calculate_voting_power_4_expected = -0.4236489301936017
def calculate_voting_power_4_testanswer(val, original_val = None) :
    return approx_equal(val, calculate_voting_power_4_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = calculate_voting_power_4_getargs,
          testanswer = calculate_voting_power_4_testanswer,
          expected_val = str(calculate_voting_power_4_expected),
          name = 'calculate_voting_power')

#perfect classifier -> INF
def calculate_voting_power_5_getargs() :  #TEST 16
    return [0]
calculate_voting_power_5_expected = INF
def calculate_voting_power_5_testanswer(val, original_val = None) :
    return val == calculate_voting_power_5_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = calculate_voting_power_5_getargs,
          testanswer = calculate_voting_power_5_testanswer,
          expected_val = str(calculate_voting_power_5_expected),
          name = 'calculate_voting_power')

#perfectly wrong classifier -> -INF
def calculate_voting_power_6_getargs() :  #TEST 17
    return [1]
calculate_voting_power_6_expected = -INF
def calculate_voting_power_6_testanswer(val, original_val = None) :
    return val == calculate_voting_power_6_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = calculate_voting_power_6_getargs,
          testanswer = calculate_voting_power_6_testanswer,
          expected_val = str(calculate_voting_power_6_expected),
          name = 'calculate_voting_power')


def get_overall_misclassifications_0_getargs() :  #TEST 18
    return [[("h1", 1)], ['ptA','ptB'], {'h1':['ptA','ptB'],'h2':['ptA']}]
get_overall_misclassifications_0_expected = set(['ptA', 'ptB'])
def get_overall_misclassifications_0_testanswer(val, original_val = None) :
    return val == get_overall_misclassifications_0_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_overall_misclassifications_0_getargs,
          testanswer = get_overall_misclassifications_0_testanswer,
          expected_val = str(get_overall_misclassifications_0_expected),
          name = 'get_overall_misclassifications')

#All classifiers included in H
#h with voting power of 0
#H misclassifies A
def get_overall_misclassifications_1_getargs() :  #TEST 19
    return [[("h1", 1),("h2", 0)], ['A','B'], {'h1': ['A'], 'h2': ['B']}]
get_overall_misclassifications_1_expected = set('A')
def get_overall_misclassifications_1_testanswer(val, original_val = None) :
    return val == get_overall_misclassifications_1_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_overall_misclassifications_1_getargs,
          testanswer = get_overall_misclassifications_1_testanswer,
          expected_val = str(get_overall_misclassifications_1_expected),
          name = 'get_overall_misclassifications')

# Not all points misclassified by any classifier
# H misclassifies A & B
def get_overall_misclassifications_2_getargs() :  #TEST 20
    return [[("h1", .5),("h2", .3),("h3", .76)], ['A','B','C','D'],
             {'h1': ['A'], 'h2': ['A','B'], 'h3': ['B','C']}]
get_overall_misclassifications_2_expected = set('AB')
def get_overall_misclassifications_2_testanswer(val, original_val = None) :
    return val == get_overall_misclassifications_2_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_overall_misclassifications_2_getargs,
          testanswer = get_overall_misclassifications_2_testanswer,
          expected_val = str(get_overall_misclassifications_2_expected),
          name = 'get_overall_misclassifications')

#No points misclassified by h3
#H misclassifies C
def get_overall_misclassifications_3_getargs() :  #TEST 21
    return [[("h1", .5),("h2", -.3),("h3", .76)], ['A','B','C'],
             {'h1': ['A','C'], 'h2': ['A','B'], 'h3': []}]
get_overall_misclassifications_3_expected = set('C')
def get_overall_misclassifications_3_testanswer(val, original_val = None) :
    return val == get_overall_misclassifications_3_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_overall_misclassifications_3_getargs,
          testanswer = get_overall_misclassifications_3_testanswer,
          expected_val = str(get_overall_misclassifications_3_expected),
          name = 'get_overall_misclassifications')

#All negative voting powers
#H misclassifies A,B,D
def get_overall_misclassifications_4_getargs() :  #TEST 22
    return [[("h1", -.5),("h2", -.3),("h3", -.45)], ['A','B','C','D'],
             {'h1': ['A','C'], 'h2': ['B','C'], 'h3': ['D']}]
get_overall_misclassifications_4_expected = set('ABD')
def get_overall_misclassifications_4_testanswer(val, original_val = None) :
    return val == get_overall_misclassifications_4_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_overall_misclassifications_4_getargs,
          testanswer = get_overall_misclassifications_4_testanswer,
          expected_val = str(get_overall_misclassifications_4_expected),
          name = 'get_overall_misclassifications')

#misclassified training point is not listed in misclassifications
#same classifier used multiple times
def get_overall_misclassifications_5_getargs() :  #TEST 23
    return [[("h1", -0.549),("h2", 0.347),("h1", -0.255)], list('ABCD'),
             dict(h1=list('ABC'), h2=list('AC'), h3=list('BC'))]
get_overall_misclassifications_5_expected = set('D')
def get_overall_misclassifications_5_testanswer(val, original_val = None) :
    return val == get_overall_misclassifications_5_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_overall_misclassifications_5_getargs,
          testanswer = get_overall_misclassifications_5_testanswer,
          expected_val = str(get_overall_misclassifications_5_expected) \
              +' (Hint: What happens if a training point is misclassified by ' \
              +'H, but not misclassified by any weak classifier?)',
          name = 'get_overall_misclassifications')

#one point misclassified, vote is a tie
# (No, this particular situation would not happen in Adaboost.)
def get_overall_misclassifications_6_getargs() :  #TEST 24
    return [[("h1", 0.5), ("h2", 0.5)], ['A','B'],
             {'h1': ['A'], 'h2': []}]
get_overall_misclassifications_6_expected = set('A')
def get_overall_misclassifications_6_testanswer(val, original_val = None) :
    return val == get_overall_misclassifications_6_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_overall_misclassifications_6_getargs,
          testanswer = get_overall_misclassifications_6_testanswer,
          expected_val = str(get_overall_misclassifications_6_expected) \
              +' (Hint: This test checks what happens when the vote is a tie.)',
          name = 'get_overall_misclassifications')

#violates triangle sum property
def get_overall_misclassifications_7_getargs() :  #TEST 25
    return [[("h1", 0.5), ("h2", 0.2), ("h3", 0.2)], list('ABCD'),
             {'h1': ['A'], 'h2': ['B'], 'h3': ['C']}]
get_overall_misclassifications_7_expected = set('A')
def get_overall_misclassifications_7_testanswer(val, original_val = None) :
    return val == get_overall_misclassifications_7_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_overall_misclassifications_7_getargs,
          testanswer = get_overall_misclassifications_7_testanswer,
          expected_val = str(get_overall_misclassifications_7_expected) \
              +" (Hint: Make sure you're summing voting powers, not just "
              +'counting classifiers.)',
          name = 'get_overall_misclassifications')

# recitation problem from 2012 Q4; all points correctly classified
def get_overall_misclassifications_8_getargs() :  #TEST 26
    H = [('<6', 0.693), ('<2', 0.549), ('>4', 0.805)]
    classifier_to_misclassified = {'<6': ['C'], '<4': ['C', 'B', 'E'],
                                   '<2': ['B', 'E'], '>2': ['A', 'C', 'D'],
                                   '>4': ['A', 'D'], '>6': ['A', 'B', 'D', 'E']}
    return [H, list('ABCDE'), classifier_to_misclassified]
get_overall_misclassifications_8_expected = set()
def get_overall_misclassifications_8_testanswer(val, original_val = None) :
    return val == get_overall_misclassifications_8_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_overall_misclassifications_8_getargs,
          testanswer = get_overall_misclassifications_8_testanswer,
          expected_val = str(get_overall_misclassifications_8_expected),
          name = 'get_overall_misclassifications')

#same classifier used multiple times
def get_overall_misclassifications_9_getargs() :  #TEST 27
    H = [('good_h', 0.1), ('bad_h1', 0.14), ('good_h', 0.1), ('bad_h2', 0.14),
         ('good_h', 0.1), ('bad_h3', 0.04)]
    classifier_to_misclassified = {'good_h': ['A'], 'bad_h1': ['B', 'C'],
                                   'bad_h2': ['C', 'D'], 'bad_h3': ['B', 'D']}
    return [H, list('ABCD'), classifier_to_misclassified]
get_overall_misclassifications_9_expected = set()
def get_overall_misclassifications_9_testanswer(val, original_val = None) :
    return val == get_overall_misclassifications_9_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_overall_misclassifications_9_getargs,
          testanswer = get_overall_misclassifications_9_testanswer,
          expected_val = str(get_overall_misclassifications_9_expected),
          name = 'get_overall_misclassifications')


def is_good_enough_0_getargs() :  #TEST 28
    return [[("h1", 1)], ['A','B'], {'h1':['A','B'],'h2':['A']}, 1]
is_good_enough_0_expected = False
def is_good_enough_0_testanswer(val, original_val = None) :
    return val == is_good_enough_0_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_good_enough_0_getargs,
          testanswer = is_good_enough_0_testanswer,
          expected_val = str(is_good_enough_0_expected),
          name = 'is_good_enough')

#All classifiers included in H
#h with voting power of 0
#H misclassifies A = mistake_tolerance
def is_good_enough_1_getargs() :  #TEST 29
    return [[("h1", 1),("h2", 0)], ['A','B'], {'h1': ['A'], 'h2': ['B']}, 1]
is_good_enough_1_expected = True
def is_good_enough_1_testanswer(val, original_val = None) :
    return val == is_good_enough_1_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_good_enough_1_getargs,
          testanswer = is_good_enough_1_testanswer,
          expected_val = str(is_good_enough_1_expected) + \
              ' (Hint: What should happen when H misclassifies exactly' \
              + ' mistake_tolerance points?)',
          name = 'is_good_enough')

# Not all points misclassified by any classifier
# H misclassifies A & B > mistake tolerance
def is_good_enough_2_getargs() :  #TEST 30
    return [[("h1", .5),("h2", .3),("h3", .76)], ['A','B','C','D'],
             {'h1': ['A'], 'h2': ['A','B'], 'h3': ['B','C']}, 1]
is_good_enough_2_expected = False
def is_good_enough_2_testanswer(val, original_val = None) :
    return val == is_good_enough_2_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_good_enough_2_getargs,
          testanswer = is_good_enough_2_testanswer,
          expected_val = str(is_good_enough_2_expected),
          name = 'is_good_enough')

#No points misclassified by h3
#H misclassifies C = mistake_tolerance
def is_good_enough_3_getargs() :  #TEST 31
    return [[("h1", .5),("h2", -.3),("h3", .76)], ['A','B','C'],
             {'h1': ['A','C'], 'h2': ['A','B'], 'h3': []}, 1]
is_good_enough_3_expected = True
def is_good_enough_3_testanswer(val, original_val = None) :
    return val == is_good_enough_3_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_good_enough_3_getargs,
          testanswer = is_good_enough_3_testanswer,
          expected_val = str(is_good_enough_3_expected) + \
              ' (Hint: What should happen when H misclassifies exactly' \
              + ' mistake_tolerance points?)',
          name = 'is_good_enough')

#All negative voting powers
#H misclassifies A,B,D > mistake_tolerance
def is_good_enough_4_getargs() :  #TEST 32
    return [[("h1", -.5),("h2", -.3),("h3", -.45)], ['A','B','C','D'],
             {'h1': ['A','C'], 'h2': ['B','C'], 'h3': ['D']}, 2]
is_good_enough_4_expected = False
def is_good_enough_4_testanswer(val, original_val = None) :
    return val == is_good_enough_4_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_good_enough_4_getargs,
          testanswer = is_good_enough_4_testanswer,
          expected_val = str(is_good_enough_4_expected),
          name = 'is_good_enough')

#misclassified training point is not listed in misclassifications
def is_good_enough_5_getargs() :  #TEST 33
    return [[("h1", -0.549),("h2", 0.347)], list('ABCD'),
             dict(h1=list('ABC'), h2=list('AC'), h3=list('BC')), 0]
is_good_enough_5_expected = False
def is_good_enough_5_testanswer(val, original_val = None) :
    return val == is_good_enough_5_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_good_enough_5_getargs,
          testanswer = is_good_enough_5_testanswer,
          expected_val = str(is_good_enough_5_expected) \
              +' (Hint: What happens if a training point is misclassified by ' \
              +'H, but not misclassified by any weak classifier?)',
          name = 'is_good_enough')

#one point misclassified, vote is a tie
# (No, this particular situation would not happen in Adaboost.)
def is_good_enough_6_getargs() :  #TEST 34
    return [[("h1", 0.5), ("h2", 0.5)], ['A','B'],
             {'h1': ['A'], 'h2': []}, 0]
is_good_enough_6_expected = False
def is_good_enough_6_testanswer(val, original_val = None) :
    return val == is_good_enough_6_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_good_enough_6_getargs,
          testanswer = is_good_enough_6_testanswer,
          expected_val = str(is_good_enough_6_expected) \
              +' (Hint: This test checks what happens when the vote is a tie.)',
          name = 'is_good_enough')

#violates triangle sum property
def is_good_enough_7_getargs() :  #TEST 35
    return [[("h1", 0.5), ("h2", 0.2), ("h3", 0.2)], list('ABCD'),
             {'h1': ['A'], 'h2': ['B'], 'h3': ['C']}, 0]
is_good_enough_7_expected = False
def is_good_enough_7_testanswer(val, original_val = None) :
    return val == is_good_enough_7_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_good_enough_7_getargs,
          testanswer = is_good_enough_7_testanswer,
          expected_val = str(is_good_enough_7_expected) \
              +" (Hint: Make sure you're summing voting powers, not just "
              +'counting classifiers.)',
          name = 'is_good_enough')

# recitation problem from 2012 Q4
def is_good_enough_8_getargs() :  #TEST 36
    H = [('<6', 0.693), ('<2', 0.549), ('>4', 0.805)]
    classifier_to_misclassified = {'<6': ['C'], '<4': ['C', 'B', 'E'],
                                   '<2': ['B', 'E'], '>2': ['A', 'C', 'D'],
                                   '>4': ['A', 'D'], '>6': ['A', 'B', 'D', 'E']}
    return [H, list('ABCDE'), classifier_to_misclassified, 0]
is_good_enough_8_expected = True
def is_good_enough_8_testanswer(val, original_val = None) :
    return val == is_good_enough_8_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_good_enough_8_getargs,
          testanswer = is_good_enough_8_testanswer,
          expected_val = str(is_good_enough_8_expected),
          name = 'is_good_enough')

#same classifier used multiple times
def is_good_enough_9_getargs() :  #TEST 37
    H = [('good_h', 0.1), ('bad_h1', 0.14), ('good_h', 0.1), ('bad_h2', 0.14),
         ('good_h', 0.1), ('bad_h3', 0.04)]
    classifier_to_misclassified = {'good_h': ['A'], 'bad_h1': ['B', 'C'],
                                   'bad_h2': ['C', 'D'], 'bad_h3': ['B', 'D']}
    return [H, list('ABCD'), classifier_to_misclassified, 0]
is_good_enough_9_expected = True
def is_good_enough_9_testanswer(val, original_val = None) :
    return val == is_good_enough_9_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_good_enough_9_getargs,
          testanswer = is_good_enough_9_testanswer,
          expected_val = str(is_good_enough_9_expected),
          name = 'is_good_enough')


def update_weights_0_getargs() :  #TEST 38
    return [{'A':F(1,6), 'B':F(1,6), 'C':F(1,6), 'D':F(1,6), 'E':F(1,6), 'F': F(1,6)}, ['A', 'B'], F(2,6)]
update_weights_0_expected = {'A':F(1,4), 'B':F(1,4), 'C':F(1,8), 'D':F(1,8), 'E':F(1,8), 'F':F(1,8)}
def update_weights_0_testanswer(val, original_val = None) :
    return val == update_weights_0_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = update_weights_0_getargs,
          testanswer = update_weights_0_testanswer,
          expected_val = str(update_weights_0_expected),
          name = 'update_weights')

def update_weights_2_getargs() :  #TEST 39
    return [{'A':F(1,2), 'B':F(1,2)}, [], 0]
update_weights_2_expected = {'A':F(1,4), 'B':F(1,4)}
def update_weights_2_testanswer(val, original_val = None) :
    return val == update_weights_2_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = update_weights_2_getargs,
          testanswer = update_weights_2_testanswer,
          expected_val = str(update_weights_2_expected),
          name = 'update_weights')

def update_weights_3_getargs() :  #TEST 40
    return [{'A':F(1,2), 'B':F(1,2)}, ['A', 'B'], 1]
update_weights_3_expected = {'A':F(1,4), 'B':F(1,4)}
def update_weights_3_testanswer(val, original_val = None) :
    return val == update_weights_3_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = update_weights_3_getargs,
          testanswer = update_weights_3_testanswer,
          expected_val = str(update_weights_3_expected),
          name = 'update_weights')


#recitation problem, from 2012 Quiz 4
boost_2012_tr_pts = ["A","B","C","D","E"]
boost_2012_cl_to_miscl = {"<2":["B","E"], "<4":["C","B","E"], "<6":["C"],
                          ">2":["A","C","D"], ">4":["A","D"],
                          ">6":["A","B","D","E"]}

#1 round
def adaboost_0_getargs() :  #TEST 41
    return [boost_2012_tr_pts, boost_2012_cl_to_miscl, True, 0, 1]
adaboost_0_expected = [("<6",.5*ln(4))]
def adaboost_0_testanswer(val, original_val = None) :
    return classifier_approx_equal(val, adaboost_0_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = adaboost_0_getargs,
          testanswer = adaboost_0_testanswer,
          expected_val = str(adaboost_0_expected),
          name = 'adaboost')

#2 rounds
def adaboost_1_getargs() :  #TEST 42
    return [boost_2012_tr_pts, boost_2012_cl_to_miscl, True, 0, 2]
adaboost_1_expected = [("<6",.5*ln(4)), ("<2", .5*ln(3))]
def adaboost_1_testanswer(val, original_val = None) :
    return classifier_approx_equal(val, adaboost_1_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = adaboost_1_getargs,
          testanswer = adaboost_1_testanswer,
          expected_val = str(adaboost_1_expected),
          name = 'adaboost')

#3 rounds
def adaboost_2_getargs() :  #TEST 43
    return [boost_2012_tr_pts, boost_2012_cl_to_miscl, True, 0, 3]
adaboost_2_expected = [("<6",.5*ln(4)), ("<2", .5*ln(3)), (">4",.5*ln(5))]
def adaboost_2_testanswer(val, original_val = None) :
    return classifier_approx_equal(val, adaboost_2_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = adaboost_2_getargs,
          testanswer = adaboost_2_testanswer,
          expected_val = str(adaboost_2_expected),
          name = 'adaboost')

#4 rounds (stops after 3)
def adaboost_3_getargs() :  #TEST 44
    return [boost_2012_tr_pts, boost_2012_cl_to_miscl, True, 0, 4]
adaboost_3_expected = [("<6",.5*ln(4)), ("<2", .5*ln(3)), (">4",.5*ln(5))]
def adaboost_3_testanswer(val, original_val = None) :
    return classifier_approx_equal(val, adaboost_3_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = adaboost_3_getargs,
          testanswer = adaboost_3_testanswer,
          expected_val = str(adaboost_3_expected),
          name = 'adaboost')

#INF rounds (stops after 3)
def adaboost_4_getargs() :  #TEST 45
    return [boost_2012_tr_pts, boost_2012_cl_to_miscl, True, 0, INF]
adaboost_4_expected = [("<6",.5*ln(4)), ("<2", .5*ln(3)), (">4",.5*ln(5))]
def adaboost_4_testanswer(val, original_val = None) :
    return classifier_approx_equal(val, adaboost_4_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = adaboost_4_getargs,
          testanswer = adaboost_4_testanswer,
          expected_val = str(adaboost_4_expected),
          name = 'adaboost')

#4 rounds (stops after 3); use error furthest from 1/2
def adaboost_5_getargs() :  #TEST 46
    return [boost_2012_tr_pts, boost_2012_cl_to_miscl, False, 0, 4]
adaboost_5_expected = [("<6",.5*ln(4)), ("<2", .5*ln(3)), ("<4",-.5*ln(5))]
def adaboost_5_testanswer(val, original_val = None) :
    return classifier_approx_equal(val, adaboost_5_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = adaboost_5_getargs,
          testanswer = adaboost_5_testanswer,
          expected_val = str(adaboost_5_expected),
          name = 'adaboost')

#allow 1 misclassification; stops after 1 round
def adaboost_6_getargs() :  #TEST 47
    return [boost_2012_tr_pts, boost_2012_cl_to_miscl, True, 1, 4]
adaboost_6_expected = [("<6",.5*ln(4))]
def adaboost_6_testanswer(val, original_val = None) :
    return classifier_approx_equal(val, adaboost_6_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = adaboost_6_getargs,
          testanswer = adaboost_6_testanswer,
          expected_val = str(adaboost_6_expected),
          name = 'adaboost')

#toy problem: exits after 1 round with all error rates = 1/2
def adaboost_7_getargs() :  #TEST 48
    return [list('XYZ'), {'cl_1':['Z'], 'cl_2':['X','Y']}, True, 0, 3]
adaboost_7_expected = [('cl_1', 0.5*ln(2))]
def adaboost_7_testanswer(val, original_val = None) :
    return classifier_approx_equal(val, adaboost_7_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = adaboost_7_getargs,
          testanswer = adaboost_7_testanswer,
          expected_val = str(adaboost_7_expected) \
              + ' (Hint: What should happen when the best error rate is 1/2?)',
          name = 'adaboost')

boost_toy1_tr_pts = list('ABCD')
boost_toy1_cl_to_miscl = {'h1':['A'], 'h2':list('BCD'), 'h3':list('ABC')}

#toy problem: exits after 1 round with smallest error rate = 1/2
def adaboost_8_getargs() :  #TEST 49
    return [boost_toy1_tr_pts, boost_toy1_cl_to_miscl, True, 0, 4]
adaboost_8_expected = [('h1', 0.5*ln(3))]
def adaboost_8_testanswer(val, original_val = None) :
    return classifier_approx_equal(val, adaboost_8_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = adaboost_8_getargs,
          testanswer = adaboost_8_testanswer,
          expected_val = str(adaboost_8_expected),
          name = 'adaboost')

#toy problem: has smallest error rate = 1/2 after 1 round, but continues
def adaboost_9_getargs() :  #TEST 50
    return [boost_toy1_tr_pts, boost_toy1_cl_to_miscl, False, 0, 2]
adaboost_9_expected = [('h1', 0.5*ln(3)), ('h3', -0.5*ln(5))]
def adaboost_9_testanswer(val, original_val = None) :
    return classifier_approx_equal(val, adaboost_9_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = adaboost_9_getargs,
          testanswer = adaboost_9_testanswer,
          expected_val = str(adaboost_9_expected),
          name = 'adaboost')

#picks same classifier multiple times
def adaboost_91_getargs() :  #TEST 51
    return [boost_toy1_tr_pts, boost_toy1_cl_to_miscl, False, 0, 4]
adaboost_91_expected = [('h1', 0.5*ln(3)), ('h3', -0.5*ln(5)),
                       ('h1', 0.5*ln(F(7,3))), ('h3', -0.5*ln(F(9,5)))]
def adaboost_91_testanswer(val, original_val = None) :
    return classifier_approx_equal(val, adaboost_91_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = adaboost_91_getargs,
          testanswer = adaboost_91_testanswer,
          expected_val = str(adaboost_91_expected),
          name = 'adaboost')

#tolerance > 1 but continues multiple rounds; exits with error_rate=0.5
def adaboost_92_getargs() :  #TEST 52
    return [list('ABCDEFG'),
            dict(h1=list('ABC'), h2=list('ABD'), h3=list('ABE')),
            True, 2, 5]
adaboost_92_expected = [('h1', 0.1438410362258895), ('h2', 0.08352704233158378),
                        ('h3', 0.041982690058667164)]
def adaboost_92_testanswer(val, original_val = None) :
    return classifier_approx_equal(val, adaboost_92_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = adaboost_92_getargs,
          testanswer = adaboost_92_testanswer,
          expected_val = str(adaboost_92_expected),
          name = 'adaboost')
