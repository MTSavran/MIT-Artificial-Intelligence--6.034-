# MIT 6.034 Lab 6: Neural Nets

from tester import make_test, get_tests
from nn_problems import *
from lab6 import sigmoid, ReLU
from random import random, randint
from math import cos, e

lab_number = 6 #for tester.py

def randnum(max_val=100):
    "Generates a random float 0 < n < max_val"
    return random() * randint(1, int(max_val))

def dict_contains(d, pairs):
    "Returns True if d contains all the specified pairs, otherwise False"
    items = d.items()
    return all([p in items for p in pairs])

def dict_approx_equal(dict1, dict2, epsilon=0.00000001):
    """Returns True if two dicts have the same keys and approximately equal
    values, otherwise False"""
    return (set(dict1.keys()) == set(dict2.keys())
            and all([approx_equal(dict1[key], dict2[key], epsilon)
                     for key in dict1.keys()]))


# WIRING A NEURAL NET

nn_half_getargs = 'nn_half'
def nn_half_testanswer(val, original_val = None):  #TEST 1
    if val == []:
        raise NotImplementedError
    return val == [1]
make_test(type = 'VALUE',
          getargs = nn_half_getargs,
          testanswer = nn_half_testanswer,
          expected_val = ('(list indicating correct minimum number of neurons '
                          + 'per layer)'),
          name = nn_half_getargs)

nn_angle_getargs = 'nn_angle'
def nn_angle_testanswer(val, original_val = None):  #TEST 2
    if val == []:
        raise NotImplementedError
    return val == [2, 1]
make_test(type = 'VALUE',
          getargs = nn_angle_getargs,
          testanswer = nn_angle_testanswer,
          expected_val = ('(list indicating correct minimum number of neurons '
                          + 'per layer)'),
          name = nn_angle_getargs)

nn_cross_getargs = 'nn_cross'
def nn_cross_testanswer(val, original_val = None):  #TEST 3
    if val == []:
        raise NotImplementedError
    return val == [2, 2, 1]
make_test(type = 'VALUE',
          getargs = nn_cross_getargs,
          testanswer = nn_cross_testanswer,
          expected_val = ('(list indicating correct minimum number of neurons '
                          + 'per layer)'),
          name = nn_cross_getargs)

nn_stripe_getargs = 'nn_stripe'
def nn_stripe_testanswer(val, original_val = None):  #TEST 4
    if val == []:
        raise NotImplementedError
    return val == [3, 1]
make_test(type = 'VALUE',
          getargs = nn_stripe_getargs,
          testanswer = nn_stripe_testanswer,
          expected_val = ('(list indicating correct minimum number of neurons '
                          + 'per layer)'),
          name = nn_stripe_getargs)

nn_hexagon_getargs = 'nn_hexagon'
def nn_hexagon_testanswer(val, original_val = None):  #TEST 5
    if val == []:
        raise NotImplementedError
    return val == [6, 1]
make_test(type = 'VALUE',
          getargs = nn_hexagon_getargs,
          testanswer = nn_hexagon_testanswer,
          expected_val = ('(list indicating correct minimum number of neurons '
                          + 'per layer)'),
          name = nn_hexagon_getargs)

nn_grid_getargs = 'nn_grid'
def nn_grid_testanswer(val, original_val = None):  #TEST 6
    if val == []:
        raise NotImplementedError
    return val == [4, 2, 1]
make_test(type = 'VALUE',
          getargs = nn_grid_getargs,
          testanswer = nn_grid_testanswer,
          expected_val = ('(list indicating correct minimum number of neurons '
                          + 'per layer) Hint: This one is tricky, but there '
                          + 'exists a neat solution with 7 neurons total.'),
          name = nn_grid_getargs)


## stairstep
#T=0, x>T -> 1
def stairstep_0_getargs() :  #TEST 7
    return [randnum()]
def stairstep_0_testanswer(val, original_val = None) :
    return val == 1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = stairstep_0_getargs,
          testanswer = stairstep_0_testanswer,
          expected_val = "1",
          name = 'stairstep')

