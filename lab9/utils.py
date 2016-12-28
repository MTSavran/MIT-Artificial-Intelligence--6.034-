# MIT 6.034 Lab 9: Boosting (Adaboost)

from math import log as ln
from fractions import Fraction

# display Fractions as e.g. 1/3 instead of Fraction(1, 3)
Fraction.__repr__ = Fraction.__str__

def make_fraction(n=0, d=1, denom_limit=1000):
    """Instantiates a Fraction equal to n/d.  If n or d is a float, fixes
    roundoff error by rounding to the nearest fraction with a denominator of at
    most denom_limit."""
    valid_rational_types = (int, long, Fraction)
    valid_types = valid_rational_types + (float,)
    if all(map(lambda x:isinstance(x, valid_rational_types), [n,d])):
        return Fraction(n,d)
    if all(map(lambda x:isinstance(x, valid_types), [n,d])):
        try:
            return Fraction(n/d).limit_denominator(denom_limit)
        except TypeError:
            raise TypeError("Invalid type for denom_limit: " + str(type(denom_limit)))
    if not isinstance(n, valid_rational_types):
        error_str = str(type(n)) + "\nNumerator n"
    else:
        error_str = str(type(d)) + "\nDenominator d"
    raise TypeError("Invalid type: " + error_str + " must be one of: " + str(valid_types))

INF = float('inf')

class NoGoodClassifiersError(ValueError):
    def __init__(self, value=""):
        self.value = value
    def __str__(self):
        return repr(self.value)

def approx_equal(a, b, epsilon=0.0001):
    "Returns True if a and b differ by at most epsilon, otherwise False"
    return abs(a-b) <= epsilon

def classifier_approx_equal(H1, H2, epsilon=0.0001):
    """Returns True if two overall classifiers have the same sequence of weak
    classifiers and approximately the same voting powers (to within epsilon),
    otherwise False"""
    return (len(H1) == len(H2) and
            all([H1[i][0] == H2[i][0] and approx_equal(H1[i][1], H2[i][1], epsilon)
                 for i in range(len(H1))]))
