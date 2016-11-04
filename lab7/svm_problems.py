# MIT 6.034 Lab 7: Support Vector Machines

from svm_api import *

# Aliases for convenience
SVM = SupportVectorMachine
Boundary = DecisionBoundary

# Points
ptA = Point('A', [1, 1], +1, 1)
ptB = Point('B', [1, 3], +1, 1)
ptD = Point('D', [2, 2], -1, 2)
ptE = Point('E', [3, 2], -1, 0)
ptF = Point('F', [4, 5], +1, 0)
ptG = Point('G', [0, 9], alpha=-1)
ptH = Point('H', [6, 7], alpha=0.3)
ptJ = Point('J', [1, 8], alpha=-0.1)
ptK = Point('K', [0.1, 0.1], -1, 4)
ptL = Point('L', [1.8, 2], -1, 0)

# Recitation example solution
svm_basic = SVM(Boundary([-2, 0], 3), [ptA, ptB, ptD, ptE], [ptA, ptB, ptD])

# Untrained: D on boundary, F misclassified
svm_untrained = SVM(Boundary([-1, 0], 2),
                    [ptA, ptB, ptD, ptE, ptF],
                    [ptA, ptB, ptE])

# A bunch of points with alpha values, for testing check_alpha_signs
svm_alphas = SVM(None,
                 [ptF, ptJ, ptH, ptD, ptG, ptA, ptE, ptK],
                 [ptF, ptG, ptA, ptK])

svm_fail_eq4 = SVM(Boundary([-2, 0], 3),
                   [ptA, ptB, ptK, ptE],
                   [ptA, ptB, ptK])

svm_fail_eq5 = SVM(Boundary([1, 0], -1.5),
                   [ptA, ptB, ptD, ptE],
                   [ptA, ptB, ptD])
