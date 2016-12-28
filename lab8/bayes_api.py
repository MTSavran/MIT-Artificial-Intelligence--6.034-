# MIT 6.034 Lab 8: Bayesian Inference

import copy

def approx_equal(a, b, epsilon=0.0000000001):
    """Returns True if two numbers a and b are equal to within epsilon,
    otherwise False"""
    return abs(a-b) <= epsilon

def product(factors):
    "Computes the product of a list of numbers"
    return reduce(lambda x,y: x*y, factors, 1)


# syntactic sugar for expanding, e.g. P(A) into P({A : True})
def negate(var) :
    return {var : False}
def affirm(var) :
    return {var : True}


def filter_dict(pred, d) :
    """Return a subset of the dictionary d, consisting only of the keys that satisfy pred(key)."""
    ret = {}
    for k in d :
        if pred(k) :
            ret[k] = d[k]
    return ret

def assoc(keyvals, key, val) :
    """Searches the list of keyval pairs for a matching key. If found, associates the value with the key. Otherwise, appends the key/val pair to the list. Returns the updated keyval list."""
    ret = [ (k, val) if k == key else (k,v) for k,v in keyvals]
    if not any([k == key for k,v in keyvals]) :
        ret.append((key,val))
    return ret

def get(keyvals, key, val_if_not_found=None) :
    for k,v in keyvals :
        if k == key :
            return v
    return val_if_not_found