#T=0, x<T -> 0
def stairstep_1_getargs() :  #TEST 8
    return [-randnum(), 0]
def stairstep_1_testanswer(val, original_val = None) :
    return val == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = stairstep_1_getargs,
          testanswer = stairstep_1_testanswer,
          expected_val = "0",
          name = 'stairstep')

#T>0, x=T -> 1
def stairstep_2_getargs() :  #TEST 9
    T = randnum()
    return [T, T]
def stairstep_2_testanswer(val, original_val = None) :
    return val == 1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = stairstep_2_getargs,
          testanswer = stairstep_2_testanswer,
          expected_val = "1",
          name = 'stairstep')


## sigmoid
#S=1, M=0, x>>M -> ~1
def sigmoid_0_getargs() :  #TEST 10
    return [10, 1, 0]
def sigmoid_0_testanswer(val, original_val = None) :
    return approx_equal(val, 0.9999, 0.0001)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = sigmoid_0_getargs,
          testanswer = sigmoid_0_testanswer,
          expected_val = "~0.9999",
          name = 'sigmoid')

#S=any, M>>0, x=M -> 0.5
def sigmoid_1_getargs() :  #TEST 11
    M = randnum()+10
    return [M, randnum(), M]
def sigmoid_1_testanswer(val, original_val = None) :
    return val == 0.5
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = sigmoid_1_getargs,
          testanswer = sigmoid_1_testanswer,
          expected_val = "0.5",
          name = 'sigmoid')

#S=1, M>>0, x=0 -> ~0
def sigmoid_2_getargs() :  #TEST 12
    return [0, 1, 15]
def sigmoid_2_testanswer(val, original_val = None) :
    return approx_equal(val, 0, 0.00001)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = sigmoid_2_getargs,
          testanswer = sigmoid_2_testanswer,
          expected_val = "~0",
          name = 'sigmoid')

#S=0.5, M=0.5, x=0 -> ~0.4378 (arbitrary parameters)
def sigmoid_3_getargs() :  #TEST 13
    return [0, 0.5, 0.5]
def sigmoid_3_testanswer(val, original_val = None) :
    return approx_equal(val, 0.4378, 0.0001)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = sigmoid_3_getargs,
          testanswer = sigmoid_3_testanswer,
          expected_val = "~0.4378",
          name = 'sigmoid')

## ReLU
# x > 0 -> x
def ReLU_0_getargs() :  #TEST 14
    return [12]
def ReLU_0_testanswer(val, original_val = None) :
    return val == 12
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = ReLU_0_getargs,
          testanswer = ReLU_0_testanswer,
          expected_val = "12",
          name = 'ReLU')

# x > 0 -> x
ReLU_1_arg = randnum()
def ReLU_1_getargs() :  #TEST 15
    return [ReLU_1_arg]
def ReLU_1_testanswer(val, original_val = None) :
    return val == ReLU_1_arg
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = ReLU_1_getargs,
          testanswer = ReLU_1_testanswer,
          expected_val = "{}".format(ReLU_1_arg),
          name = 'ReLU')

ReLU_2_arg = -1 * randnum()
def ReLU_2_getargs() :  #TEST 16
    return [ReLU_2_arg]
def ReLU_2_testanswer(val, original_val = None) :
    return val == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = ReLU_2_getargs,
          testanswer = ReLU_2_testanswer,
          expected_val = "0",
          name = 'ReLU')

## accuracy
#d=a -> 0
def accuracy_0_getargs() :  #TEST 17
    d = randnum()-50
    return [d, d]
def accuracy_0_testanswer(val, original_val = None) :
    return val == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = accuracy_0_getargs,
          testanswer = accuracy_0_testanswer,
          expected_val = "0",
          name = 'accuracy')

#d=1, a=0 -> -0.5
def accuracy_1_getargs() :  #TEST 18
    return [1, 0]
