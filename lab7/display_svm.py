# MIT 6.034 Lab 7: Support Vector Machines
# This file is based on code originally written by Kelly Shen.

import matplotlib.pyplot as pl

# Helper functions
get_x = lambda pt: pt[0]
get_y = lambda pt: pt[1]

def create_svm_graph(training_points):
    """Graphs and displays training data.  Returns an update function
        update_svm_plot(svm, final_update=False)
    which can be used to update the graph with the SVM's decision boundary,
    gutters, and support vectors."""

    # Use interactive mode for graph updates during training
    pl.ion()

    # Add gridlines
    pl.grid()

    training_point_x_vals = map(get_x, training_points)
    training_point_y_vals = map(get_y, training_points)

    # Define graph range
    x_min_actual, x_max_actual = min(training_point_x_vals), max(training_point_x_vals)
    x_diff = x_max_actual - x_min_actual
    x_min = x_min_actual - x_diff*0.2
    x_max = x_max_actual + x_diff*0.2
    pl.xlim([x_min, x_max])

    y_min_actual, y_max_actual = min(training_point_y_vals), max(training_point_y_vals)
    y_diff = y_max_actual - y_min_actual
    y_min = y_min_actual - y_diff*0.2
    y_max = y_max_actual + y_diff*0.2
    pl.ylim([y_min, y_max])

    # Partition training points into positive and negative
    positive_point_x_vals, positive_point_y_vals = [], []
    negative_point_x_vals, negative_point_y_vals = [], []
    for pt in training_points:
        if pt.classification == 1:
            positive_point_x_vals.append(pt.coords[0])
            positive_point_y_vals.append(pt.coords[1])
        else:
            negative_point_x_vals.append(pt.coords[0])
            negative_point_y_vals.append(pt.coords[1])

    # Plot training points as red (positive) and blue (negative) circles
    pl.plot(positive_point_x_vals, positive_point_y_vals, "ro")
    pl.plot(negative_point_x_vals, negative_point_y_vals, "bo")

    # Prepare to plot support vectors as open circles
    sv_circles, = pl.plot([], [], "o", markersize=14, mfc='none')

    # Prepare to plot boundary line (solid black) and gutters (dashed black)
    boundary_line, = pl.plot([], [], "k")
    positive_gutter_line, = pl.plot([], [], "k--")
    negative_gutter_line, = pl.plot([], [], "k--")

    pl.pause(0.0001)


    # Create update function for this SVM
    def update_svm_plot(svm, final_update=False):
        """Update the SVM's graph with the current decision boundary and
        gutters, as determined by w and b, and the current support vectors.
        If final_update is True, displays the graph statically after update,
        blocking execution until the graph is closed."""
        w, b, support_vectors = svm.w, svm.b, svm.support_vectors

        # Circle support vectors
        sv_circles.set_xdata(map(get_x, support_vectors))
        sv_circles.set_ydata(map(get_y, support_vectors))

        # Create helper function for computing points on boundary and gutters
        def compute_y(x, c=0):
            "Given x, returns y such that [x,y] is on the line w dot [x,y] + b = c"
            return (-w[0] * x - b + c) / float(w[1])
        def compute_x(y, c=0):
            "Given y, returns x such that [x,y] is on the line w dot [x,y] + b = c"
            return (-w[1] * y - b + c) / float(w[0])

        def update_line(line, c=0):
            """helper function for updating a pyplot line (specifically, the
            decision boundary or a gutter)"""
            try:
                line.set_xdata([x_min, x_max])
                line.set_ydata([compute_y(x_min, c), compute_y(x_max, c)])
            except ZeroDivisionError:
                # line is vertical
                line.set_xdata([compute_x(y_min, c), compute_x(y_max, c)])
                line.set_ydata([y_min, y_max])

        # Update decision boundary (w dot x + b = 0)
        update_line(boundary_line)

        # Update gutters (w dot x + b = +/-1)
        update_line(positive_gutter_line, 1)
        update_line(negative_gutter_line, -1)

        # Redraw graph
        pl.pause(0.0001)

        if final_update:
            # Turn off interactive mode so that pl.show() will block
            pl.ioff()
            pl.show()

    # Return update function
    return update_svm_plot