class BayesNet:
    def __init__(self, variables=None) :
        self.variables = variables or []
        self.adjacency = {}
        self.conditional_probability_table = []
        self.domain = {}

    def __eq__(self, other):
        try:
            assert self.variables == other.variables
            assert self.adjacency == other.adjacency
            assert self.conditional_probability_table == other.conditional_probability_table
            assert self.domain == other.domain
            return True
        except Exception:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_variables(self):
        return list(self.variables)

    def get_children(self, var) :
        """Return a set containing the children of var."""
        if var not in self.variables:
            raise LookupError, str(var)+" is not a variable in this network."
        return self.adjacency.get(var, set([])).copy()

    def get_parents(self, var) :
        """Return a set containing the parents of var."""
        if var not in self.variables:
            raise LookupError, str(var)+" is not a variable in this network."
        return set(filter(lambda w: var in self.adjacency.get(w,[]),
                          self.variables))


    def is_neighbor(self, var1, var2) :
        """Return True if var1 is a parent of var2 or vice-versa, otherwise
        False."""
        return var1 in self.get_parents(var2) or var2 in self.get_parents(var1)



    def link(self, var_parent, var_child) :
        """Make var_parent a parent of var_child."""
        if var_parent not in self.adjacency :
            self.adjacency[var_parent] = set([])
        self.adjacency[var_parent].add(var_child)
        return self

    def unlink(self, var1, var2=None) :
        """Remove link between var1 and var2, if any.
        If var2 is not specified, removes all links connected to var1."""
        if var2 == None:
            map(lambda v2: self.unlink(var1, v2), self.variables)
            return self

        if var1 not in self.adjacency:
            self.adjacency[var1] = set()
        if var2 not in self.adjacency :
            self.adjacency[var2] = set()

        self.adjacency[var1].discard(var2)
        self.adjacency[var2].discard(var1)

        if self.adjacency[var1] == set():
            del self.adjacency[var1]
        if var1 != var2 and self.adjacency[var2] == set():
            del self.adjacency[var2]

        return self

    def make_bidirectional(self):
        "Adds links to make all edges bidirectional"
        for var1 in self.variables:
            for var2 in self.get_children(var1):
                self.link(var2, var1)
        return self

    def remove_variable(self, var):
        """Removes var from net and deletes all links to/from var.
        If var is not in net, does nothing."""
        self.unlink(var)
        self.variables.remove(var)
        return self

    def find_path(self, start_var, goal_var):
        """Performs BFS to find a path from start_var to goal_var.  Returns path
        as a list of nodes (variables), or None if no path was found."""
        if start_var not in self.variables or goal_var not in self.variables:
            return None
        if start_var == goal_var:
            return [start_var]
        agenda = [[start_var]]
        while agenda:
            path = agenda.pop(0)
            next_nodes = self.get_children(path[-1])
            if goal_var in next_nodes:
                return path + [goal_var]
            agenda.extend([path+[node] for node in next_nodes if node not in path])
        return None


    def subnet(self, subnet_variables):
        """Returns a new BayesNet that is a subnet of this one.  The new net
        includes the specified variables and any links that exist between them
        in the original Bayes net.  Ignores any specified variables that aren't
        in the original Bayes net."""
        new_net = self.copy()
        for var in self.variables:
            if var not in subnet_variables:
                new_net.remove_variable(var)
        return new_net


    def get_probability(self, hypothesis, parents_vals=None, infer_missing=True) :
        """Look up and return the conditional probability of var given its
        parents. If infer_missing is true, the function will infer missing CPT
        entries using the fact that certain probabilities sum to 1. Note that
        infer_missing only works for boolean variables.
        """
        parents_vals = parents_vals or {} #because gross things with mutable default args

        # allow only one hypothesis var
        if len(hypothesis) != 1 :
            raise ValueError, "Hypothesis must contain exactly one variable."

        var = hypothesis.keys()[0]
        if var not in self.variables:
            raise LookupError, str(var) + " is not a variable in this network."

        # check allowed values
        if set(parents_vals) != self.get_parents(var) :
            raise ValueError, "CPT entries must specify values for just the parents of " + var + "."

        explicit_probability = get(self.conditional_probability_table,
                                   (hypothesis, parents_vals))

        # infer probability if all other values are specified
        if explicit_probability is None and infer_missing :
            other_probabilities = [self.get_probability(d, parents_vals, False)
                                   for d in self.combinations([var])
                                   if d[var] != hypothesis[var]]
            if(all(other_probabilities)) :
                return reduce(lambda a,b : a - b, other_probabilities, 1)

        if explicit_probability is None:
            raise LookupError, "Unable to compute probability of " + str(hypothesis) + " given " + str(parents_vals)

        return explicit_probability


    def set_probability(self, hypothesis, parents_vals, p) :
        """Given a variable and a map of given vars to values, set the
        probability value of an entry in the conditional probability
        table.
        """
        # allow only one hypothesis var
        if len(hypothesis) != 1 :
            raise ValueError, "Hypothesis must contain exactly one variable."

        var = hypothesis.keys()[0]
        if var not in self.variables:
            raise LookupError, str(var)+" is not a variable in this network."

        if set(parents_vals.keys()) != self.get_parents(var) :
            raise ValueError, "CPT entries must specify values for just the parents of " + var + "."

        self.conditional_probability_table = assoc(
            self.conditional_probability_table,
            (hypothesis, parents_vals), p)
        return self



    def CPT_print(self, var=None) :
        """Pretty-prints the Bayes net's conditional probability table for var.
        If var is not specified, prints every conditional probability table."""
        if var==None:
            for v in self.variables:
                self.CPT_print(v)
            return

        parents = sorted(list(self.get_parents(var)))
        header = " | ".join(["%6s" % par for par in parents] + ["P("+var+")"])
        rows = filter(lambda row: row[0][0].keys()[0]==var,
                      self.conditional_probability_table)

        print header
        print "-" * len(header)
        if not rows:
            print '(No probabilities specified)\n'
            return
        for row in rows:
            parents_vals = row[0][1]
            prob = row[1]
            print " | ".join(["%6s" % str(parents_vals[par]) for par in parents]
                             + [str(prob)])
        print


    def set_domain(self, var, values) :
        """Establish the list of values that var can take on."""
        self.domain[var] = values[:]
        return self

    def get_domain(self, var) :
        return self.domain.get(var, (False, True))


    def combinations(self, variables, constant_bindings=None) :
        """Given a list of variables, returns a list of every possible binding
        of those variables.  Each variable included in constant_bindings will
        only appear with its specified binding.  Variables are assumed to be
        boolean except when specified otherwise using set_domain."""
        constant_bindings = constant_bindings or {}
        unbound_variables = filter(lambda v: v not in constant_bindings, variables)

        def asc(m,k,v):
            m2 = copy.deepcopy(m)
            m2[k] = v
            return m2

        def merge_dicts(m1,m2) :
            m = copy.deepcopy(m1)
            m.update(m2)
            return m

        def loop(agenda, partial_bindings=None) :
            partial_bindings = partial_bindings or [{}]
            if agenda and not agenda[0] in self.variables :
                raise ValueError(str(agenda[0])
                                 +" is not a variable in this network.")
            return partial_bindings if not agenda else \
                loop(agenda[1:],
                    [asc(d, agenda[0], val)
                     for d in partial_bindings
                     for val in self.get_domain(agenda[0])])

        return [merge_dicts(d,constant_bindings) for d in loop(unbound_variables)]


    def is_ordered(self, variables=None) :
        variables = self.variables if variables is None else variables
        return None is not reduce(lambda e, v : None if e is None or v in e else e + [v] +
                                  (lambda v : (lambda f:f(f,[v],[],[]))( lambda r,a,c,e : e if not a else r(r,a[1:],c,e) if a[0] in c else r(r,a[1:]+list(self.get_parents(a[0])),c+[a[0]],e+list(self.get_parents(a[0])))))(v), vars, [])


    def topological_sort(self, variables=None) :
        """Return a topologically sorted list of the variables, in which each
        node comes after its parents. (By default, uses the list of all
        variables.)"""
        variables = variables or self.variables

        # dfs takes a visited list, a path, and a one-node extension
        # of the path. To the visited list, it prepends a list
        # consisting of all the descendants of that path in
        # topological order.

        def dfs(visited, path, var) :
            if var not in visited :
                for y in self.get_children(var) :
                    visited= dfs(visited, path+[var],y)
                visited = [var] + visited
            return visited

        agenda = list(variables)
        visited = []
        while agenda :
            agenda = filter(lambda x: x not in visited,
                            agenda)
            if agenda :
                visited = dfs(visited, [], agenda[0])
        return visited

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        len_and_str = lambda x: tuple([fn(x) for fn in (len, str)])
        num_params = len(self.conditional_probability_table)
        return ('BayesNet with:'
                + '\n * %i variables: %s' % len_and_str(self.variables)
                + '\n * edges {parent: set([children])}: ' + str(self.adjacency)
                + '\n * %i conditional probabilities specified' % num_params
                + (' (use net.CPT_print() to view probabilities)'
                   if num_params else ''))

    __repr__ = __str__