def accuracy_1_testanswer(val, original_val = None) :
    return val == -0.5
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = accuracy_1_getargs,
          testanswer = accuracy_1_testanswer,
          expected_val = "-0.5",
          name = 'accuracy')

#d=0, a=0.3 -> -0.045 (arbitrary parameters)
def accuracy_2_getargs() :  #TEST 19
    return [0, 0.3]
def accuracy_2_testanswer(val, original_val = None) :
    return val == -0.045
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = accuracy_2_getargs,
          testanswer = accuracy_2_testanswer,
          expected_val = "-0.045",
          name = 'accuracy')


## forward_prop
#basic fwd prop, 1 neuron, constant and variable inputs
def forward_prop_0_getargs() :  #TEST 20
    return [nn_basic.copy(), nn_basic_inputs.copy()]
def forward_prop_0_testanswer(val, original_val = None) :
    out, d = val
    return out == 1 and dict_contains(d, [('neuron', 1)])
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_0_getargs,
          testanswer = forward_prop_0_testanswer,
          expected_val = ("(1, (dict containing key-value pair: "
                          + "('neuron', 1))"),
          name = 'forward_prop')

#1 neuron, edge case: ==T -> 1
def forward_prop_1_getargs() :  #TEST 21
    return [nn_AND.copy(), {'x':1.5, 'y':0}]
def forward_prop_1_testanswer(val, original_val = None) :
    out, d = val
    return out == 1 and dict_contains(d, [('N1', 1)])
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_1_getargs,
          testanswer = forward_prop_1_testanswer,
          expected_val = ("(1, (dict containing key-value pair: "
                          + "('N1', 1)))"),
          name = 'forward_prop')

#5 neurons, XOR of two lines
def forward_prop_2_getargs() :  #TEST 22
    return [nn_XOR_lines.copy(), {'x':0.5, 'y':4}]
forward_prop_2_expected_outputs = [('line1', 0), ('line2', 0),
                                   ('X1', 0), ('X2', 1), ('AND', 0)]
def forward_prop_2_testanswer(val, original_val = None) :
    out, d = val
    return out == 0 and dict_contains(d, forward_prop_2_expected_outputs)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_2_getargs,
          testanswer = forward_prop_2_testanswer,
          expected_val = ("(0, (dict containing key-value pairs: "
                          + str(forward_prop_2_expected_outputs) + "))"),
          name = 'forward_prop')

#5 neurons, XOR of two lines; shuffle to check for dependence on list ordering
def forward_prop_3_getargs() :  #TEST 23
    return [nn_XOR_lines.copy().shuffle_lists(), {'x':4, 'y':0.5}]
forward_prop_3_expected_outputs = [('line1', 1), ('line2', 0),
                                   ('X1', 1), ('X2', 1), ('AND', 1)]
def forward_prop_3_testanswer(val, original_val = None) :
    out, d = val
    return out == 1 and dict_contains(d, forward_prop_3_expected_outputs)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_3_getargs,
          testanswer = forward_prop_3_testanswer,
          expected_val = ("(1, (dict containing key-value pairs: "
                          + str(forward_prop_3_expected_outputs) + "))"),
          name = 'forward_prop')

#3 neurons, River problem with stairstep function
def forward_prop_4_getargs() :  #TEST 24
    return [get_nn_River(1, -2, 5, 1, -2, 1), nn_River_inputs.copy()]
forward_prop_4_expected_outputs = [('A', 1), ('B', 0), ('C', 0)]
def forward_prop_4_testanswer(val, original_val = None) :
    out, d = val
    return out == 0 and dict_contains(d, forward_prop_4_expected_outputs)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_4_getargs,
          testanswer = forward_prop_4_testanswer,
          expected_val = ("(0, (dict containing key-value pairs: "
                          + str(forward_prop_4_expected_outputs) + "))"),
          name = 'forward_prop')

#3 neurons, River problem with stairstep function
def forward_prop_5_getargs() :  #TEST 25
    return [get_nn_River(1, -2, 5, 3, -2, 1), nn_River_inputs.copy()]
