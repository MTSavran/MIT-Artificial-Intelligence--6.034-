# MIT 6.034 Lab 9: Boosting (Adaboost)
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), and 6.034 staff

from math import log as ln
from utils import *


#### BOOSTING (ADABOOST) #######################################################

def initialize_weights(training_points):
    """Assigns every training point a weight equal to 1/N, where N is the number
    of training points.  Returns a dictionary mapping points to weights."""
    N = len(training_points)
    return {point : make_fraction(1,N) for point in training_points}
    

def calculate_error_rates(point_to_weight, classifier_to_misclassified):
    """Given a dictionary mapping training points to their weights, and another
    dictionary mapping classifiers to the training points they misclassify,
    returns a dictionary mapping classifiers to their error rates."""
    result = {}
    for classifier in classifier_to_misclassified:
        summ = 0 
        for missclassifiedpoint in classifier_to_misclassified[classifier]:
            summ += point_to_weight[missclassifiedpoint]
        result[classifier] = summ
    return result

def pick_best_classifier(classifier_to_error_rate, use_smallest_error=True):
    """Given a dictionary mapping classifiers to their error rates, returns the
    best* classifier, or raises NoGoodClassifiersError if best* classifier has
    error rate 1/2.  best* means 'smallest error rate' if use_smallest_error
    is True, otherwise 'error rate furthest from 1/2'."""
    if use_smallest_error==True:

        best = list(classifier_to_error_rate)[0]
        bestval = make_fraction(classifier_to_error_rate[best])
        for classifier in classifier_to_error_rate:
            if make_fraction(classifier_to_error_rate[classifier]) <= bestval:
                print best
                if bestval == make_fraction(classifier_to_error_rate[classifier]):
                    
                    a = sorted([best,classifier])

                    best = a[0]
                    bestval = make_fraction(classifier_to_error_rate[best])
                else:
                    print 'aaaaaaa'
                    best = classifier
                    bestval = make_fraction(classifier_to_error_rate[classifier])
        if bestval == 0.5:
            raise NoGoodClassifiersError
        return best 

    else:

        best = list(classifier_to_error_rate)[0]
        bestval = make_fraction(classifier_to_error_rate[best])
        print classifier_to_error_rate
        for classifier in classifier_to_error_rate:
            if abs(make_fraction(1,2)-make_fraction(classifier_to_error_rate[classifier])) >= abs(make_fraction(bestval)-make_fraction(1,2)):  
                print "bestval is", make_fraction(bestval), "the other one is ", make_fraction(classifier_to_error_rate[classifier])

                if abs(make_fraction(1,2)-make_fraction(classifier_to_error_rate[classifier])) == abs(make_fraction(bestval)-make_fraction(1,2)):
                    
                    a = sorted([best,classifier])
                    best = a[0]
                    bestval = make_fraction(classifier_to_error_rate[best])
                else:
                    print 'aaaaaaflhjcbfd'
                    best = classifier
                    bestval = make_fraction(classifier_to_error_rate[classifier])
        
        if bestval == make_fraction(1,2):
            raise NoGoodClassifiersError
        else:
            return best

def calculate_voting_power(error_rate):
    """Given a classifier's error rate (a number), returns the voting power
    (aka alpha, or coefficient) for that classifier."""
    if error_rate == 1:
        return -INF
    if error_rate == 0:
        return INF
    return make_fraction(1,2)*ln(make_fraction(1-error_rate,error_rate))

def get_overall_misclassifications(H, training_points, classifier_to_misclassified):
    """Given an overall classifier H, a list of all training points, and a
    dictionary mapping classifiers to the training points they misclassify,
    returns a set containing the training points that H misclassifies.
    H is represented as a list of (classifier, voting_power) tuples."""
    # print H 
    # answer = set()
    # for classifier in classifier_to_misclassified:
    #     for element in classifier_to_misclassified[classifier]:
    #         answer.add(element)
    # return answer

    counter = 0
    answer = set()
    for p in training_points:
        summ = 0
        tie = False
        for (classifier, voting_power) in H:
            points = classifier_to_misclassified[classifier]
            if p in points:
                summ += (-voting_power)
            else:
                summ += (voting_power)

        index = 1
        for i in range(1, len(H)):
            if H[index-1][1] == H[index][1]:
                tie = True
                counter += 1
                index += 2 
                break

        if summ <= 0:
            counter += 1
            print p
            answer.add(p)

    return answer


def is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance=0):
    """Given an overall classifier H, a list of all training points, a
    dictionary mapping classifiers to the training points they misclassify, and
    a mistake tolerance (the maximum number of allowed misclassifications),
    returns False if H misclassifies more points than the tolerance allows,
    otherwise True.  H is represented as a list of (classifier, voting_power)
    tuples."""
    import numpy

    counter = 0
    for p in training_points:
        summer = 0
        tie = False
        for (classifier, voting_power) in H:
            points = classifier_to_misclassified[classifier]
            if p in points:
                summer += (-voting_power)
            else:
                summer += (voting_power)

        for i in range(1, len(H)):
            if H[i-1][1] == H[i][1]:
                tie = True
                counter += 1
                break

        if tie == True:
            continue

        if numpy.sign(summer) == -1:
            counter += 1

    if counter > mistake_tolerance:
        return False
    else:
        return True

def update_weights(point_to_weight, misclassified_points, error_rate):
    """Given a dictionary mapping training points to their old weights, a list
    of training points misclassified by the current weak classifier, and the
    error rate of the current weak classifier, returns a dictionary mapping
    training points to their new weights.  This function is allowed (but not
    required) to modify the input dictionary point_to_weight."""
    answer = {}
    for point, old_weight in point_to_weight.items():
        if point in misclassified_points:
            answer[point] = make_fraction(0.5*make_fraction(1,error_rate)*old_weight)
        else:
            answer[point] = make_fraction(0.5*make_fraction(1,(1-error_rate)) * old_weight)
    
    return answer

def adaboost(training_points, classifier_to_misclassified,
             use_smallest_error=True, mistake_tolerance=0, max_rounds=INF):
    """Performs the Adaboost algorithm for up to max_rounds rounds.
    Returns the resulting overall classifier H, represented as a list of
    (classifier, voting_power) tuples."""
    H = []

    point_to_weight = initialize_weights(training_points)

    rounds = 0

    while rounds < max_rounds:

        classifier_to_error_rate = calculate_error_rates(point_to_weight, classifier_to_misclassified)

        try:
            best_classifier = pick_best_classifier(classifier_to_error_rate, use_smallest_error)

        except:
            return H 
            # raise NoGoodClassifiersError

        error_rate = make_fraction(classifier_to_error_rate[best_classifier])

        voting_power = calculate_voting_power(error_rate )

        H.append( (best_classifier, voting_power) )

        misclassified_points = classifier_to_misclassified[best_classifier]

        
        if is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance):
            return H

        point_to_weight = update_weights(point_to_weight, misclassified_points, error_rate)
        rounds += 1

    return H


#### SURVEY ####################################################################

NAME = "Mehmet Tugrul Savran"
COLLABORATORS = "None"
HOW_MANY_HOURS_THIS_LAB_TOOK = "126"
WHAT_I_FOUND_INTERESTING = "Adaboost"
WHAT_I_FOUND_BORING = "Adaboost"
SUGGESTIONS = "Boost more"
