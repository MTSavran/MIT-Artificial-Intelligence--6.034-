# MIT 6.034 Lab 1: Rule-Based Systems
# Written by 6.034 staff

from production import IF, AND, OR, NOT, THEN, DELETE, forward_chain
from data import *

#### Part 1: Multiple Choice #########################################

ANSWER_1 = '2'

ANSWER_2 = '4'

ANSWER_3 = '2'

ANSWER_4 = '0'

ANSWER_5 = '3'

ANSWER_6 = '1'

ANSWER_7 = '0'

#### Part 2: Transitive Rule #########################################

# transitive_rule = IF( AND(), THEN() )

transitive_rule = IF( AND( '(?x) beats (?y)',
                           '(?y) beats (?z)'),
                      THEN( '(?x) beats (?z)') )

# You can test your rule by uncommenting these print statements:
#print forward_chain([transitive_rule], abc_data)
#print forward_chain([transitive_rule], poker_data)
#print forward_chain([transitive_rule], minecraft_data)


#### Part 3: Family Relations #########################################

# Define your rules here:

# Add your rules to this list:
family_rules = [ IF( 'person (?x)',
                     THEN('self (?x) (?x)') ),

                 IF( AND('parent (?p) (?x)',
                         'parent (?p) (?y)',
                         NOT('self (?x) (?y)')),
                     THEN('sibling (?x) (?y)') ),

                 IF ( 'sibling (?x) (?y)',
                      THEN('sibling (?y) (?x)') ),

                 IF(   'parent (?y) (?x)',
                     THEN('child (?x) (?y)') ),

                 IF( AND('parent (?p) (?x)',
                         'parent (?q) (?y)',
                         'sibling (?p) (?q)',
                          NOT('sibling (?x) (?y)')),
                     THEN('cousin (?x) (?y)') ),

                 IF ( 'cousin (?x) (?y)',
                      THEN('cousin (?y) (?x)')),

                 IF( AND('parent (?x) (?p)',
                         'parent (?p) (?y)'),
                     THEN('grandparent (?x) (?y)') ),
                 IF ( AND('parent (?y) (?p)',
                          'parent (?p) (?x)'),
                      THEN('grandchild (?x) (?y)') )]

# Uncomment this to test your data on the Simpsons family:
#print forward_chain(family_rules, simpsons_data, verbose=False)

# These smaller datasets might be helpful for debugging:
#print forward_chain(family_rules, sibling_test_data, verbose=True)
#print forward_chain(family_rules, grandparent_test_data, verbose=True)

# The following should generate 14 cousin relationships, representing 7 pairs
# of people who are cousins:
black_family_cousins = [
    relation for relation in
    forward_chain(family_rules, black_data, verbose=False)
    if "cousin" in relation ]

# To see if you found them all, uncomment this line:
#print black_family_cousins


#### Part 4: Backward Chaining #########################################

# Import additional methods for backchaining
from production import PASS, FAIL, match, populate, simplify, variables

# def backchain_to_goal_tree(rules, hypothesis):
#     """
#     Takes a hypothesis (string) and a list of rules (list
#     of IF objects), returning an AND/OR tree representing the
#     backchain of possible statements we may need to test
#     to determine if this hypothesis is reachable or not.

#     This method should return an AND/OR tree, that is, an
#     AND or OR object, whose constituents are the subgoals that
#     need to be tested. The leaves of this tree should be strings
#     (possibly with unbound variables), *not* AND or OR objects.
#     Make sure to use simplify(...) to flatten trees where appropriate.
#     """
#     raise NotImplementedError

def backchain_to_goal_tree(rules, hypothesis):
    
    length = len(rules) 

    if length==0:
        return hypothesis
    tree = OR()
    
    for element in rules:
        con = element.consequent()
        mat = match(con[0], hypothesis)
        if mat is not None and len(mat)>=0:
            antec = element.antecedent()
            if isinstance(antec, list):
                sub = AND()
                if isinstance(antec, OR): sub = OR()
                for x in antec:
                    new_tree = backchain_to_goal_tree(rules, populate(x, mat))
                    sub.append(new_tree)
                tree.append(sub)
            else:
                new_tree = backchain_to_goal_tree(rules, populate(antec, mat))
                tree.append(AND(new_tree))
        else:
            tree.append(hypothesis)
    new = simplify(tree)
    return new

# Uncomment this to run your backward chainer:
#print backchain_to_goal_tree(zookeeper_rules, 'opus is a penguin')


#### Survey #########################################

NAME = "MEHMET TUGRUL SAVRAN"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 2.5
WHAT_I_FOUND_INTERESTING = "Backward Chaining"
WHAT_I_FOUND_BORING = "Nothing!"
SUGGESTIONS = "I really liked this pset!"


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the tester. DO NOT CHANGE!
transitive_rule_poker = forward_chain([transitive_rule], poker_data)
transitive_rule_abc = forward_chain([transitive_rule], abc_data)
transitive_rule_minecraft = forward_chain([transitive_rule], minecraft_data)
family_rules_simpsons = forward_chain(family_rules, simpsons_data)
family_rules_black = forward_chain(family_rules, black_data)
family_rules_sibling = forward_chain(family_rules, sibling_test_data)
family_rules_grandparent = forward_chain(family_rules, grandparent_test_data)
family_rules_anonymous_family = forward_chain(family_rules, anonymous_family_test_data)