forward_prop_5_expected_outputs = [('A', 1), ('B', 0), ('C', 1)]
def forward_prop_5_testanswer(val, original_val = None) :
    out, d = val
    return out == 1 and dict_contains(d, forward_prop_5_expected_outputs)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_5_getargs,
          testanswer = forward_prop_5_testanswer,
          expected_val = ("(1, (dict containing key-value pairs: "
                          + str(forward_prop_5_expected_outputs) + "))"),
          name = 'forward_prop')

#1 neuron, sigmoid
def forward_prop_6_getargs() :  #TEST 26
    return [nn_AND.copy(), {'x':1, 'y':1}, sigmoid]
def forward_prop_6_testanswer(val, original_val = None) :
    out, d = val
    return approx_equal(out, 0.622459, 0.0001) and d['N1'] == out
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_6_getargs,
          testanswer = forward_prop_6_testanswer,
          expected_val = ("(~0.62246, (dict containing key-value pair: "
                          + "('N1', ~0.62246)))"),
          name = 'forward_prop')

#1 neuron, different threshold function
def forward_prop_7_getargs() :  #TEST 27
    return [nn_AND.copy(), {'x':20, 'y':23.5}, ReLU]
def forward_prop_7_testanswer(val, original_val = None) :
    out, d = val
    return out == 42 and d['N1'] == out
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_7_getargs,
          testanswer = forward_prop_7_testanswer,
          expected_val = ("(42, (dict containing key-value pair: "
                          + "('N1', 42)))"),
          name = 'forward_prop')

# checks that the user doesn't modify the neural net
input_net = nn_AND.copy()
not_modified = input_net.copy()
def forward_prop_8_getargs() :  #TEST 28
    return [input_net, {'x':20, 'y':23.5}, ReLU]
def forward_prop_8_testanswer(val, original_val = None) :
    out, d = val
    return out == 42 and d['N1'] == out and input_net == not_modified
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_8_getargs,
          testanswer = forward_prop_8_testanswer,
          expected_val = ("(42, (dict containing key-value pair: "
                          + "('N1', 42))) and also checks for an unmodified neural net"),
          name = 'forward_prop')

#### GRADIENT ASCENT
def funct1(x, y, z):
    return 5 * x + 3 * y ** 3 + cos(e - z ** 2)

def funct2(x, y, z):
    return -x + y + z

def gradient_ascent_step_0_getargs() :  #TEST 29
    return [funct1, [2, -5, 3], 0.1]
def gradient_ascent_step_0_testanswer(val, original_val = None) :
    return approx_equal(val[0], -341.4470010762434, 0.001) and all(approx_equal(a,b,0.01) for (a,b) in zip(val[1], [2.1, -4.9, 3]))
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = gradient_ascent_step_0_getargs,
          testanswer = gradient_ascent_step_0_testanswer,
          expected_val = "(-341.4470, [2.1, -4.9, 3])",
          name = 'gradient_ascent_step')

def gradient_ascent_step_1_getargs() :  #TEST 30
    return [funct2, [0, 0, 0], 0.001]
def gradient_ascent_step_1_testanswer(val, original_val = None) :
    return approx_equal(val[0], 0.003, 0.0001) and all(approx_equal(a,b,0.0001) for (a,b) in zip(val[1], [-0.001, 0.001, 0.001]))
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = gradient_ascent_step_1_getargs,
          testanswer = gradient_ascent_step_1_testanswer,
          expected_val = "(0.003, [-0.001, 0.001, 0.001])",
          name = 'gradient_ascent_step')

#### BACK PROP DEPENDENCIES

get_back_prop_dependencies_0_expected = set(["in1", Wire("in1", "neuron", 1), "neuron"])
def get_back_prop_dependencies_0_getargs() :  #TEST 31
    return [nn_basic.copy(), Wire("in1", "neuron", 1)]
