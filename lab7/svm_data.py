# MIT 6.034 Lab 7: Support Vector Machines

from svm_api import *

# Alias for convenience
SVM = SupportVectorMachine

# Points
ptA = Point('A', [1, 3], +1, 1)
ptB = Point('B', [1, 1], +1, 1)
ptD = Point('D', [2, 2], -1, 2)
ptE = Point('E', [3, 2], -1, 0)
ptF = Point('F', [4, 5], +1, 0)
ptG = Point('G', [0, 9], alpha=-1)
ptH = Point('H', [6, 7], alpha=0.3)
ptJ = Point('J', [1, 8], alpha=-0.1)
ptK = Point('K', [0.1, 0.1], -1, 4)
ptL = Point('L', [1.8, 2], -1, 0)
ptLx = Point('Lx', [1.5, 2], -1, 0)
ptD2 = Point('D2', [2, 2], -1, 1)
ptBx = Point('Bx', [1, 1], +1, -1)
ptDx = Point('Dx', [2, 2], -1, 1)
ptMpos = Point('M+', [4, 2], +1, 1)
ptMneg = Point('M-', [4, 2], +1, -1)

# Recitation example solution
svm_basic = SVM([-2, 0], 3, [ptA, ptB, ptD, ptE], [ptA, ptB, ptD])

# Untrained: D on boundary, F misclassified
svm_untrained = SVM([-1, 0], 2, [ptA, ptB, ptD, ptE, ptF], [ptA, ptB, ptE])

# A bunch of points with alpha values, for testing check_alpha_signs
svm_alphas = SVM([], 0, [ptF, ptJ, ptH, ptD, ptG, ptA, ptE, ptK],
                 [ptF, ptG, ptA, ptK])

svm_fail_eq4 = SVM([-2, 0], 3, [ptA, ptB, ptK, ptE], [ptA, ptB, ptK])
svm_fail_eq4_but_not_eq3 = SVM([-2, 0], 3, [ptA, ptB, ptD2, ptE], [ptA, ptB, ptD2])
svm_fail_eq4_only = SVM([-2, 0], 3, [ptA, ptBx, ptDx, ptE], [ptA, ptBx, ptDx])

svm_fail_eq5 = SVM([1, 0], -1.5, [ptA, ptB, ptD, ptE], [ptA, ptB, ptD])

svm_fail_gutter_only = SVM([-2, 0], 3, [ptA, ptB, ptD, ptE, ptL], [ptA, ptB, ptD])
svm_fail_alphas_only = SVM([-2, 0], 3, [ptA, ptB, ptD, ptMpos, ptMneg], [ptA, ptB, ptD])

# Problems for update_svm_from_alphas
svm_update_recit_0 = SVM([-1.0, 1.0], -1.0,
    [Point('A', [1, 3], 1, 1.0), Point('B', [1, 1], 1, 0), Point('D', [2, 2], -1, 1.0), Point('E', [3, 2], -1, 0)],
    [Point('A', [1, 3], 1, 1.0), Point('D', [2, 2], -1, 1.0)]
)

svm_update_recit_1 = SVM([-1.5, -0.5], 3.5,
    [Point('A', [1, 3], 1, 0.5), Point('B', [1, 1], 1, 1.0), Point('D', [2, 2], -1, 1.5), Point('E', [3, 2], -1, 0)],
    [Point('A', [1, 3], 1, 0.5), Point('B', [1, 1], 1, 1.0), Point('D', [2, 2], -1, 1.5)]
)

svm_update_recit_2 = SVM([-2.0, 0.0], 3.0,
    [Point('A', [1, 3], 1, 1.0), Point('B', [1, 1], 1, 1.0), Point('D', [2, 2], -1, 2.0), Point('E', [3, 2], -1, 0)],
    [Point('A', [1, 3], 1, 1.0), Point('B', [1, 1], 1, 1.0), Point('D', [2, 2], -1, 2.0)]
)

svm_update_harvard_mit_n = SVM([0.06574373689438234, -0.6228375087370781], 0.785468859213,
    [Point('A', [0, 4], -1, 0.0994664095146), Point('B', [2, 6], -1, 0), Point('C', [7, 5], -1, 0),
     Point('D', [6, 4], -1, 0.0520595502372), Point('E', [6, 3], -1, 0.0209578913533), Point('F', [9, 3], -1, 0),
     Point('G', [1, 0], 1, 0.123549011768), Point('I', [8, 1], 1, 0.0461400043301),
     Point('H', [4, 0], 1, 0.00279483500717), Point('J', [9, 0], 1, 0)],
    [Point('A', [0, 4], -1, 0.0994664095146), Point('D', [6, 4], -1, 0.0520595502372), Point('E', [6, 3], -1, 0.0209578913533),
     Point('G', [1, 0], 1, 0.123549011768), Point('I', [8, 1], 1, 0.0461400043301), Point('H', [4, 0], 1, 0.00279483500717)]
)


# Datasets for training, with alphas initialized to 0
sample_data_1 = [Point('A', [-1,5], 1, 0), Point('B', [1,4], 1, 0),
                 Point('C', [3,2], -1, 0), Point('D', [4,4], -1, 0), Point('E', [5,1], -1, 0)]
sample_data_2 = [Point('A', [1,1], -1, 0), Point('B', [1,3], -1, 0),
                 Point('C', [3,5], 1, 0), Point('D', [4,2], 1, 0), Point('E', [6,6], 1, 0)]
recit_data = [Point('A', [1,3], 1, 0), Point('B', [1,1], 1, 0),
              Point('D', [2,2], -1, 0), Point('E', [3,2], -1, 0)]

# 2014 Q3
harvard_mit_data = [Point('A', [0,4], -1, 0), Point('B', [2,6], -1, 0),
                    Point('C', [7,5], -1, 0), Point('D', [6,4], -1, 0),
                    Point('E', [6,3], -1, 0), Point('F', [9,3], -1, 0),
                    Point('G', [1,0], +1, 0), Point('H', [4,0], +1, 0),
                    Point('I', [8,1], +1, 0), Point('J', [9,0], +1, 0)]

unseparable_data = harvard_mit_data + [Point('X', [4,4], +1, 0)]
