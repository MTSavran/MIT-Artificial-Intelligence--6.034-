# MIT 6.034 Lab 5: k-Nearest Neighbors and Identification Trees
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), and Jake Barnwell (jb16)

from api import *
from data import *
import math
log2 = lambda x: math.log(x, 2)
INF = float('inf')

################################################################################
############################# IDENTIFICATION TREES #############################
################################################################################

def id_tree_classify_point(point, id_tree):
    """Uses the input ID tree (an IdentificationTreeNode) to classify the point.
    Returns the point's classification."""
    if id_tree.is_leaf():
        #STOP BASE CASE
        return id_tree.get_node_classification()
    dic = id_tree.get_branches()
    for child in dic:
        return id_tree_classify_point(point,dic[child]) 

def split_on_classifier(data, classifier):
    """Given a set of data (as a list of points) and a Classifier object, uses
    the classifier to partition the data.  Returns a dict mapping each feature
    values to a list of points that have that value."""
    dic = {}
    for point in data:
        result = classifier.classify(point)
        if result not in dic:
            dic[result] = []
        dic[result].append(point)
    return dic
#### CALCULATING DISORDER

def branch_disorder(data, target_classifier):
    """Given a list of points representing a single branch and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the branch."""
    totalsamples = len(data)
    tally = {}
    s = set()
    for point in data:
        c = target_classifier.classify(point)
        s.add(c)
        if c not in tally:
            tally[c] = 0 
        if c in tally:
            tally[c] += 1
    if len(s) == 1:
        return 0 #data homog
    length = len(tally.keys())
    disorder = 0
    for key in tally.keys():
        #totalsamples and length have to be equal
        disorder += - (float(tally[key])/totalsamples)*log2((float(tally[key])/totalsamples))
    return disorder



def average_test_disorder(data, test_classifier, target_classifier):
    """Given a list of points, a feature-test Classifier, and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the feature-test stump."""
    totalsize = len(data)
    branches = split_on_classifier(data,test_classifier)

    disorder = 0  
    for branch in branches:
        currentdata = branches[branch]
        samplesize = len(currentdata)
        branchdisorder = branch_disorder(currentdata,target_classifier)
        disorder += branchdisorder*samplesize/float(totalsize)
    return disorder

## To use your functions to solve part A2 of the "Identification of Trees"
## problem from 2014 Q2, uncomment the lines below and run lab5.py:
#for classifier in tree_classifiers:
#    print classifier.name, average_test_disorder(tree_data, classifier, feature_test("tree_type"))



#### CONSTRUCTING AN ID TREE

def find_best_classifier(data, possible_classifiers, target_classifier):
    """Given a list of points, a list of possible Classifiers to use as tests,
    and a Classifier for determining the true classification of each point,
    finds and returns the classifier with the lowest disorder.  Breaks ties by
    preferring classifiers that appear earlier in the list.  If the best
    classifier has only one branch, raises NoGoodClassifiersError."""
    val = float('inf')
    li = []
    d = {}
    min_cl = possible_classifiers[0]
    for classifier in possible_classifiers:
        disorder = average_test_disorder(data,classifier,target_classifier)
        li.append((disorder,possible_classifiers.index(classifier)))
        d[disorder] = classifier
        if disorder < val:
             val = disorder
             min_cl = classifier
    if val == 1.0:
        raise NoGoodClassifiersError
    return min_cl

## To find the best classifier from 2014 Q2, Part A, uncomment:
print find_best_classifier(tree_data, tree_classifiers, feature_test("tree_type"))