def get_back_prop_dependencies_0_testanswer(val, original_val = None) :
    return val == get_back_prop_dependencies_0_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_back_prop_dependencies_0_getargs,
          testanswer = get_back_prop_dependencies_0_testanswer,
          expected_val = "{}".format(get_back_prop_dependencies_0_expected),
          name = 'get_back_prop_dependencies')

get_back_prop_dependencies_1_expected = set([-1, "N1", Wire(-1, "N1", 1.5)])
def get_back_prop_dependencies_1_getargs() :  #TEST 32
    return [nn_AND.copy(), Wire(-1, "N1", 1.5)]
def get_back_prop_dependencies_1_testanswer(val, original_val = None) :
    return val == get_back_prop_dependencies_1_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_back_prop_dependencies_1_getargs,
          testanswer = get_back_prop_dependencies_1_testanswer,
          expected_val = "set of inputs, Wires, and neurons necessary to update this weight",
          name = 'get_back_prop_dependencies')

get_back_prop_dependencies_2_expected = set(["x", "line2", "X1", "X2", "AND", Wire("x", "line2", 1), Wire("line2", "X1", 1), Wire("line2", "X2", -1), Wire("X1", "AND", 1), Wire("X2", "AND", 1)])
def get_back_prop_dependencies_2_getargs() :  #TEST 33
    return [nn_XOR_lines.copy(), Wire("x", "line2", 1)]
def get_back_prop_dependencies_2_testanswer(val, original_val = None) :
    return val == get_back_prop_dependencies_2_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_back_prop_dependencies_2_getargs,
          testanswer = get_back_prop_dependencies_2_testanswer,
          expected_val = "set of inputs, Wires, and neurons necessary to update this weight",
          name = 'get_back_prop_dependencies')

#### BACKWARD PROPAGATION

## calculate_deltas
#3 weights to update, final layer only
def calculate_deltas_0_getargs() :  #TEST 34
    return [nn_AND.copy(), 1, {'N1': 0.5}]
def calculate_deltas_0_testanswer(val, original_val = None) :
    return val == {'N1': 0.125}
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = calculate_deltas_0_getargs,
          testanswer = calculate_deltas_0_testanswer,
          expected_val = "{'N1': 0.125}",
          name = 'calculate_deltas')

#6 weights to update (River nn); shuffled
def calculate_deltas_2_getargs() :  #TEST 35
    return [get_nn_River(1, -2, 5, 3, -2, 1).shuffle_lists(),
            nn_River_desired, nn_River_fwd_prop1.copy()]
calculate_deltas_2_expected_deltas = {'A': 0.04441976755198489,
                                      'B': -0.01186039570737828,
                                      'C': -0.1129630506644473}
def calculate_deltas_2_testanswer(val, original_val = None) :
    return dict_approx_equal(val, calculate_deltas_2_expected_deltas)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = calculate_deltas_2_getargs,
          testanswer = calculate_deltas_2_testanswer,
          expected_val = str(calculate_deltas_2_expected_deltas),
          name = 'calculate_deltas')

# Here's where all the numbers above came from:
#    A = sigmoid(1) = 0.7310585786300049
#    B = sigmoid(-2) = 0.11920292202211757
#    C = sigmoid(A*-2+B+3) = 0.839846413654423
#    delta_C = C*(1-C)*-C = -0.1129630506644473
#    delta_A = A*(1-A)*-2*delta_C = 0.04441976755198489
#    delta_B = B*(1-B)*delta_C = -0.011860395707378284

#requires summation over outgoing neurons C_i
def calculate_deltas_3_getargs() :  #TEST 36
    return [nn_branching.shuffle_lists(), 1, nn_branching_fwd_prop1.copy()]
calculate_deltas_3_expected_deltas = {'N1': 0.033042492944110255, \
    'N2': 0.027644450191861528, 'N3': -0.06291182225171182, \
    'Nin': -0.025101018356825537, 'Nout': 0.1406041318860752}
