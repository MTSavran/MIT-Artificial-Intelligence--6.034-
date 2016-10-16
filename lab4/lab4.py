# MIT 6.034 Lab 4: Constraint Satisfaction Problems
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from constraint_api import *
from test_problems import get_pokemon_problem
import itertools



#### PART 1: WRITE A DEPTH-FIRST SEARCH CONSTRAINT SOLVER

def has_empty_domains(csp) :
    "Returns True if the problem has one or more empty domains, otherwise False"
    variables = csp.variables
    for variable in variables:
        if len(csp.get_domain(variable)) == 0:
            return True
    return False

def check_all_constraints(csp) :
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""
    constraints = csp.get_all_constraints()
    values = csp.assigned_values
    for c in constraints:
        v1 = c.var1
        v2 = c.var2
        if v1 in values and v2 in values:
            if c.check(values[v1],values[v2])==False:
                return False
    return True

    # for c in constraints:
    #     for value in




def solve_constraint_dfs(problem) :
    """Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values), and
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple."""
    count = 0 
    agenda = [problem]
    while agenda:
        prob = agenda.pop(0)
        count += 1
        values = prob.assigned_values

        if has_empty_domains(prob) or not(check_all_constraints(prob)):
            continue

        if check_all_constraints(prob):

            if len(prob.unassigned_vars)==0:
                return(prob.assigned_values,count)
            else:
                nextvar = prob.pop_next_unassigned_var()
                nextdomain = prob.get_domain(nextvar)
                listofnews = []
                for element in nextdomain:
                        copyprob = prob.copy()
                        newproblem = copyprob.set_assigned_value(nextvar, element)
                        listofnews.append(newproblem)
                agenda = listofnews + agenda

    return(None,count)

#### PART 2: DOMAIN REDUCTION BEFORE SEARCH

def eliminate_from_neighbors(csp, var) :
    """Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
    If a domain is reduced to size 0, quits immediately and returns None."""

    #values = csp.assigned_values
    neighbors = csp.get_neighbors(var)
    result = set()
    for n in neighbors:
        li = []
        for nval in csp.get_domain(n):
            r = 0

            for val in csp.get_domain(var):
                a = []
                for c in csp.constraints_between(var,n):
                    a.append(c.check(val,nval))
                    
                if all(a) == True:
                    r = 1

            if r ==0:
                li.append(nval)


        if li: #Meaning it violated  all
#remove nval from n's domain
            for i in li:
                csp.eliminate(n,i)
                result.add(n)
            if not(csp.get_domain(n)):
                return None


    result = sorted(result)
    return result