def construct_greedy_id_tree(data, possible_classifiers, target_classifier, id_tree_node=None):
    """Given a list of points, a list of possible Classifiers to use as tests,
    a Classifier for determining the true classification of each point, and
    optionally a partially completed ID tree, returns a completed ID tree by
    adding classifiers and classifications until either perfect classification
    has been achieved, or there are no good classifiers left."""
    if id_tree_node == None:
        id_tree_node = IdentificationTreeNode(target_classifier)
    if len(split_on_classifier(data, target_classifier).keys())==1: #SPLIT ON TARGET IF ONLY HAS ONE KEY IT IS HOMOG. 
        id_tree_node.set_node_classification(target_classifier.classify(data[0]))
    else:
        try:
            best = find_best_classifier(data, possible_classifiers, target_classifier)
            diction = split_on_classifier(data, best)
            id_tree_node = id_tree_node.set_classifier_and_expand(best, diction)
            branchdic = id_tree_node.get_branches()
            for branch in branchdic:
                construct_greedy_id_tree(diction[branch], possible_classifiers, target_classifier, branchdic[branch])
        except NoGoodClassifiersError:
            return id_tree_node    
    return id_tree_node

## To construct an ID tree for 2014 Q2, Part A:
#print construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))

## To use your ID tree to identify a mystery tree (2014 Q2, Part A4):
#tree_tree = construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))
#print id_tree_classify_point(tree_test_point, tree_tree)

## To construct an ID tree for 2012 Q2 (Angels) or 2013 Q3 (numeric ID trees):
#print construct_greedy_id_tree(angel_data, angel_classifiers, feature_test("Classification"))
#print construct_greedy_id_tree(numeric_data, numeric_classifiers, feature_test("class"))


#### MULTIPLE CHOICE

ANSWER_1 = "bark_texture"
ANSWER_2 = "leaf_shape"
ANSWER_3 = "orange_foliage"

ANSWER_4 = [2,3]
ANSWER_5 = [3]
ANSWER_6 = [2]
ANSWER_7 = 2

ANSWER_8 = "No"
ANSWER_9 = "No"


################################################################################
############################# k-NEAREST NEIGHBORS ##############################
################################################################################

#### MULTIPLE CHOICE: DRAWING BOUNDARIES

BOUNDARY_ANS_1 = 3
BOUNDARY_ANS_2 = 4

BOUNDARY_ANS_3 = 1
BOUNDARY_ANS_4 = 2

BOUNDARY_ANS_5 = 2
BOUNDARY_ANS_6 = 4
BOUNDARY_ANS_7 = 1
BOUNDARY_ANS_8 = 4
BOUNDARY_ANS_9 = 4

BOUNDARY_ANS_10 = 4
BOUNDARY_ANS_11 = 2
BOUNDARY_ANS_12 = 1
BOUNDARY_ANS_13 = 4
BOUNDARY_ANS_14 = 4


#### WARM-UP: DISTANCE METRICS

def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    dotproduct = 0 
    for i in range(len(u)):
        dotproduct += u[i]*v[i]
    return dotproduct

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    length = len(v)
    toberooted = 0 
    for i in range(length):
        toberooted += v[i]**2
    return math.sqrt(toberooted)


def euclidean_distance(point1, point2):
    "Given two Points, computes and returns the Euclidean distance between them."
    coords1 = point1.coords
    coords2 = point2.coords
    dimension = len(coords1)
    toberooted = 0 
    for i in range(dimension):
        toberooted += (coords1[i]-coords2[i])**2
    return math.sqrt(toberooted)


def manhattan_distance(point1, point2):
    "Given two Points, computes and returns the Manhattan distance between them."
    coords1 = point1.coords
    coords2 = point2.coords
    dimension = len(coords2)
    distance = 0
    for i in range(dimension):
        distance += abs(coords2[i] - coords1[i])
    return distance

def hamming_distance(point1, point2):
    "Given two Points, computes and returns the Hamming distance between them."
    distance = 0
    coords1 = point1.coords
    coords2 = point2.coords
    for c1,c2 in zip(coords1,coords2):
        if c1 != c2:
            distance += 1
    return distance
def cosine_distance(point1, point2):
    """Given two Points, computes and returns the cosine distance between them,
    where cosine distance is defined as 1-cos(angle_between(point1, point2))."""
    coords1 = point1.coords
    coords2 = point2.coords
    dp = dot_product(coords1,coords2)
    norm1 = norm(coords1)
    norm2 = norm(coords2)
    denominator = norm1*norm2
    return 1-dp/float(denominator)