def calculate_deltas_3_testanswer(val, original_val = None) :
    return dict_approx_equal(val, calculate_deltas_3_expected_deltas)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = calculate_deltas_3_getargs,
          testanswer = calculate_deltas_3_testanswer,
          expected_val = str(calculate_deltas_3_expected_deltas),
          name = 'calculate_deltas')

# Here's where the numbers above came from:
# sigmoid(0) = 0.5
# delta_Nout = out*(1-out)*(1-out)
# delta_N1 = sigmoid(0.5)*(1-sigmoid(0.5))*1*delta_Nout
# delta_N2 = sigmoid(2*0.5)*(1-sigmoid(2*0.5))*1*delta_Nout
# delta_N3 = sigmoid(3*0.5)*(1-sigmoid(3*0.5))*-3*delta_Nout
# delta_Nin = 0.5*(1-0.5)*(delta_N1+2*delta_N2+3*delta_N3)


## update_weights
#3 weights to update, final layer only
def update_weights_0_getargs() :  #TEST 37
    return [nn_AND.copy(), nn_AND_input.copy(), 1, {'N1': 0.5}]
def update_weights_0_testanswer(val, original_val = None) :
    return val == nn_AND_update_iter1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = update_weights_0_getargs,
          testanswer = update_weights_0_testanswer,
          expected_val = str(nn_AND_update_iter1),
          name = 'update_weights')

#3 weights to update, final layer only, different r
def update_weights_1_getargs() :  #TEST 38
    return [nn_AND.copy(), nn_AND_input.copy(), 1, {'N1': 0.5}, 10]
def update_weights_1_testanswer(val, original_val = None) :
    return val == nn_AND_update_iter1_r10
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = update_weights_1_getargs,
          testanswer = update_weights_1_testanswer,
          expected_val = str(nn_AND_update_iter1_r10),
          name = 'update_weights')

#6 weights to update (River nn); shuffled
def update_weights_2_getargs() :  #TEST 39
    return [get_nn_River(1, -2, 5, 3, -2, 1).shuffle_lists(),
            nn_River_inputs.copy(), nn_River_desired, nn_River_fwd_prop1.copy()]
update_weights_2_expected_net = get_nn_River(1.0444197675519848, \
    -2.0118603957073784, 5, 2.8870369493355525, -2.08258260725646, \
    0.9865344742802654)
def update_weights_2_testanswer(val, original_val = None) :
    return val == update_weights_2_expected_net
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = update_weights_2_getargs,
          testanswer = update_weights_2_testanswer,
          expected_val = str(update_weights_2_expected_net),
          name = 'update_weights')

# Here's where all the numbers above came from:
#    A = sigmoid(1) = 0.7310585786300049
#    B = sigmoid(-2) = 0.11920292202211757
#    C = sigmoid(A*-2+B+3) = 0.839846413654423
#    delta_C = C*(1-C)*-C = -0.1129630506644473
#    delta_A = A*(1-A)*-2*delta_C = 0.04441976755198489
#    delta_B = B*(1-B)*delta_C = -0.011860395707378284
#    w1 = 1+delta_A = 1.0444197675519848
#    w2 = -2+delta_B = -2.0118603957073784
#    w3 = 5 + 0 = 5
#    w4 = 3+delta_C = 2.8870369493355525
#    w5 = -2+A*delta_C = -2.08258260725646
#    w6 = 1+B*delta_C = 0.9865344742802654

#requires summation over outgoing neurons C_i
def update_weights_3_getargs() :  #TEST 40
    return [nn_branching.shuffle_lists(), nn_branching_input.copy(), 1, nn_branching_fwd_prop1.copy()]
def update_weights_3_testanswer(val, original_val = None) :
    return val.__eq__(nn_branching_update_iter1, 0.00000001)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = update_weights_3_getargs,
          testanswer = update_weights_3_testanswer,
          expected_val = str(nn_branching_update_iter1),
          name = 'update_weights')