def domain_reduction(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    If queue is None, initializes propagation queue by adding all variables in
    their default order.  Returns a list of all variables that were dequeued,
    in the order they were removed from the queue.  Variables may appear in the
    list multiple times.
    If a domain is reduced to size 0, quits immediately and returns None."""
    dequeued = []
    if queue is None:
        q = csp.get_all_variables()
    else:
        q = queue
    while q:
        var = q.pop(0)
        dequeued.append(var)
        liste = eliminate_from_neighbors(csp,var)
        if liste:
            for neighbor in liste:
                if neighbor not in q:
                    q.append(neighbor)
        if liste is None:
            return None
        
    return dequeued

# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DON'T use domain reduction before solving it?

# Hint: Use get_pokemon_problem() to get a new copy of the Pokemon problem
#    each time you want to solve it with a different search method.
print solve_constraint_dfs(get_pokemon_problem())
ANSWER_1 = 20

# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DO use domain reduction before solving it?
d =  (get_pokemon_problem())
#domain_reduction(d)
print solve_constraint_dfs(d)
ANSWER_2 = 6


#### PART 3: PROPAGATION THROUGH REDUCED DOMAINS

def solve_constraint_propagate_reduced_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs."""
    count = 0 
    agenda = [problem]
    while agenda:
        prob = agenda.pop(0)
        count += 1
        values = prob.assigned_values

        if has_empty_domains(prob) or not(check_all_constraints(prob)):
            continue

        if check_all_constraints(prob):

            if len(prob.unassigned_vars)==0:
                return(prob.assigned_values,count)
            else:
                nextvar = prob.pop_next_unassigned_var()
                nextdomain = prob.get_domain(nextvar)
                listofnews = []
                for element in nextdomain:
                        copyprob = prob.copy()
                        newproblem = copyprob.set_assigned_value(nextvar, element)
                        domain_reduction(newproblem,[nextvar])
                        listofnews.append(newproblem)
                agenda = listofnews + agenda

    return(None,count)

# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with propagation through reduced domains? (Don't use domain reduction
#    before solving it.)

ANSWER_3 = solve_constraint_propagate_reduced_domains(get_pokemon_problem())[1]
print ANSWER_3
#### PART 4: PROPAGATION THROUGH SINGLETON DOMAINS

def domain_reduction_singleton_domains(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Only propagates through singleton domains.
    Same return type as domain_reduction."""
    dequeued = []
    if queue is None:
        q = csp.get_all_variables()
    else:
        q = queue
    while q:
        var = q.pop(0)
        dequeued.append(var)
        liste = eliminate_from_neighbors(csp,var)
        #print csp
        if has_empty_domains(csp):
            return None
        if liste:
            for neighbor in liste:
                # if len(csp.get_domain(neighbor)) == 0:
                #     return None
                if neighbor not in q:
                    if len(csp.get_domain(neighbor)) == 1:
                        q.append(neighbor)

    return dequeued

def solve_constraint_propagate_singleton_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through singleton domains.  Same return type as
    solve_constraint_dfs."""
    count = 0 
    agenda = [problem]
    while agenda:
        prob = agenda.pop(0)
        count += 1
        values = prob.assigned_values

        if has_empty_domains(prob) or not(check_all_constraints(prob)):
            continue

        if check_all_constraints(prob):

            if len(prob.unassigned_vars)==0:
                return(prob.assigned_values,count)
            else:
                nextvar = prob.pop_next_unassigned_var()
                nextdomain = prob.get_domain(nextvar)
                listofnews = []
                for element in nextdomain:
                        copyprob = prob.copy()
                        newproblem = copyprob.set_assigned_value(nextvar, element)
                        domain_reduction_singleton_domains(newproblem,[nextvar])
                        listofnews.append(newproblem)
                agenda = listofnews + agenda

    return(None,count)


# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with propagation through singleton domains? (Don't use domain reduction
#    before solving it.)

ANSWER_4 = solve_constraint_propagate_singleton_domains(get_pokemon_problem())[1]


#### PART 5: FORWARD CHECKING

def propagate(enqueue_condition_fn, csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced.  Same return type as domain_reduction."""
    dequeued = []
    if queue is None:
        q = csp.get_all_variables()
    else:
        q = queue
    while q:
        var = q.pop(0)
        dequeued.append(var)
        liste = eliminate_from_neighbors(csp,var)
        #print csp
        if has_empty_domains(csp):
            return None
        if liste:
            for neighbor in liste:
                # if len(csp.get_domain(neighbor)) == 0:
                #     return None
                if neighbor not in q:
                    if enqueue_condition_fn(csp,neighbor):
                        q.append(neighbor)

    return dequeued

def condition_domain_reduction(csp, var) :
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    return True

def condition_singleton(csp, var) :
    """Returns True if var should be enqueued under the singleton-domains
    condition, otherwise False"""
    leng = csp.get_domain(var)
    if len(leng) ==1:
        return True
    else: 
        return False


def condition_forward_checking(csp, var) :
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    return False


#### PART 6: GENERIC CSP SOLVER

def solve_constraint_generic(problem, enqueue_condition=None) :
    """Solves the problem, calling propagate with the specified enqueue
    condition (a function).  If enqueue_condition is None, uses DFS only.
    Same return type as solve_constraint_dfs."""
    count = 0 
    agenda = [problem]
    while agenda:
        prob = agenda.pop(0)
        count += 1
        values = prob.assigned_values

        if has_empty_domains(prob) or not(check_all_constraints(prob)):
            continue

        if check_all_constraints(prob):

            if len(prob.unassigned_vars)==0:
                return(prob.assigned_values,count)
            else:
                nextvar = prob.pop_next_unassigned_var()
                nextdomain = prob.get_domain(nextvar)
                listofnews = []
                for element in nextdomain:
                        copyprob = prob.copy()
                        newproblem = copyprob.set_assigned_value(nextvar, element)
                        if enqueue_condition is not None:
                            propagate(enqueue_condition,newproblem,[nextvar])
                        listofnews.append(newproblem)
                agenda = listofnews + agenda

    return(None,count)


# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking, but no propagation? (Don't use domain
#    reduction before solving it.)

ANSWER_5 = solve_constraint_generic(get_pokemon_problem(), condition_forward_checking)[1]


#### PART 7: DEFINING CUSTOM CONSTRAINTS

def constraint_adjacent(m, n) :
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    if abs(m-n) == 1:
        return True
    return False

def constraint_not_adjacent(m, n) :
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    if abs(m-n) == 1:
        return False
    return True

def all_different(variables) :
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    # liste = []
    # print variables
    # for i in range(len(variables)):
    #     if i+1==len(variables):
    #         break
    #     new = Constraint(variables[i],variables[i+1],constraint_different)
    #     liste.append(new)
    # return liste
    kume = set(itertools.combinations(variables, 2))

    liste = list(kume)
    result = []
    for i in liste:
        result.append(Constraint(i[0],i[1],constraint_different))
    return result

#### PART 8: MOOSE PROBLEM (OPTIONAL)

moose_problem = ConstraintSatisfactionProblem(["You", "Moose", "McCain",
                                               "Palin", "Obama", "Biden"])

# Add domains and constraints to your moose_problem here:


# To test your moose_problem AFTER implementing all the solve_constraint
# methods above, change TEST_MOOSE_PROBLEM to True:
TEST_MOOSE_PROBLEM = False


#### SURVEY ###################################################

NAME = "Mehmet Tugrul Savran"
COLLABORATORS = "None"
HOW_MANY_HOURS_THIS_LAB_TOOK = 8
WHAT_I_FOUND_INTERESTING = "All different function"
WHAT_I_FOUND_BORING = "Debugging"
SUGGESTIONS = "None"


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

if TEST_MOOSE_PROBLEM:
    # These lines are used in the local tester iff TEST_MOOSE_PROBLEM is True
    moose_answer_dfs = solve_constraint_dfs(moose_problem.copy())
    moose_answer_propany = solve_constraint_propagate_reduced_domains(moose_problem.copy())
    moose_answer_prop1 = solve_constraint_propagate_singleton_domains(moose_problem.copy())
    moose_answer_generic_dfs = solve_constraint_generic(moose_problem.copy(), None)
    moose_answer_generic_propany = solve_constraint_generic(moose_problem.copy(), condition_domain_reduction)
    moose_answer_generic_prop1 = solve_constraint_generic(moose_problem.copy(), condition_singleton)
    moose_answer_generic_fc = solve_constraint_generic(moose_problem.copy(), condition_forward_checking)
    moose_instance_for_domain_reduction = moose_problem.copy()
    moose_answer_domain_reduction = domain_reduction(moose_instance_for_domain_reduction)
    moose_instance_for_domain_reduction_singleton = moose_problem.copy()
    moose_answer_domain_reduction_singleton = domain_reduction_singleton_domains(moose_instance_for_domain_reduction_singleton)
