# MIT 6.034 Lab 5: k-Nearest Neighbors and Identification Trees

import os
from copy import deepcopy

################################################################################
############################# IDENTIFICATION TREES #############################
################################################################################

class Classifier :
    def __init__(self, name, classify_fn) :
        self.name = str(name)
        self._classify_fn = classify_fn

    def classify(self, point):
        try:
            return self._classify_fn(point)
        except KeyError, key:
            raise ClassifierError("point has no attribute " + str(key) + ": " + str(point))

    def copy(self):
        return deepcopy(self)

    def __eq__(self, other):
        try:
            return (self.name == other.name
                    and self._classify_fn.__code__.co_code == other._classify_fn.__code__.co_code)
        except:
            return False

    def __str__(self):
        return "Classifier<" + str(self.name) + ">"

    __repr__ = __str__


## HELPER FUNCTIONS FOR CREATING CLASSIFIERS

def maybe_number(x) :
    try :
        return float(x)
    except (ValueError, TypeError) :
        return x

def feature_test(key) :
    return Classifier(key, lambda pt : maybe_number(pt[key]))

def threshold_test(feature, threshold) :
    return Classifier(feature + " > " + str(threshold),
                      lambda pt: "Yes" if (maybe_number(pt.get(feature)) > threshold) else "No")


## CUSTOM ERROR CLASSES

class NoGoodClassifiersError(ValueError):
    def __init__(self, value=""):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ClassifierError(RuntimeError):
    def __init__(self, value=""):
        self.value = value
    def __str__(self):
        return repr(self.value)


class IdentificationTreeNode:
    def __init__(self, target_classifier, parent_branch_name=None):
        self.target_classifier = target_classifier
        self._parent_branch_name = parent_branch_name
        self._classification = None #value, if leaf node
        self._classifier = None #Classifier, if tree continues
        self._children = {} #dict mapping feature to node, if tree continues
        self._data = [] #only used temporarily for printing with data

    def get_parent_branch_name(self):
        return self._parent_branch_name if self._parent_branch_name else "(Root node: no parent branch)"

    def is_leaf(self):
        return not self._classifier

    def set_node_classification(self, classification):
        self._classification = classification
        if self._classifier:
            print "Warning: Setting the classification", classification, "converts this node from a subtree to a leaf, overwriting its previous classifier:", self._classifier
            self._classifier = None
            self._children = {}
        return self

    def get_node_classification(self):
        return self._classification

    def set_classifier_and_expand(self, classifier, features):
        if classifier is None:
            raise TypeError("Cannot set classifier to None")
        if not isinstance_Classifier(classifier):
            raise TypeError("classifier must be Classifier-type object: " + str(classifier))
        self._classifier = classifier

        try:
            self._children = {feature:IdentificationTreeNode(self.target_classifier, parent_branch_name=str(feature))
                              for feature in features}
        except TypeError:
            raise TypeError("Expected list of feature names, got: " + str(features))
        if len(self._children) == 1:
            print "Warning: The classifier", classifier.name, "has only one relevant feature, which means it's not a useful test!"
        if self._classification:
            print "Warning: Setting the classifier", classifier.name, "converts this node from a leaf to a subtree, overwriting its previous classification:", self._classification
            self._classification = None
        return self

    def get_classifier(self):
        return self._classifier

    def apply_classifier(self, point):
        if self._classifier is None:
            raise ClassifierError("Cannot apply classifier at leaf node")
        return self._children[self._classifier.classify(point)]

    def get_branches(self):
        return self._children

    def copy(self):
        return deepcopy(self)

    def print_with_data(self, data):
        tree = self.copy()
        tree._assign_data(data)
        print tree.__str__(with_data=True)

    def _assign_data(self, data):
        if not self._classifier:
            self._data = deepcopy(data)
            return self
        try:
            pairs = self._soc(data, self._classifier).items()
        except KeyError: #one of the points is missing a feature
            raise ClassifierError("One or more points cannot be classified by " + str(self._classifier))

        for (feature, branch_data) in pairs:
            if self._children.has_key(feature):
                self._children[feature]._assign_data(branch_data)
            else: #feature branch doesn't exist
                self._data.extend(branch_data)
        return self

    _ssc=lambda self,c,d:self.set_classifier_and_expand(c,self._soc(d,c))
    _soc=lambda self,d,c:reduce(lambda b,p:b.__setitem__(c.classify(p),b.get(c.classify(p),[])+[p]) or b,d,{})

    def __eq__(self, other):
        try:
            return (self.target_classifier == other.target_classifier
                    and self._parent_branch_name == other._parent_branch_name
                    and self._classification == other._classification
                    and self._classifier == other._classifier
                    and self._children == other._children
                    and self._data == other._data)
        except:
            return False

    def __str__(self, indent=0, with_data=False):
        newline = os.linesep
        ret = ''
        if indent == 0:
            ret += (newline + "IdentificationTreeNode classifying by "
                    + self.target_classifier.name + ":" + newline)
        ret += "    "*indent + (self._parent_branch_name + ": " if self._parent_branch_name else '')
        if self._classifier:
            ret += self._classifier.name
            if with_data and self._data:
                ret += self._render_points()
            for (feature, node) in sorted(self._children.items()):
                ret += newline + node.__str__(indent+1, with_data)
        else: #leaf
            ret += str(self._classification)
            if with_data and self._data:
                ret += self._render_points()
        return ret

    def _render_points(self):
        ret = ' ('
        first_point = True
        for point in self._data:
            if first_point:
                first_point = False
            else:
                ret += ', '
            ret += str(point.get("name","datapoint")) + ": "
            try:
                ret += str(self.target_classifier.classify(point))
            except ClassifierError:
                ret += '(unknown)'
        ret += ')'
        return ret


################################################################################
############################# k-NEAREST NEIGHBORS ##############################
################################################################################

class Point(object):
    """A Point has a name and a list or tuple of coordinates, and optionally a
    classification, and/or alpha value."""
    def __init__(self, coords, classification=None, name=None):
        self.name = name
        self.coords = coords
        self.classification = classification

    def copy(self):
        return deepcopy(self)

    def __getitem__(self, i): # make Point iterable
        return self.coords[i]

    def __eq__(self, other):
        try:
            return (self.coords == other.coords
                    and self.classification == other.classification)
        except:
            return False

    def __str__(self):
        ret = "Point(" + str(self.coords)
        if self.classification:
            ret += ", " + str(self.classification)
        if self.name:
            ret += ", name=" + str(self.name)
        ret += ")"
        return ret

    __repr__ = __str__


################################################################################
############################### OTHER FUNCTIONS ################################
################################################################################

def is_class_instance(obj, class_name):
    return hasattr(obj, '__class__') and obj.__class__.__name__ == class_name

def isinstance_Classifier(obj):
    return is_class_instance(obj, 'Classifier')

def isinstance_IdentificationTreeNode(obj):
    return is_class_instance(obj, 'IdentificationTreeNode')

def isinstance_Point(obj):
    return is_class_instance(obj, 'Point')
