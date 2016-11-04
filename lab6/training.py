#!/usr/bin/env python2

# MIT 6.034 Lab 6: Neural Nets
# This file originally written by Joel Gustafson and Kenny Friedman

from sys import argv
from random import random, shuffle
from matplotlib import pyplot
import numpy
from lab6 import *



def multi_accuracy(desired_outputs, actual_outputs):
    pairs = []
    actual_outputs.sort()
    for d_o in sorted(desired_outputs):
        a_o = actual_outputs.pop(0)
        while a_o[0] != d_o[0]:
            a_o = actual_outputs.pop(0)
        pairs.append((d_o, a_o))
    total = sum(accuracy(a[1], b[1]) for a, b in pairs)
    return float(total) / len(pairs)

# Multi-point forward propagation
def multi_forward_prop(net, threshold_fn=sigmoid, resolution=1):
    outputs = []
    data = []
    for i in xrange(resolution * 5):
        y = float(i) / resolution
        line = []
        for j in xrange(resolution * 5):
            x = float(j) / resolution
            result = forward_prop(net, {'x': x, 'y': y}, threshold_fn)[0]
            if i % resolution == 0 and j % resolution == 0:
                outputs.append(((x, y), result))
            line.append(result)
        data.append(line)
    data = numpy.array(data)

    pyplot.pcolor(data)
    pyplot.draw()

    return (sorted(outputs), data)

# Backward propagation
def multi_update_weights(net, desired_outputs, r=1, width=5, height=5):
    shuffle(desired_outputs)
    for desired_output in desired_outputs:
        input_values = {'x': desired_output[0][0], 'y': desired_output[0][1]}
        neuron_outputs = forward_prop(net, input_values, sigmoid)[1]
        net = update_weights(net, input_values, desired_output[1], neuron_outputs, r)
    return net

def multi_back_prop(net, desired_outputs, r=1, minimum_accuracy=-0.001, resolution=1):
    actual_outputs = multi_forward_prop(net, sigmoid, resolution)[0]
    c = 0
    current_accuracy = multi_accuracy(desired_outputs, actual_outputs)
    print c, current_accuracy
    while current_accuracy < minimum_accuracy:
        net = multi_update_weights(net, desired_outputs, r)
        actual_outputs = multi_forward_prop(net, sigmoid, resolution)[0]
        c += 1
        current_accuracy = multi_accuracy(desired_outputs, actual_outputs)
        print c, current_accuracy
    return net

# Define neural nets
def get_small_nn(w=None):
    if w is None:
        w = [10 * (0.5 - random()) for n in xrange(9)]
    return NeuralNet(['x', 'y', -1], ['A','B','C']) \
        .join('x', 'A', w[0]).join('x', 'B', w[1]) \
        .join('y', 'A', w[2]).join('y', 'B', w[3]) \
        .join('A', 'C', w[4]).join('B', 'C', w[5]) \
        .join(-1, 'A', w[6]).join(-1, 'B', w[7]).join(-1, 'C', w[8]) \
        .join('C', NeuralNet.OUT)

def get_medium_nn(w=None):
    if w is None:
        w = [10 * (0.5 - random()) for n in xrange(20)]
    return NeuralNet(['x', 'y', -1], list('ABCDEF')) \
        .join('x', 'A', w[0]).join('x', 'B', w[1]).join('y', 'A', w[2]) \
        .join('y', 'B', w[3]).join('y', 'C', w[4]).join('x', 'C', w[5]) \
        .join(-1, 'A', w[6]).join(-1, 'B', w[7]).join(-1, 'C', w[8]) \
        .join('A', 'E', w[9]).join('A', 'D', w[10]).join('B', 'D', w[11]) \
        .join(-1, 'D', w[12]).join(-1, 'E', w[13]).join(-1, 'F', w[14]) \
        .join('B', 'E', w[15]).join('C', 'E', w[16]).join('C', 'D', w[17]) \
        .join('D', 'F', w[18]).join('E', 'F', w[19]).join('F', NeuralNet.OUT)

