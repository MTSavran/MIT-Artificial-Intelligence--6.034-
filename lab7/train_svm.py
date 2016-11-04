#!/usr/bin/env python2

# MIT 6.034 Lab 7: Support Vector Machines
# This file is based on code originally written by Crystal Pan.

from lab7 import *
from display_svm import create_svm_graph
INF = float('inf')
from time import time


"""
sample_data_1:

 + 5     /
   4 +  /  -
   3   /
   2  /  -
   1 /       -
-1 0 1 2 3 4 5


sample_data_2:

6   \             +
5    \   +
4     \
3  -   \
2       \   +
1  -     \
0  1  2  3  4  5  6
"""


def train_svm(training_points, kernel_fn=dot_product, max_iter=500,
              show_graph=True, animate=True, animation_delay=0.5, manual_animation=False):
    """Performs SMO using all of the training points until there are no changed
    alphas or until the max iteration depth is reached"""
    # Define alias for kernel function, converting Points to coordinates just in case
    K = lambda p1, p2: kernel_fn(p1.coords, p2.coords)

    # Copy training data to avoid modifying input data
    training_points = deepcopy(training_points)

    # Initialize SVM
    svm = SupportVectorMachine([0,0], 0, training_points, [])

    if show_graph:
        if not manual_animation:
            update_svm_plot = create_svm_graph(training_points)

        if (animate and animation_delay > 0) or manual_animation:
            # Keep track of last update time and old SVM values
            last_update_time = time()
            old_w = [0,0]
            old_b = 0
            old_support_vectors = []

    b = 0
    iteration = 0

    while iteration < max_iter:

        # Keep track of current alpha values
        old_alphas = map(lambda pt: pt.alpha, training_points)

        # Two nested summations, as in lecture
        for i in training_points:
            for j in training_points:

                # If the points are the same or have the same coordinates, skip this pair
                if i.name == j.name or i.coords == j.coords:
                    continue

                # Compute lower and upper bounds on j.alpha
                if i.classification == j.classification:
                    if i.alpha == 0 and j.alpha == 0:
                        # Skip this pair, because they are both non-SVs of the same class,
                        # so no need to update their alphas or make one become a SV
                        continue
                    lower_bound = 0
                    upper_bound = i.alpha + j.alpha
                else:
                    lower_bound = max(0, j.alpha - i.alpha)
                    upper_bound = INF

                # Compute current error of alpha_i and alpha_j
                error_i = reduce(lambda total,pt: total + (pt.classification * pt.alpha * K(i,pt) + b), training_points, 0) - i.classification
                error_j = reduce(lambda total,pt: total + (pt.classification * pt.alpha * K(j,pt) + b), training_points, 0) - j.classification

                # Store old alpha values before updating
                old_alpha_i = i.alpha
                old_alpha_j = j.alpha

                # Update j.alpha, but keep it between lower and upper bounds
                n = 2 * K(i,j) - K(i,i) - K(j,j) # Note: if K is dot_product, n = -||i-j||^2
                j.alpha = old_alpha_j - ( j.classification * (error_i - error_j) / float(n) )
                if j.alpha > upper_bound:
                    j.alpha = upper_bound
                elif j.alpha < lower_bound:
                    j.alpha = lower_bound

                # If j.alpha hasn't changed *at all*, continue
                if j.alpha == old_alpha_j:
                    continue

                # Update i.alpha, but ensure it stays non-negative
                i.alpha = max(0, old_alpha_i + (i.classification * j.classification) * (old_alpha_j - j.alpha))

                # Update SVM based on alphas
                update_svm_from_alphas(svm) # Note: kernel_fn is hardcoded as dot_product

                # Update b from SVM
                b = svm.b

            if show_graph and (animate or manual_animation):
                show_update = True
                if animation_delay > 0 or manual_animation:
                    # If values have not changed perceptibly, skip this update
                    if (map(lambda sv: sv.name, svm.support_vectors) == map(lambda sv: sv.name, old_support_vectors)
                          and ((b==0 and old_b==0 and list_approx_equal(svm.w, old_w, 0.001))
                               or (b!=0 and old_b !=0 and list_approx_equal(scalar_mult(1./b, svm.w), scalar_mult(1./old_b, old_w), 0.001)))):
                        show_update = False
                    else:
                        # Update old stored values
                        old_w = svm.w[:]
                        old_b = svm.b
                        old_support_vectors = svm.support_vectors[:]

                if show_update:
                    if manual_animation:
                        # Recreate graph and block further execution
                        create_svm_graph(training_points)(svm, True)
                        # When user closes graph window, update timer to current time
                        last_update_time = time()
                    else:
                        if animation_delay > 0:
                            while time() - last_update_time < animation_delay:
                                pass
                            # Update time before updating plot, in case rendering is slow
                            last_update_time = time()
                        update_svm_plot(svm)

        iteration += 1

        # If alpha values have not changed *at all*, cease training
        if old_alphas == map(lambda pt: pt.alpha, training_points):
            break

    print '# iterations:', iteration

    # Compute final w, b, and SVs based on alphas
    update_svm_from_alphas(svm) # Note: kernel_fn is hardcoded as dot_product

    # Check training
    misclassified = misclassified_training_points(svm)
    print "Training complete! SVM with decision boundary %.3f*x + %.3f*y + %.3f >= 0 misclassified %i points." \
        % (svm.w[0], svm.w[1], svm.b, len(misclassified))

    if show_graph:
        if manual_animation:
            update_svm_plot = create_svm_graph(training_points)
        # Update graph with final values
        update_svm_plot(svm, final_update=True)

    # Return the trained SVM
    return svm


if __name__ == '__main__':
    # Uncomment below to train on a different dataset.  Feel free to use different arguments!
    #train_svm(sample_data_1)
#    train_svm(sample_data_2)
     train_svm(recit_data)
#    train_svm(harvard_mit_data)
#    train_svm(unseparable_data, animation_delay=0)
