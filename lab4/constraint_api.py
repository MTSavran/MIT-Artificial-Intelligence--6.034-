# MIT 6.034 Lab 4: Constraint Satisfaction Problems

from copy import deepcopy

class Constraint :
    def __init__(self, var1, var2, constraint_fn) :
        self.var1 = var1
        self.var2 = var2
        self.constraint_fn = constraint_fn

    def reverse(self) :
        return Constraint(self.var2, self.var1, lambda a,b: self.constraint_fn(b,a))

    def check(self, val1, val2) :
        "Returns True if values satisfy constraint_fn, otherwise False"
        return bool(self.constraint_fn(val1, val2))

    def __str__(self):
        return 'Constraint(%s, %s, %s)' % (str(self.var1), str(self.var2),
                                           self.constraint_fn.__name__)
    __repr__ = __str__

    def __eq__(self, other):
        return (isinstance_Constraint(other)
                and self.var1 == other.var1
                and self.var2 == other.var2
                and self.constraint_fn.__code__.co_code == other.constraint_fn.__code__.co_code)


def constraint_equal(a,b) :
    return a == b

def constraint_different(a,b) :
    return a != b


class ConstraintSatisfactionProblem :
    def __init__(self, variables, constraints=[]) :
        self.variables = sorted(variables[:])
        self.constraints = deepcopy(constraints)
        self.unassigned_vars = self.variables[:]
        self.domains = deepcopy({})
        self.assigned_values = deepcopy({})

    def get_domain(self, var) :
        "Returns the list of values in the variable's domain."
        if var not in self.variables :
            raise KeyError(str(var) + " is not a variable in this problem." + str(self.variables))
        return self.domains.get(var, [])

    def set_domain(self, var, domain) :
        """Sets the domain of the variable to the specified list of values,
        sorted alphabetically/numerically."""
        if var not in self.variables :
            raise KeyError(str(var) + " is not a variable in this problem.")
        self.domains[var] = sorted(domain[:])
        return self

    def set_all_domains(self, domains_dict) :
        """Sets the .domains attribute to the specified dictionary.  Does not
        sort domains."""
        if not set(domains_dict.keys()) <= set(self.variables):
            invalid_vars = filter(lambda v: v not in self.variables, domains_dict.keys())
            raise KeyError(str(invalid_vars) + " are not variables in this problem.")
        self.domains = deepcopy(domains_dict)
        return self

    def get_all_variables(self):
        "Returns a list of all the variables in the problem."
        return self.variables[:]

    def get_all_constraints(self):
        "Returns a list of all the constraints in the problem."
        return self.constraints[:]

    def eliminate(self, var, val) :
        """Removes the value from variable's domain.  Returns True if
        the domain contained the value when this function was
        called; False if the domain didn't contain the value."""
        values = self.domains.get(var, [])
        found = val in values
        if found:
            values.remove(val)
        self.domains[var] = values
        return found

    def get_assigned_value(self, var) :
        """If the variable has been assigned a value, retrieve it. Returns None
        if the variable hasn't been assigned yet"""
        return self.assigned_values.get(var, None)

    def set_assigned_value(self, var, val) :
        """Sets the assigned value of the variable to val, returning a modified
        copy of the constraint satisfaction problem. Throws an error if val is
        not in the domain of the variable, or if var has already been assigned
        a value. For convenience, also modifies the variable's domain to contain
        only the assigned value."""
        if self.assigned_values.get(var) is not None:
            raise AttributeError("Can't assign variable " + str(var) + " to value " + str(val) + ": var has already been assigned value " + str(self.assigned_values.get(var)) +".")
        elif val not in self.get_domain(var) :
            raise KeyError("The domain of " + str(var) + " does not contain the value " + str(val) + ".")
        self.domains[var] = [val]
        self.assigned_values[var] = val
        if var in self.unassigned_vars:
            self.unassigned_vars.remove(var)
        return self

    def set_assigned_values(self, var_val_pairs):
        map(lambda p: self.set_assigned_value(*p), var_val_pairs)
        return self

    def pop_next_unassigned_var(self):
        """Returns first unassigned variable, or None if all variables are
        assigned.  Modifies unassigned_vars list."""
        return self.unassigned_vars.pop(0) if self.unassigned_vars else None

    def add_constraint(self, var1, var2, constraint_fn) :
        """Given two variables and a function to act as a constraint between
        them, creates a Constraint and adds it to the list of constraints"""
        self.constraints.append(Constraint(var1, var2, constraint_fn))
        return self

    def add_constraints(self, constraint_list):
        "Adds all of the specified constraints to the problem"
        self.constraints.extend(deepcopy(constraint_list))
        return self

    def constraints_between(self, var1=None, var2=None) :
        """Returns a list of constraints in the problem. If either
        variable is provided, returns only variables that start/end
        at those variables."""

        # The returned constraints will be transformed so that var1
        # comes first and var2 comes second, as requested.

        pred1 =  lambda node : (var1 is None) or (node == var1)
        pred2 =  lambda node : (var2 is None) or (node == var2)

        return filter(
            lambda e : e is not None,
            [e if pred1(e.var1) and pred2(e.var2) else
             e.reverse() if pred2(e.var1) and pred1(e.var2)
             else None
             for e in self.constraints
        ])

    def get_neighbors(self, var):
        "Returns a list of variables that share constraints with var"
        return sorted(set(map(lambda c: c.var2, self.constraints_between(var))))

    def set_unassigned_vars_order(self, unassigned_vars_ordered) :
        """Given an ordered list of unassigned variables, sets the list of
        unassigned vars."""
        if (unassigned_vars_ordered is not None
            and not (set(unassigned_vars_ordered) <= set(self.variables))) :
            raise AttributeError("unassigned_vars_ordered contains items that "
                                 +"are not variables in this problem")
        if any([var in self.assigned_values.keys() for var in unassigned_vars_ordered]):
            raise AttributeError("unassigned_vars_ordered contains variables "
                                 +"that are already assigned")
        self.unassigned_vars = unassigned_vars_ordered[:]
        return self

    def copy(self) :
        "Return a (deep) copy of this problem."
        return deepcopy(self)

    def __str__(self):
        len_and_str = lambda x: tuple([fn(x) for fn in (len, str)])
        return ('ConstraintSatisfactionProblem with:'
                + '\n * %i variables: %s' % len_and_str(self.variables)
                + '\n * %i constraints: %s' % len_and_str(self.constraints)
                + '\n * %i domains: %s' % len_and_str(self.domains)
                + '\n * %i unassigned vars: %s' % len_and_str(self.unassigned_vars)
                + '\n * %i assigned values: %s' % len_and_str(self.assigned_values))

    def __eq__(self, other):
        return (isinstance_ConstraintSatisfactionProblem(other)
                and self.variables == other.variables
                and self.constraints == other.constraints
                and self.unassigned_vars == other.unassigned_vars
                and self.domains == other.domains
                and self.assigned_values == other.assigned_values)


def is_class_instance(obj, class_name):
    return hasattr(obj, '__class__') and obj.__class__.__name__ == class_name

def isinstance_Constraint(obj):
    return is_class_instance(obj, 'Constraint')

def isinstance_ConstraintSatisfactionProblem(obj):
    return is_class_instance(obj, 'ConstraintSatisfactionProblem')