def get_large_nn():
    w = lambda: 10 * (0.5 - random())
    nn = NeuralNet(['x', 'y', -1], list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    #first layer: A-J (10 neurons)
    for n1 in 'ABCDEFGHIJ':
        nn.join('x', n1, w()).join('y', n1, w())

        #second layer: K-T (10 neurons)
        for n2 in 'KLMNOPQRST':
            nn.join(n1, n2, w())

    #third layer: U-Y (5 neurons)
    for n3 in 'UVWXY':
        for n2 in 'KLMNOPQRST':
            nn.join(n2, n3, w())

        #final layer: Z (1 neuron)
        nn.join(n3, 'Z', w())

    #define Z as output neuron
    nn.join('Z', NeuralNet.OUT)

    return nn

nets = {'small': get_small_nn, 'medium': get_medium_nn, 'large': get_large_nn}


# Define data sets

# horizontal
# - - - - -
# - - - - -
# - - - - -
# + + + + +
# + + + + +
horizontal = sorted([((0,0),1),((0,1),1),((0,2),1),((0,3),0),((0,4),0),((1,0),1),
                    ((1,1),1),((1,2),1),((1,3),0),((1,4),0),((2,0),1),((2,1),1),
                    ((2,2),1),((2,3),0),((2,4),0),((3,0),1),((3,1),1),((3,2),1),
                    ((3,3),0),((3,4),0),((4,0),1),((4,1),1),((4,2),1),((4,3),0),((4,4),0)])

# diagonal
# + + + + -
# + + + - -
# + + - - -
# + - - - -
# - - - - -
diagonal = sorted([((0,0),0),((0,1),1),((0,2),1),((0,3),1),((0,4),1),((1,0),0),
                    ((1,1),0),((1,2),1),((1,3),1),((1,4),1),((2,0),0),((2,1),0),
                    ((2,2),0),((2,3),1),((2,4),1),((3,0),0),((3,1),0),((3,2),0),
                    ((3,3),0),((3,4),1),((4,0),0),((4,1),0),((4,2),0),((4,3),0),((4,4),0)])

# stripe
# - - - - +
# - - - + -
# - - + - -
# - + - - -
# + - - - -
stripe = sorted([((0,0),1),((0,1),0),((0,2),0),((0,3),0),((0,4),0),((1,0),0),
                    ((1,1),1),((1,2),0),((1,3),0),((1,4),0),((2,0),0),((2,1),0),
                    ((2,2),1),((2,3),0),((2,4),0),((3,0),0),((3,1),0),((3,2),0),
                    ((3,3),1),((3,4),0),((4,0),0),((4,1),0),((4,2),0),((4,3),0),((4,4),1)])

# checkerboard
# - -   + +
# - -   + +
#
# + +   - -
# + +   - -
checkerboard = sorted([((0,0),1),((1,0),1),((0,1),1),((1,1),1),((3,3),1),((4,3),1),
                        ((3,4),1),((4,4),1),((0,3),0),((1,3),0),((0,4),0),
                        ((1,4),0),((3,0),0),((3,1),0),((4,0),0),((4,1),0)])

# letterL
# + -
# + -
# + -
# + - - - -
# - + + + +
letterL = sorted([((0,0),0),((1,0),1),((2,0),1),((3,0),1),((4,0),1),((0,1),1),
                    ((1,1),0),((2,1),0),((3,1),0),((4,1),0),((0,2),1),((0,3),1),
                    ((0,4),1),((1,2),0),((1,3),0),((1,4),0)])

# moat
# - - - - -
# -       -
# -   +   -
# -       -
# - - - - -
moat = sorted([((0,0),0),((0,1),0),((0,2),0),((0,3),0),((0,4),0),((1,4),0),
                ((2,4),0),((3,4),0),((4,4),0),((4,3),0),((4,2),0),((4,1),0),
                ((4,0),0),((3,0),0),((2,0),0),((1,0),0),((2,2),1)])

training_data = {'horizontal': horizontal, 'diagonal': diagonal, 'stripe': stripe,
                 'checkerboard': checkerboard, 'letterL': letterL, 'moat': moat}


# Main function for training and heatmap
def start_training(data=None, net=None, resolution=None):
    if data == None:
        print 'defaulting to diagonal training dataset'
        train = diagonal
    elif data in training_data:
        train = training_data[data]
    else:
        print 'training dataset not found, defaulting to diagonal'
        train = diagonal

    if net == None:
        print 'defaulting to medium net'
        net_fn = get_medium_nn
    elif net in nets:
        net_fn = nets[net]
    else:
        print 'net not found, defaulting to medium net'
        net_fn = get_medium_nn

    if resolution == None:
        print 'defaulting to resolution of 1'
        resolution = 1
    else:
        try:
            resolution = int(resolution)
            assert resolution > 0
        except Exception:
            print 'invalid resolution, defaulting to 1'
            resolution = 1

    pyplot.ion()
    pyplot.show()

    nn = net_fn()
    print '\nInitial neural net:\n', nn

    print '\nIter, Accuracy:'

    try:
        nn = multi_back_prop(nn, train, 1.0, -0.01, resolution)
    except Exception, e:
        if str(type(e)) == "<class '_tkinter.TclError'>": #this is a hack
            print '\nException caught: _tkinter.TclError:', e, '\n'
            Athena_ssh_error_message = ("If you are running this on Athena "
                + "over ssh, try sshing again using the -X flag, which allows "
                + "Athena to display GUI windows on your local desktop.  "
                + "If you want to see the original stack trace instead of this "
                + "error, find the line in training.py that raises this "
                + "RuntimeError and replace it with 'raise e'.")
            raise RuntimeError(Athena_ssh_error_message)
        else:
            raise e

    pyplot.ioff()

    print '\nTrained neural net:\n', nn
    data = multi_forward_prop(nn, sigmoid, resolution)[1]

    pyplot.clf()
    pc = pyplot.pcolor(data)
    pyplot.colorbar(pc)
    pyplot.show()


if __name__ == "__main__":
    train = "diagonal"
    net = "large"
    resolution = 1

    if '-data' in argv:
        train = argv[argv.index('-data') + 1]
    else:
        print 'defaulting to diagonal training dataset'

    if '-net' in argv:
        net = argv[argv.index('-net') + 1]
    else:
        print 'defaulting to medium net'

    if '-resolution' in argv:
        resolution = argv[argv.index('-resolution') + 1]
    else:
        print 'defaulting to resolution of 1'

    start_training("checkerboard", "large", 1)
