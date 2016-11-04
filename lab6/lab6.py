# MIT 6.034 Lab 6: Neural Nets
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), Jake Barnwell (jb16), and 6.034 staff

from nn_problems import *
from math import e
INF = float('inf')
import numpy as np
import matplotlib

#### NEURAL NETS ###############################################################

# Wiring a neural net

nn_half = [1]

nn_angle = [2,1]

nn_cross = [2,2,1]

nn_stripe = [3,1]

nn_hexagon = [6,1]

nn_grid = [4,2,1]

# Threshold functions
def stairstep(x, threshold=0):
    "Computes stairstep(x) using the given threshold (T)"
    if x >= threshold:
        return 1 
    return 0 

def sigmoid(x, steepness=1, midpoint=0):
    "Computes sigmoid(x) using the given steepness (S) and midpoint (M)"
    return 1/(1+e**(-steepness*(x-midpoint)))

def ReLU(x):
    "Computes the threshold of an input using a rectified linear unit."
    if x<0:
        return 0
    return x

# Accuracy function
def accuracy(desired_output, actual_output):
    "Computes accuracy. If output is binary, accuracy ranges from -0.5 to 0."
    acc = -0.5*(desired_output-actual_output)**2
    return acc

# Forward propagation

def node_value(node, input_values, neuron_outputs):  # STAFF PROVIDED
    """Given a node, a dictionary mapping input names to their values, and a
    dictionary mapping neuron names to their outputs, returns the output value
    of the node."""
    if isinstance(node, basestring):
        return input_values[node] if node in input_values else neuron_outputs[node]
    return node  # constant input, such as -1

def forward_prop(net, input_values, threshold_fn=stairstep):
    """Given a neural net and dictionary of input values, performs forward
    propagation with the given threshold function to compute binary output.
    This function should not modify the input net.  Returns a tuple containing:
    (1) the final output of the neural net
    (2) a dictionary mapping neurons to their immediate outputs"""
    lis = net.topological_sort()
    neuron_outputs = {}
    for neuron in lis:
        weightedsum = 0
        for i in net.get_incoming_neighbors(neuron):
            wires = net.get_wires(i,neuron)
            weightedsum += node_value(i, input_values, neuron_outputs)*wires[0].get_weight()
        out = threshold_fn(weightedsum)
        neuron_outputs[neuron] = out
    return (neuron_outputs[neuron],neuron_outputs)


