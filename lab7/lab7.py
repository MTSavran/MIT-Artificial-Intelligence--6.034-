# MIT 6.034 Lab 7: Support Vector Machines
# Written by Jessica Noss (jmn) and 6.034 staff

from svm_data import *


# Vector math
def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    dotproduct = 0
    for i in range(len(u)):
        dotproduct += u[i] * v[i]
    return dotproduct

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    sq = 0
    for i in range(len(v)):
        sq+= v[i]**2
    return sq**0.5

# Equation 1
def positiveness(svm, point):
    "Computes the expression (w dot x + b) for the given point"
    return dot_product(svm.w,point) + svm.b 

def classify(svm, point):
    """Uses given SVM to classify a Point.  Assumes that point's true
    classification is unknown.  Returns +1 or -1, or 0 if point is on boundary"""
    val = positiveness(svm,point)
    if val >0:
        return 1
    if val <0:
        return -1
    return 0

# Equation 2
def margin_width(svm):
    "Calculate margin width based on current boundary."
    return 2.0/(norm(svm.w))

# Equation 3
def check_gutter_constraint(svm):
    """Returns the set of training points that violate one or both conditions:
        * gutter constraint (positiveness == classification for support vectors)
        * training points must not be between the gutters
    Assumes that the SVM has support vectors assigned."""
    violators = set()
    diff = set()
    pointlist = svm.training_points
    supportvecs = svm.support_vectors
    for vec in supportvecs:
        if vec.classification != positiveness(svm,vec):
            violators.add(vec)
        diff.add(vec)
    for point in pointlist:
        if point not in diff:
            if positiveness(svm,point) < 1 and positiveness(svm,point) > -1:
                violators.add(point)
    return violators

# Equations 4, 5
def check_alpha_signs(svm):
    """Returns the set of training points that violate either condition:
        * all non-support-vector training points have alpha = 0
        * all support vectors have alpha > 0
    Assumes that the SVM has support vectors assigned, and that all training
    points have alpha values assigned."""
    diff = set()
    violators = set()
    supvecs = svm.support_vectors
    pointlist = svm.training_points
    for vec in supvecs:
        if vec.alpha <=0:
            violators.add(vec)
        diff.add(vec)

    for point in pointlist:
        if point not in diff:
            if point.alpha != 0:
                violators.add(point)
    return violators

def check_alpha_equations(svm):
    """Returns True if both Lagrange-multiplier equations are satisfied,
    otherwise False.  Assumes that the SVM has support vectors assigned, and
    that all training points have alpha values assigned."""
    summ = 0
    diff = set()
    supvecs = svm.support_vectors
    pointlist = svm.training_points
    for vec in supvecs:
        summ += vec.classification*vec.alpha
        diff.add(vec)
    for point in pointlist:
        if point not in diff:
            summ += point.classification*point.alpha

    eqn4 = summ == 0

    vecsum = [0]*len(point)
    for point in pointlist:
        vecsum = vector_add(scalar_mult(point.classification*point.alpha,point),vecsum)
    
    eqn5 = vecsum == svm.w 
    return eqn4 and eqn5 
# Classification accuracy
def misclassified_training_points(svm):
    """Returns the set of training points that are classified incorrectly
    using the current decision boundary."""
    miss = set()
    for point in svm.training_points:

        if classify(svm,point) != point.classification:
            miss.add(point)
    return miss

# Training
def update_svm_from_alphas(svm):
    """Given an SVM with training data and alpha values, use alpha values to
    update the SVM's support vectors, w, and b.  Return the updated SVM."""
    supvecs = []
    for point in svm.training_points:
        if point.alpha >0:
            supvecs.append(point)
    w = [0,0]
    for vec in supvecs:
        w = vector_add(scalar_mult(vec.classification*vec.alpha,vec),w)
    bspos = []
    bsneg = []
    for vec in supvecs:
        if vec.classification <0:
            bsneg.append(vec.classification -(dot_product(w,vec.coords)))
        else: 
            bspos.append(vec.classification -(dot_product(w,vec.coords)))

    minim = min(bsneg)
    maxim = max(bspos)
    b = (minim + maxim)*0.5
    svm.support_vectors = supvecs
    svm = svm.set_boundary(w,b)
    return svm

# Multiple choice
ANSWER_1 = 11
ANSWER_2 = 6
ANSWER_3 = 3
ANSWER_4 = 2

ANSWER_5 = ["A","D"]
ANSWER_6 = ["A","B","D"]
ANSWER_7 = ["A","B","D"]
ANSWER_8 = []
ANSWER_9 = ["A","B","D"]
ANSWER_10 = ["A","B","D"]

ANSWER_11 = False
ANSWER_12 = True
ANSWER_13 = False
ANSWER_14 = False
ANSWER_15 = False
ANSWER_16 = True

ANSWER_17 = [1,3,6,8]
ANSWER_18 = [1,2,4,5,6,7,8]
ANSWER_19 = [1,2,4,5,6,7,8]

ANSWER_20 = 6


#### SURVEY ####################################################################

NAME = "Mehmet Tugrul Savran"
COLLABORATORS = "None"
HOW_MANY_HOURS_THIS_LAB_TOOK = 3
WHAT_I_FOUND_INTERESTING = "SVMs in general"
WHAT_I_FOUND_BORING = "Nothing really!"
SUGGESTIONS = "Great visualization! Thanks"
