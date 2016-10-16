# MIT 6.034 Lab 4: Constraint Satisfaction Problems

# ConstraintSatisfactionProblem instances

# Note: Most of these problems are used in the tester, so don't change them.
# If you import these problems into your lab4.py, be sure to use .copy() to
# avoid mutating the original problems.

from constraint_api import *
CSP = ConstraintSatisfactionProblem

#########################################################

# Pokemon problem (2012 Q2)

pokemon_problem = ConstraintSatisfactionProblem(["Q1","Q2","Q3","Q4","Q5"])

pokemon_problem.set_domain("Q1",list("ABCE"))
pokemon_problem.set_domain("Q2",list("BCD"))
pokemon_problem.set_domain("Q3",list("BCD"))
pokemon_problem.set_domain("Q4",list("BCD"))
pokemon_problem.set_domain("Q5",list("ACE"))

pokemon_problem.add_constraint("Q1","Q4", constraint_different)
pokemon_problem.add_constraint("Q1","Q2", constraint_equal)
pokemon_problem.add_constraint("Q3","Q2", constraint_different)
pokemon_problem.add_constraint("Q3","Q4", constraint_different)
pokemon_problem.add_constraint("Q4","Q5", constraint_equal)

def get_pokemon_problem():
    return pokemon_problem.copy()

#########################################################

# New constraint functions
def constraint_or(var1, var2):
    return bool(var1 or var2)

# Constraint instances
cons_AB_different = Constraint('A', 'B', constraint_different)
cons_AB_equal = Constraint('A', 'B', constraint_equal)
cons_AB_or = Constraint('A', 'B', constraint_or)
cons_AC_different = Constraint('A', 'C', constraint_different)
cons_AC_equal = Constraint('A', 'C', constraint_equal)
cons_BC_different = Constraint('B', 'C', constraint_different)
cons_BC_equal = Constraint('B', 'C', constraint_equal)

#########################################################

# More past quiz questions

#2014f Triangle Problem
domains_triangle = {'A':[0,1], 'B':[0,1], 'C':[0,1,2]}
triangle_problem = CSP(list('ABC')).set_all_domains(domains_triangle) \
    .add_constraints([cons_AB_or, cons_AC_equal, cons_BC_equal])

triangle_problem_soln = triangle_problem.copy() \
    .set_assigned_values([('A',1), ('B',1), ('C',1)])

#2014f, starting with a smaller domain for C
triangle_problem_modified = triangle_problem.copy().set_domain('C',[1,2])
triangle_problem_modified_reduced = triangle_problem_modified.copy() \
    .set_all_domains({'A':[1], 'B':[1], 'C':[1]})


#########################################################

# Base triangle CSP instance
domains_ABC_default = {'A':[1,2,3], 'B':[1,2,3], 'C':[1,2,3]}
CSP_ABC = CSP(list('ABC')).set_all_domains(domains_ABC_default)

# Simple CSP instances for tests.py (triangle problems), using CSP_ABC
CSP_no_constraints = CSP_ABC.copy()

CSP_singleton = CSP_ABC.copy().set_domain('C',[3])

CSP_no_vars_assigned = CSP_ABC.copy().add_constraints([cons_AB_equal,
                                                       cons_BC_different])

CSP_no_vars_assigned_impossible_one_constraint = CSP_ABC.copy() \
    .add_constraints([cons_AB_equal]).set_domain('A',[1,2]).set_domain('B',[3])

CSP_one_var_assigned = CSP_ABC.copy().add_constraints([cons_AB_different]) \
    .set_assigned_value('A',2)

CSP_do_not_sort_queue = CSP_ABC.copy().add_constraints([cons_AB_different]) \
    .set_domain('B',[2]).set_domain('A',[1,2])
CSP_do_not_sort_queue_reduced = CSP_do_not_sort_queue.copy().set_domain('A',[1])

CSP_singleton_differentiate = CSP_one_var_assigned.copy() \
    .add_constraints([cons_AC_equal])
CSP_singleton_differentiate_reduced = CSP_singleton_differentiate.copy() \
    .set_domain('B',[1,3]).set_domain('C',[2])

CSP_one_var_assigned_unconstrained = CSP_ABC.copy() \
    .add_constraints([cons_AC_equal]).set_assigned_value('B',2)

CSP_some_vars_assigned_consistent = CSP_no_vars_assigned.copy() \
    .set_assigned_values([('B',3), ('C',1)])

CSP_all_vars_assigned_consistent = CSP_some_vars_assigned_consistent.copy() \
    .set_assigned_value('A',3)

CSP_all_vars_assigned_inconsistent = CSP_some_vars_assigned_consistent.copy() \
    .set_assigned_value('A',2)

CSP_impossible = CSP_ABC.copy().add_constraints([cons_AB_equal,
                                                 cons_AB_different,
                                                 cons_BC_equal])

CSP_some_vars_assigned_inconsistent = CSP_impossible.copy() \
    .set_assigned_values([('A',2), ('B',2)])

CSP_propany_not_prop1 = CSP_ABC.copy().set_domain('B', [2,3]).set_domain('A', [2]) \
    .add_constraints([cons_AC_different, cons_BC_equal])

CSP_propany_and_prop1 = CSP_ABC.copy().set_domain('A', [2]) \
    .add_constraints([cons_AC_equal, cons_BC_equal])

CSP_no_prop = CSP_propany_and_prop1.copy().set_domain('C', [2])


# More triangle problems for tests.py, with custom domains (not using CSP_ABC)
domains_no_soln = {'A':[0,1], 'B':[0,1], 'C':[0,1,2]}
CSP_no_soln = CSP(list('ABC')).set_all_domains(domains_no_soln) \
    .add_constraints([cons_AB_equal, cons_BC_different, cons_BC_equal])
CSP_no_soln_after_eliminate = CSP_no_soln.copy().set_domain('C',[])

domains_empty_domain = {'A':[1,2,3], 'B':[], 'C':[1,2,3,4]}
CSP_empty_domain = CSP(list('ABC')).set_all_domains(domains_empty_domain)
CSP_empty_domain_with_constraint = CSP_empty_domain.copy() \
    .add_constraints([cons_AB_equal]).set_assigned_value('A',2)

CSP_all_domains_empty = CSP(list('ABC')).set_all_domains({'A':[], 'B':[], 'C':[]})

domains_almost_stuck = {'A':[1,2,3], 'B':[1,2,3], 'C':[1,2,3]}
CSP_almost_stuck = CSP(list('ABC')).set_all_domains(domains_almost_stuck) \
    .add_constraints([cons_AB_equal, cons_BC_equal, cons_AC_different]) \
    .set_assigned_value('A',3)
CSP_almost_stuck_after_eliminate = CSP_almost_stuck.copy() \
    .set_domain('B',[3]).set_domain('C',[1,2])
CSP_now_stuck = CSP_almost_stuck_after_eliminate.copy().set_domain('C',[])

CSP_almost_stuck_singletons = CSP_almost_stuck.copy() \
    .set_all_domains({'A':[3], 'B':[3], 'C':[3]})

domains_B_nope = {'A':[1,2,3], 'B':[1,3], 'C':[1,2,3]}
CSP_B_nope = CSP(list('ABC')).set_all_domains(domains_B_nope) \
    .add_constraints([cons_AB_equal]).set_assigned_value('A',2)
CSP_B_nope_after_eliminate = CSP_B_nope.copy().set_domain('B',[])