# Backward propagation warm-up
def gradient_ascent_step(func, inputs, step_size):
    """Given an unknown function of three variables and a list of three values
    representing the current inputs into the function, increments each variable
    by +/- step_size or 0, with the goal of maximizing the function output.
    After trying all possible variable assignments, returns a tuple containing:
    (1) the maximum function output found, and
    (2) the list of inputs that yielded the highest function output."""
    maxval = float('-inf')
    A = inputs[0]
    B = inputs[1]
    C = inputs[2]
    if func(A,B,C) > maxval:
        best = (A,B,C)
        maxval = func(A,B,C)
    for i in range(1,8):
        [x,y,z] = inputs
        if i == 1:
            if func(x,y,z+step_size)>maxval:
                best = (x,y,z+step_size)
                maxval=func(x,y,z+step_size)
            if func(x,y,z-step_size)>maxval:
                maxval=func(x,y,z-step_size)
        if i == 2:
            if func(x,y+step_size,z)>maxval:
                best = (x,y+step_size,z)
                maxval=func(x,y+step_size,z)
            if func(x,y-step_size,z)>maxval:
                best = (x,y-step_size,z)
                maxval=func(x,y-step_size,z)
        if i == 3: 
            if func(x,y+step_size,z+step_size)>maxval:
                best = (x,y+step_size,z+step_size)
                maxval=func(x,y+step_size,z+step_size)

            if func(x,y+step_size,z-step_size)>maxval:
                best = (x,y+step_size,z-step_size)
                maxval=func(x,y+step_size,z-step_size)

            if func(x,y-step_size,z+step_size)>maxval:
                best = (x,y-step_size,z+step_size)
                maxval=func(x,y-step_size,z+step_size)

            if func(x,y-step_size,z-step_size)>maxval:
                best = (x,y-step_size,z-step_size)
                maxval=func(x,y-step_size,z-step_size)
        if i == 4:
            if func(x+step_size,y,z)>maxval:
                best = (x+step_size,y,z)
                maxval=func(x+step_size,y,z)
            if func(x-step_size,y,z)>maxval:
                best = (x-step_size,y,z)
                maxval=func(x-step_size,y,z)
        if i == 5:
            if func(x+step_size,y,z+step_size)>maxval:
                best = (x+step_size,y,z+step_size)
                maxval=func(x+step_size,y,z+step_size)

            if func(x+step_size,y,z-step_size)>maxval:
                best = (x+step_size,y,z-step_size)
                maxval=func(x+step_size,y,z-step_size)

            if func(x-step_size,y,z+step_size)>maxval:
                best = (x-step_size,y,z+step_size)
                maxval=func(x-step_size,y,z+step_size)

            if func(x-step_size,y,z-step_size)>maxval:
                best = (x-step_size,y,z-step_size)
                maxval=func(x-step_size,y,z-step_size)
        if i == 6:
            if func(x+step_size,y+step_size,z)>maxval:
                best = (x+step_size,y+step_size,z)
                maxval=func(x+step_size,y+step_size,z)

            if func(x+step_size,y-step_size,z)>maxval:
                best = (x+step_size,y-step_size,z)
                maxval=func(x+step_size,y-step_size,z)

            if func(x-step_size,y+step_size,z)>maxval:
                best = (x-step_size,y+step_size,z)
                maxval=func(x-step_size,y+step_size,z)

            if func(x-step_size,y-step_size,z)>maxval:
                best = (x-step_size,y-step_size,z)
                maxval=func(x-step_size,y-step_size,z)
        if i == 7:
            if func(x+step_size,y+step_size,z+step_size) > maxval:
                best = (x+step_size,y+step_size,z+step_size)
                maxval = func(x+step_size,y+step_size,z+step_size)

            if func(x+step_size,y+step_size,z-step_size) > maxval:
                best = (x+step_size,y+step_size,z-step_size)
                maxval = func(x+step_size,y+step_size,z-step_size)

            if func(x+step_size,y-step_size,z-step_size) > maxval:
                best = (x+step_size,y-step_size,z-step_size)
                maxval = func(x+step_size,y-step_size,z-step_size)

            if func(x+step_size,y-step_size,z+step_size) > maxval:
                best = (x+step_size,y-step_size,z+step_size)
                maxval = func(x+step_size,y-step_size,z+step_size)

            if func(x+step_size,y+step_size,z+step_size) > maxval:
                best = (x+step_size,y+step_size,z+step_size)
                maxval = func(x+step_size,y+step_size,z+step_size)

            if func(x-step_size,y+step_size,z+step_size) > maxval:
                best = (x-step_size,y+step_size,z+step_size)
                maxval = func(x-step_size,y+step_size,z+step_size)

            if func(x-step_size,y-step_size,z+step_size) > maxval:
                best = (x-step_size,y-step_size,z+step_size)
                maxval = func(x-step_size,y-step_size,z+step_size)

            if func(x-step_size,y+step_size,z-step_size) > maxval:
                best = (x-step_size,y+step_size,z-step_size)
                maxval = func(x-step_size,y+step_size,z-step_size)

            if func(x-step_size,y-step_size,z-step_size) > maxval:
                best = (x-step_size,y-step_size,z-step_size)
                maxval = func(x-step_size,y-step_size,z-step_size)

    return (maxval,list(best))

