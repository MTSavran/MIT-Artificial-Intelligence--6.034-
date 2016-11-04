# MIT 6.034 Lab 6: Neural Nets

from neural_net_api import *

# Recitation example
nn_basic = NeuralNet(['in1', 2, 'in3', -1], ['neuron']) \
    .join('in1', 'neuron', 1).join(2, 'neuron', 2).join('in3', 'neuron', -1) \
    .join(-1, 'neuron', 2) \
    .join('neuron', NeuralNet.OUT)
nn_basic_inputs = {'in1':5, 'in3':-1}

# boolean AND function
nn_AND = NeuralNet(['x', 'y', -1], ['N1']) \
    .join('x', 'N1').join('y', 'N1').join(-1, 'N1', 1.5) \
    .join('N1', NeuralNet.OUT)

nn_AND_input = {'x':3.5, 'y':-2}

# Results of taining nn_AND with inputs x=3.5, y=-2 and desired_output=1
nn_AND_update_iter1 = NeuralNet(['x', 'y', -1], ['N1']) \
    .join('x', 'N1', 1.4375).join('y', 'N1', 0.75).join(-1, 'N1', 1.375) \
    .join('N1', NeuralNet.OUT)

nn_AND_update_iter2 = NeuralNet(['x', 'y', -1], ['N1']) \
    .join('x', 'N1', 1.4712646765161501).join('y', 'N1', 0.7307058991336285) \
    .join(-1, 'N1', 1.3653529495668142) \
    .join('N1', NeuralNet.OUT)

nn_AND_update_iter3 = NeuralNet(['x', 'y', -1], ['N1']) \
    .join('x', 'N1', 1.4966631783746651).join('y', 'N1', 0.7161924695001913) \
    .join(-1, 'N1', 1.3580962347500956) \
    .join('N1', NeuralNet.OUT)

# Higher rate constant, r=10
nn_AND_update_iter1_r10 = NeuralNet(['x', 'y', -1], ['N1']) \
    .join('x', 'N1', 5.375).join('y', 'N1', -1.5).join(-1, 'N1', 0.25) \
    .join('N1', NeuralNet.OUT)

# This neural net takes the XOR of two line shadings.
#   line1: y >= -2x + 7  ->  2x + 1y >= 7
#   line2: y <= x - 5    ->  1x + -1y >= 5
nn_XOR_lines = NeuralNet(['x', 'y', -1], ['line1', 'line2', 'X1', 'X2', 'AND'])\
    .join('x', 'line1', 2).join('y', 'line1', 1).join(-1, 'line1', 7) \
    .join('x', 'line2', 1).join('y', 'line2', -1).join(-1, 'line2', 5) \
    .join('line1', 'X1', 1).join('line2', 'X1', 1).join(-1, 'X1', 0.5) \
    .join('line1', 'X2', -1).join('line2', 'X2', -1).join(-1, 'X2', -1.5) \
    .join('X1', 'AND', 1).join('X2', 'AND', 1).join(-1, 'AND', 1.5) \
    .join('AND', NeuralNet.OUT)

# River problem from 2012 Quiz 3
def get_nn_River(w1, w2, w3, w4, w5, w6):
    nn_River = NeuralNet(['M', 'S', 'G'], ['A', 'B', 'C']) \
        .join('M', 'A', w1).join('M', 'B', w2).join('S', 'B', w3) \
        .join('G', 'C', w4).join('A', 'C', w5).join('B', 'C', w6) \
        .join('C', NeuralNet.OUT)
    return nn_River
nn_River_inputs = {'M':1, 'S':0, 'G':1}  # River's features
nn_River_fwd_prop1 = {'A': 0.7310585786300049, 'C': 0.839846413654423, 'B': 0.11920292202211757}
nn_River_desired = 0  # River is a human

nn_branching = NeuralNet(['in'], ['Nin', 'N1', 'N2', 'N3', 'Nout']) \
    .join('in', 'Nin', 0) \
    .join('Nin', 'N1', 1).join('Nin', 'N2', 2).join('Nin', 'N3', 3) \
    .join('N1', 'Nout', 1).join('N2', 'Nout', 1).join('N3', 'Nout', -3) \
    .join('Nout', NeuralNet.OUT)
nn_branching_input = {'in': 17}
# Results from starting with 'in':17 and with desired output = 1
nn_branching_fwd_prop1 = {'N1': 0.6224593312018546, 'N2': 0.7310585786300049, 'N3': 0.8175744761936437, 'Nin': 0.5, 'Nout': 0.24988878585697502}
nn_branching_update_iter1 = NeuralNet(['in'], ['Nin','N1','N2','N3','Nout']) \
    .join('in', 'Nin', -0.426717312066) \
    .join('Nin', 'N1', 1.01652124647) \
    .join('Nin', 'N2', 2.0138222251) \
    .join('Nin', 'N3', 2.96854408887) \
    .join('N1', 'Nout', 1.0875203539) \
    .join('N2', 'Nout', 1.10278985681) \
    .join('N3', 'Nout', -2.88504565052) \
    .join('Nout', NeuralNet.OUT)