#### CLASSIFYING POINTS

def get_k_closest_points(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns a list containing the k points
    from the data that are closest to the test point, according to the distance
    metric.  Breaks ties lexicographically by coordinates."""
    li = []
    for point2 in data:
        li.append((distance_metric(point, point2),point2))
    li = sorted(li, key=lambda tup: tup[1].coords)
    li = sorted(li,key=lambda tup: tup[0])
    result = []
    for i in range(k):
        result.append(li[i][1])
    return result

def knn_classify_point(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns the classification of the test
    point based on its k nearest neighbors, as determined by the distance metric.
    Assumes there are no ties."""
    points = get_k_closest_points(point,data,k,distance_metric)
    cs = []
    for element in points:
        cs.append(element.classification)
    cs = max(set(cs), key=cs.count)
    return cs
## To run your classify function on the k-nearest neighbors problem from 2014 Q2
## part B2, uncomment the line below and try different values of k:
#print knn_classify_point(knn_tree_test_point, knn_tree_data, 5, euclidean_distance)


#### CHOOSING k

def cross_validate(data, k, distance_metric): #WHAT THE HELL IS THIS
    """Given a list of points (the data), an int 0 < k <= len(data), and a
    distance metric (a function), performs leave-one-out cross-validation.
    Return the fraction of points classified correctly, as a float."""
    pay = 0
    n = len(data)
    for i in range(len(data)): 
        new = data[:i] + data[(i+1):]
        first = data[i].classification
        second = knn_classify_point(data[i],new,k,distance_metric)
        if first == second:
            pay += 1 
    return float(pay)/n



def find_best_k_and_metric(data):
    """Given a list of points (the data), uses leave-one-out cross-validation to
    determine the best value of k and distance_metric, choosing from among the
    four distance metrics defined above.  Returns a tuple (k, distance_metric),
    where k is an int and distance_metric is a function."""
    val1 = 0 
    val2 = 0
    val3 = 0
    val4 = 0
    bestk1 = 0
    bestk2 = 0 
    bestk3 = 0 
    bestk4 = 0 
    for i in range(1,len(data)):
        if val1 < cross_validate(data,i,euclidean_distance):
            val1 = cross_validate(data,i,euclidean_distance)
            bestk1 = i 

        if val2 < cross_validate(data,i,manhattan_distance):
            val2 = cross_validate(data,i,manhattan_distance)
            bestk2 = i 
        if val3 < cross_validate(data,i,hamming_distance):
            val3 = cross_validate(data,i,hamming_distance)
            bestk3 = i
        if val4 < cross_validate(data,i,cosine_distance):
            val4 = cross_validate(data,i,cosine_distance)
            bestk4 = i 

    li = [val1,val2,val3,val4]
    li = sorted(li, reverse=True)
    if li[0] == val1:
        return (bestk1,euclidean_distance)
    if li[0] == val2:
        return (bestk2,manhattan_distance)
    if li[0] == val3:
        return (bestk3,hamming_distance)
    if li[0] == val4:
        return (bestk4,cosine_distance)



## To find the best k and distance metric for 2014 Q2, part B, uncomment:
#print find_best_k_and_metric(knn_tree_data)


#### MORE MULTIPLE CHOICE

kNN_ANSWER_1 = "Overfitting"
kNN_ANSWER_2 = "Underfitting"
kNN_ANSWER_3 = 4

kNN_ANSWER_4 = 4
kNN_ANSWER_5 = 1
kNN_ANSWER_6 = 3
kNN_ANSWER_7 = 3

#### SURVEY ###################################################

NAME = "Mehmet Tugrul Savran"
COLLABORATORS = "None"
HOW_MANY_HOURS_THIS_LAB_TOOK = "7"
WHAT_I_FOUND_INTERESTING = "Knn"
WHAT_I_FOUND_BORING = "ID tree part"
SUGGESTIONS = "None"
