# MIT 6.034 Lab 7: Support Vector Machines

from copy import deepcopy

def approx_equal(a, b, epsilon=0.00000001):
    return abs(a-b) <= epsilon

def list_approx_equal(list1, list2, epsilon=0.00000001):
    return len(list1) == len(list2) and all([approx_equal(a,b,epsilon) for (a,b) in zip(list1,list2)])

class Point(object):
    """A Point has a name and a list or tuple of coordinates, and optionally a
    classification, and/or alpha value."""
    def __init__(self, name, coords, classification=None, alpha=None):
        self.name = name
        self.coords = coords
        self.classification = classification
        self.alpha = alpha

    def copy(self):
        return deepcopy(self)

    def __getitem__(self, i): # make Point iterable
        return self.coords[i]

    def __len__(self):
        return len(self.coords)

    def __eq__(self, other):
        try:
            return (self.coords == other.coords
                    and self.classification == other.classification
                    and self.alpha == other.alpha)
        except Exception:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        if self.classification is None and self.alpha is None:
            return "Point(%s, %s)" % (str(self.name), str(self.coords))
        return "Point(%s, %s, class=%s, alpha=%s)" % (str(self.name), \
            str(self.coords), str(self.classification), str(self.alpha))

    __repr__ = __str__


class SupportVectorMachine(object):
    """A SupportVectorMachine is a classifier that uses a decision boundary to
    classify points.  The decision boundary is defined by two parameters: a
    normal vector w (represented as a list or tuple of coordinates), and an
    offset b.  The SVM has a list of training points and optionally a list of
    support vectors."""
    def __init__(self, w=[], b=0, training_points=[], support_vectors=[]):
        self.w = w[:]
        self.b = b
        self.training_points = training_points[:]
        self.support_vectors = support_vectors[:]

    def set_boundary(self, new_w, new_b):
        self.w = new_w[:]
        self.b = new_b
        return self

    def copy(self):
        return deepcopy(self)

    def __eq__(self, other, epsilon=0.00000001):
        try:
            assert list_approx_equal(self.w, other.w, epsilon)
            assert approx_equal(self.b, other.b, epsilon)
            assert equality_by_string(self.training_points, other.training_points)
            assert equality_by_string(self.support_vectors, other.support_vectors)
            return True
        except Exception:
            return False

    def __ne__(self, other, epsilon=0.00000001):
        return not self.__eq__(other, epsilon)

    def __str__(self):
        len_and_str = lambda x: tuple([fn(x) for fn in (len, str)])
        return ('SupportVectorMachine with:'
            + '\n * boundary with w=%s, b=%s' % (str(self.w), str(self.b))
            + '\n * %i training points: %s' % len_and_str(self.training_points)
            + '\n * %i support vectors: %s' % len_and_str(self.support_vectors))

    __repr__ = __str__


def vector_add(v1, v2):
    """Given two iterable vectors or Points, returns their vector sum as a list
    list of coordinates."""
    if len(v1) != len(v2):
        raise IndexError("vector_add: Input vectors must be same length")
    return [x1 + x2 for (x1,x2) in zip(v1,v2)]

def scalar_mult(scalar, vector):
    """Given a constant scalar and an iterable vector or Point, returns a scaled
    list of coordinates"""
    return [scalar*coord for coord in vector]

def equality_by_string(set1, set2):
    """This is a hack to get around reference equality.
    Returns True if two sets (or lists) contain equivalent elements"""
    return sorted(map(str, set1)) == sorted(map(str, set2))