# Here's where the numbers above came from:
# sigmoid(0) = 0.5
# delta_Nout = out*(1-out)*(1-out)
# delta_N1 = sigmoid(0.5)*(1-sigmoid(0.5))*1*delta_Nout
# delta_N2 = sigmoid(2*0.5)*(1-sigmoid(2*0.5))*1*delta_Nout
# delta_N3 = sigmoid(3*0.5)*(1-sigmoid(3*0.5))*-3*delta_Nout
# delta_Nin = 0.5*(1-0.5)*(delta_N1+2*delta_N2+3*delta_N3)
# w_in_to_Nin = 0 + 17*delta_Nin
# w_Nin_to_N1 = 1 + 0.5*delta_N1
# w_Nin_to_N2 = 2 + 0.5*delta_N2
# w_Nin_to_N3 = 3 + 0.5*delta_N3
# w_N1_to_Nout = 0 + sigmoid(0.5) * delta_Nout
# w_N2_to_Nout = 0 + sigmoid(2*0.5) * delta_Nout
# w_N3_to_Nout = 0 + sigmoid(3*0.5) * delta_Nout


## back_prop
#stops after 1 iter, better than default min_acc
def back_prop_0_getargs() :  #TEST 41
    return [nn_AND.copy(), {'x':3.5, 'y':-2}, 1, 10, -0.000001]
def back_prop_0_testanswer(val, original_val = None) :
    net, count = val
    return net == nn_AND_update_iter1_r10 and count == 1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = back_prop_0_getargs,
          testanswer = back_prop_0_testanswer,
          expected_val = "(" + str(nn_AND_update_iter1_r10) + ", 1)",
          name = 'back_prop')

#stops after 1 iter, not as good as default min_acc
def back_prop_1_getargs() :  #TEST 42
    return [nn_AND.copy(), {'x':3.5, 'y':-2}, 1, 1, -0.01]
def back_prop_1_testanswer(val, original_val = None) :
    net, count = val
    return net == nn_AND_update_iter1 and count == 1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = back_prop_1_getargs,
          testanswer = back_prop_1_testanswer,
          expected_val = "(" + str(nn_AND_update_iter1) + ", 1)",
          name = 'back_prop')

#already high enough accuracy; stops after 0 iter
def back_prop_2_getargs() :  #TEST 43
    return [nn_AND.copy(), {'x':-10, 'y':-10}, 0]
def back_prop_2_testanswer(val, original_val = None) :
    net, count = val
    return net == nn_AND and count == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = back_prop_2_getargs,
          testanswer = back_prop_2_testanswer,
          expected_val = "((original neural net, unchanged), 0)",
          name = 'back_prop')


#three iterations
def back_prop_4_getargs() :  #TEST 44
    return [nn_AND.copy(), {'x':3.5, 'y':-2}, 1, 1, -0.0035]
def back_prop_4_testanswer(val, original_val = None) :
    net, count = val
    return nn_AND_update_iter3.__eq__(net, 0.000000000001) and count == 3
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = back_prop_4_getargs,
          testanswer = back_prop_4_testanswer,
          expected_val = "(" + str(nn_AND_update_iter3) + ", 3)",
          name = 'back_prop')


#### Training a neural net

#ANSWER_1
ANSWER_1_getargs = 'ANSWER_1'  #TEST 45
def ANSWER_1_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return isinstance(val, int) and 11 <= val <= 60
make_test(type = 'VALUE',
          getargs = ANSWER_1_getargs,
          testanswer = ANSWER_1_testanswer,
          expected_val = "an int in the correct range",
          name = ANSWER_1_getargs)

#ANSWER_2
ANSWER_2_getargs = 'ANSWER_2'  #TEST 46
def ANSWER_2_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return isinstance(val, int) and 11 <= val <= 60
make_test(type = 'VALUE',
          getargs = ANSWER_2_getargs,
          testanswer = ANSWER_2_testanswer,
          expected_val = "an int in the correct range",
          name = ANSWER_2_getargs)

