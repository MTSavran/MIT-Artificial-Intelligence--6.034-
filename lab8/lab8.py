# MIT 6.034 Lab 8: Bayesian Inference
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from nets import *


#### ANCESTORS, DESCENDANTS, AND NON-DESCENDANTS ###############################

def get_ancestors(net, var):
    "Return a set containing the ancestors of var"
    ancestors = set()
    q = [var]
    while len(q)!=0:
        var = q.pop(0)
        for parent in net.get_parents(var):
            if parent not in ancestors:
                ancestors.add(parent)
                q.append(parent)
    return ancestors

def get_descendants(net, var):
    "Returns a set containing the descendants of var"
    descendants = set()
    q = [var]
    while len(q)!=0:
        var = q.pop(0)
        for child in net.get_children(var):
            if child not in descendants:
                descendants.add(child)
                q.append(child)
    return descendants

def get_nondescendants(net, var):
    "Returns a set containing the non-descendants of var"
    nondescendants = set()
    descendants = get_descendants(net,var)
    for variable in net.topological_sort():
        if variable not in descendants:
            nondescendants.add(variable)
    nondescendants.remove(var)
    return nondescendants

def simplify_givens(net, var, givens):
    """If givens include every parent of var and no descendants, returns a
    simplified list of givens, keeping only parents.  Does not modify original
    givens.  Otherwise, if not all parents are given, or if a descendant is
    given, returns original givens."""
    givenset = set(givens)
    parents = net.get_parents(var)
    descendants = get_descendants(net,var)
    if parents.issubset(givenset) and givenset.isdisjoint(descendants):
        nondescendants = get_nondescendants(net,var)
        copy = dict(givens)
        for key in givens:
            if key not in parents:
                del copy[key]
        
        return copy
    else:
        return givens



#### PROBABILITY ###############################################################

def probability_lookup(net, hypothesis, givens=None):
    "Looks up a probability in the Bayes net, or raises LookupError"

    if givens is not None:
        if len(hypothesis) > 1:
            raise LookupError
        else:
            newgivens = simplify_givens(net,hypothesis.keys()[0],givens)
            try:
                return net.get_probability(hypothesis, newgivens)
            except (ValueError, LookupError) as e:
                raise LookupError
    else:
        if len(hypothesis) > 1:
            raise LookupError
        else:
            try:
                return net.get_probability(hypothesis)
            except (ValueError,LookupError) as e:
                raise LookupError
        

def probability_joint(net, hypothesis):
    "Uses the chain rule to compute a joint probability"
    toposorted = net.topological_sort()
    toposorted = toposorted[::-1]
    givens = dict(hypothesis)
    p = 1 
    for variable in toposorted:
        if variable in hypothesis:
            del givens[variable]
            p = p*probability_lookup(net,{variable:hypothesis[variable]},givens)
    return p 

def probability_marginal(net, hypothesis):
    "Computes a marginal probability as a sum of joint probabilities"

    combinations = net.combinations(net.get_variables(),hypothesis)
    prob = 0 
    for combination in combinations:
        prob += probability_joint(net,combination)
    return prob

def probability_conditional(net, hypothesis, givens=None):
    "Computes a conditional probability as a ratio of marginal probabilities"
    if givens == hypothesis:
        return 1 
    for variable in hypothesis:
        if givens != None:
            if variable in givens:
                if hypothesis[variable] != givens[variable]:
                    return 0 
    if givens != None:
        d3 = dict(hypothesis,**givens)
        return float(probability_marginal(net,d3))/float(probability_marginal(net,givens))
    else: 
        return float(probability_marginal(net,hypothesis))/float(probability_marginal(net,givens))



def probability(net, hypothesis, givens=None):
    "Calls previous functions to compute any probability"
    return probability_conditional(net,hypothesis,givens)

#### PARAMETER-COUNTING AND INDEPENDENCE #######################################

def number_of_parameters(net):
    "Computes minimum number of parameters required for net"
    reslist = []
    variables = net.get_variables()
    for variable in variables: 
        val = 1 
        variablesoptions = len(net.get_domain(variable))-1
        for parent in net.get_parents(variable):
            parentoptions = len(net.get_domain(parent))
            val *= parentoptions
        reslist.append(variablesoptions*val)
    return sum(reslist)

def is_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    otherwise False.  Uses numerical independence."""

    for combination in net.get_domain(var1):
        for combination2 in net.get_domain(var2):

            if givens != None:
                d3 = dict({var2: combination2},**givens)
                prob1 = probability(net,{var1:combination},d3) 
            else:
                prob1 = probability(net,{var1:combination},{var2:combination2}) 

            prob2 = probability(net,{var1:combination},givens)

            if not approx_equal(prob1, prob2):
                return False

    return True

def is_structurally_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    based on the structure of the Bayes net, otherwise False.
    Uses structural independence only (not numerical independence)."""




    #ANCESTRAL GRAPH
    tobeadded = set()
    ancestors1 = get_ancestors(net, var1)
    ancestors1.add(var1)
    ancestors2 = get_ancestors(net,var2)
    ancestors2.add(var2)
    ancestors1.update(ancestors2)

    tobeadded.update(ancestors1)
    if givens != None:
        tobeadded.update(givens)


    if givens != None:
        for given in givens:
            if net.find_path(var1,given) != None:
                tobeadded.update(net.find_path(var1,given))
            if net.find_path(var2,given) != None:
                tobeadded.update(net.find_path(var2,given))
    

    newnet = net.subnet(tobeadded)
    copy = newnet.copy()
    #MORALIZE GRAPH

    copytoposort = copy.topological_sort()

    copytoposort = copytoposort[::-1]

    visited = set()
    for variable in copytoposort:
        q = [variable]
        visited.add(variable)
        while len(q)!=0:
            var = q.pop(0)
            parents = list(copy.get_parents(var))
            if len(parents) > 1:
                for i in range(len(parents)):
                    for j in range(i):
                        if parents[i] not in visited and parents[j] not in visited:
                            newnet.link(parents[i], parents[j])
                            visited.add(parents[i])
                            visited.add(parents[j])
                            q.append(parents[i])
                            q.append(parents[j])

    #MAKE BIDIRECTIONAL
    newnet.make_bidirectional()

    #REMOVE GIVENS
    if givens != None:
        for given in givens:
            if given in newnet.get_variables():
                newnet.remove_variable(given)

    #CHECK IF VAR1 AND VAR2 ARE CONNECTED
    if newnet.find_path(var1,var2) == None:
        return True
    return False
       

#### SURVEY ####################################################################

NAME = "Mehmet Tugrul Savran"
COLLABORATORS = "None"
HOW_MANY_HOURS_THIS_LAB_TOOK = "8"
WHAT_I_FOUND_INTERESTING = "Everything except is structurally independent"
WHAT_I_FOUND_BORING = "Structurally independent part"
SUGGESTIONS = "Happy thanksgiving!"