def get_back_prop_dependencies(net, wire):
    """Given a wire in a neural network, returns a set of inputs, neurons, and
    Wires whose outputs/values are required to update this wire's weight."""
    queue = [wire.endNode]
    inputset = set()
    inputset.add(wire)
    inputset.add(wire.startNode)
    while queue:
        node = queue.pop(0)
        inputset.add(node)
        if net.is_output_neuron(node):
            return inputset
        for i in net.get_outgoing_neighbors(node):
            wires = net.get_wires(node,i)[0]
            inputset.add(wires)
            queue.append(i)
    return inputset

# Backward propagation
def calculate_deltas(net, desired_output, neuron_outputs):
    """Given a neural net and a dictionary of neuron outputs from forward-
    propagation, computes the update coefficient (delta_B) for each
    neuron in the net. Uses the sigmoid function to compute neuron output.
    Returns a dictionary mapping neuron names to update coefficient (the
    delta_B values). """
    valuemap = {}
    #current = net.get_output_neuron()
    graph = net.topological_sort()
    graph.reverse()
    for neuron in graph:
        if net.is_output_neuron(neuron):
            deltab = neuron_outputs[neuron]*(1-neuron_outputs[neuron])*(desired_output-neuron_outputs[neuron])
            valuemap[neuron] = deltab
        else:
            w = 0 
            for node in net.get_outgoing_neighbors(neuron):
                wire = net.get_wires(neuron,node)[0]
                weight = wire.get_weight()
                deltanode = valuemap[node]
                w += weight*deltanode
            out = neuron_outputs[neuron]*(1-neuron_outputs[neuron])*w
            valuemap[neuron] = out
    return valuemap

def update_weights(net, input_values, desired_output, neuron_outputs, r=1):
    """Performs a single step of back-propagation.  Computes delta_B values and
    weight updates for entire neural net, then updates all weights.  Uses the
    sigmoid function to compute neuron output.  Returns the modified neural net,
    with the updated weights."""
    valuemap = calculate_deltas(net, desired_output, neuron_outputs)
    allwires = net.get_wires()
    for wire in allwires:
        deltab = valuemap[wire.endNode] 
        if wire.startNode in neuron_outputs:
            outA = neuron_outputs[wire.startNode]
        elif wire.startNode in input_values:
            outA = input_values[wire.startNode]
        else:
            outA = wire.startNode
        deltaw = r*outA*deltab
        newweight = wire.get_weight() + deltaw
        wire.set_weight(newweight)
    return net 

def back_prop(net, input_values, desired_output, r=1, minimum_accuracy=-0.001):
    """Updates weights until accuracy surpasses minimum_accuracy.  Uses the
    sigmoid function to compute neuron output.  Returns a tuple containing:
    (1) the modified neural net, with trained weights
    (2) the number of iterations (that is, the number of weight updates)"""
    tup = forward_prop(net, input_values, sigmoid)
    acc = accuracy(desired_output,tup[0])
    count = 0
    while acc < minimum_accuracy:
        tup = forward_prop(net, input_values, sigmoid)
        acc = accuracy(desired_output, tup[0])
        neuron_outputs = tup[1]
        net = update_weights(net,input_values,desired_output, neuron_outputs, r=r)
        acc = accuracy(desired_output,forward_prop(net, input_values, sigmoid)[0])
        count += 1
    return (net,count)


# Training a neural net

ANSWER_1 = 20
ANSWER_2 = 17
ANSWER_3 = 8
ANSWER_4 = 193
ANSWER_5 = 19

ANSWER_6 = 1
ANSWER_7 = "checkerboard"
ANSWER_8 = ["small","medium","large"]
ANSWER_9 = "B"

ANSWER_10 = "D"
ANSWER_11 = ["A","C"]
ANSWER_12 = ["A","E"]


#### SURVEY ####################################################################

NAME = "Mehmet Tugrul Savran"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = "5"
WHAT_I_FOUND_INTERESTING = "EVERYTHING!!!!!!!!!"
WHAT_I_FOUND_BORING = "NOTHING!!!!!!!!"
SUGGESTIONS = "NOTHING!!!!!!!!"