#ANSWER_3
ANSWER_3_getargs = 'ANSWER_3'  #TEST 47
def ANSWER_3_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return isinstance(val, int) and 2 <= val <= 10
make_test(type = 'VALUE',
          getargs = ANSWER_3_getargs,
          testanswer = ANSWER_3_testanswer,
          expected_val = "an int in the correct range",
          name = ANSWER_3_getargs)

#ANSWER_4
ANSWER_4_getargs = 'ANSWER_4'  #TEST 48
def ANSWER_4_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return isinstance(val, int) and 60 <= val <= 350
make_test(type = 'VALUE',
          getargs = ANSWER_4_getargs,
          testanswer = ANSWER_4_testanswer,
          expected_val = "an int in the correct range",
          name = ANSWER_4_getargs)

#ANSWER_5
ANSWER_5_getargs = 'ANSWER_5'  #TEST 49
def ANSWER_5_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return isinstance(val, int) and 10 <= val <= 70
make_test(type = 'VALUE',
          getargs = ANSWER_5_getargs,
          testanswer = ANSWER_5_testanswer,
          expected_val = "an int in the correct range",
          name = ANSWER_5_getargs)

#ANSWER_6
ANSWER_6_getargs = 'ANSWER_6'  #TEST 50
def ANSWER_6_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 1
make_test(type = 'VALUE',
          getargs = ANSWER_6_getargs,
          testanswer = ANSWER_6_testanswer,
          expected_val = "an int representing the resolution",
          name = ANSWER_6_getargs)

#ANSWER_7
ANSWER_7_getargs = 'ANSWER_7'  #TEST 51
def ANSWER_7_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return isinstance(val, str) and val.lower() == 'checkerboard'
make_test(type = 'VALUE',
          getargs = ANSWER_7_getargs,
          testanswer = ANSWER_7_testanswer,
          expected_val = "the name of a dataset, as a string",
          name = ANSWER_7_getargs)

#ANSWER_8
ANSWER_8_getargs = 'ANSWER_8'  #TEST 52
def ANSWER_8_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    try:
        return set([s.lower() for s in val]) == set(['small', 'medium', 'large'])
    except Exception:
        return False
make_test(type = 'VALUE',
          getargs = ANSWER_8_getargs,
          testanswer = ANSWER_8_testanswer,
          expected_val = "a list containing one or more of the strings 'small', 'medium', 'large'",
          name = ANSWER_8_getargs)

#ANSWER_9
ANSWER_9_getargs = 'ANSWER_9'  #TEST 53
def ANSWER_9_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val in list('Bb')
make_test(type = 'VALUE',
          getargs = ANSWER_9_getargs,
          testanswer = ANSWER_9_testanswer,
          expected_val = "a string ('A', 'B', 'C', or 'D')",
          name = ANSWER_9_getargs)

#ANSWER_10
ANSWER_10_getargs = 'ANSWER_10'  #TEST 54
def ANSWER_10_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val in list('Dd')
make_test(type = 'VALUE',
          getargs = ANSWER_10_getargs,
          testanswer = ANSWER_10_testanswer,
          expected_val = "a string ('A', 'B', 'C', 'D', or 'E')",
          name = ANSWER_10_getargs)

#ANSWER_11
ANSWER_11_getargs = 'ANSWER_11'  #TEST 55
def ANSWER_11_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    try:
        return set([s.upper() for s in val]) == set('AC')
    except Exception:
        return False
make_test(type = 'VALUE',
          getargs = ANSWER_11_getargs,
          testanswer = ANSWER_11_testanswer,
          expected_val = "a list of one or more strings, selected from " + str(list('ABCD')),
          name = ANSWER_11_getargs)

#ANSWER_12
ANSWER_12_getargs = 'ANSWER_12'  #TEST 56
def ANSWER_12_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    try:
        return set([s.upper() for s in val]) == set('AE')
    except Exception:
        return False
make_test(type = 'VALUE',
          getargs = ANSWER_12_getargs,
          testanswer = ANSWER_12_testanswer,
          expected_val = "a list of one or more strings, selected from " + str(list('ABCDE')),
          name = ANSWER_12_getargs)
