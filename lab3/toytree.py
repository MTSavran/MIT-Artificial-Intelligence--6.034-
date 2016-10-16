# MIT 6.034 Lab 3: Games

from game_api import *
from copy import deepcopy

class ToyTree :
    def __init__(self, label=None, score=None) :
        self.score = score
        self.label = label
        self.children = []
        self.zipper = []
        self.sibling_index = None
        # sibling index records how many left siblings this node has.

        self.sibling = None

    def __eq__(self, other) :
        return [self.score, self.label, self.children, self.zipper] == [other.score, other.label, other.children, other.zipper]

    def __str__(self, tab=0) :
        ret = ""
        for x in self.children :
            ret += x.__str__(tab+1)
        ret = ("-" * 3 * tab) + (" " * (tab > 0) ) +  (self.label or "node") + ("("+str(self.score)+")" if self.score is not None else "") + "\n" + ret
        return ret

    def copy(self):
        return deepcopy(self)

    def describe_previous_move(self) :
                return "Took branch "+str(self.sibling_index) if self.sibling_index is not None else "[none]"

    def get_score(self) :
        return self.score

    def set_score(self, score) :
        self.score = score
        return self

    def append(self, child) :
        """Append a ToyTree child node to the end of the list of children."""
        child.zipper = []
        child.sibling_index = len(self.children)
        self.children.append(child)
        if len(self.children) > 1 :
            self.children[-2].sibling = child
        return self

    def sub(self, label=None, value=None) :
        return self.append(ToyTree(label, value))

    def is_leaf(self) :
        return not self.children


    # moving around
    def down(self) :
        """Visit the first child."""
        child = self.children[0]
        child.zipper = self.zipper + [self]
        return child

    def up(self) :
        """Visit parent."""
        parent = self.zipper[-1]
        parent.zipper = self.zipper[:-1]
        return parent

    def right(self) :
        """Visit sibling."""
        assert self.sibling
        self.sibling.zipper = self.zipper
        return self.sibling

    def top(self) :
        """Visit root."""
        if self.zipper :
            return self.zipper[0]
        else :
            return self



def create_toy_tree(name_to_score, nested_list) :
    """Creates a ToyTree from two inputs:
    1. a dict mapping node names to scores, eg {"A":3, "B":2}
    2. a nested list of node names. A well-formed nested list is a pair whose
    first element is a node name, and whose second element is a (possibly empty)
    list containing well-formed nested lists, each of which represents a subtree.
    If a node is not in the the input dict, its score is assumed to be 0.
    """
    label, sublists = nested_list
    root = ToyTree(label, name_to_score.get(label, 0))
    children = [create_toy_tree(name_to_score, sublist) for sublist in sublists]
    for child in children:
        root.append(child)
    return root

    # OR EQUIVALENTLY:
#    return reduce(lambda parent, child : parent.append(child),
#                   map(lambda x : create_toy_tree(score_dict, x), nested_list[1]),
#                   ToyTree(nested_list[0], score_dict.get(nested_list[0])))

def wrapper_toytree(score_dict, nested_list) :
    tree = create_toy_tree(score_dict, nested_list)
    return AbstractGameState(snapshot = tree,
                             is_game_over_fn = toytree_is_game_over,
                             generate_next_states_fn = toytree_generate_next_states,
                             endgame_score_fn = toytree_endgame_score)


# TREE FOR ALL SEARCHES
tree4 = ToyTree()
tree4.sub().sub().sub().sub()
tree4.down().sub(None,7).sub(None,11).sub(None, 3).sub(None, 10)
tree4.down().right().sub(None,4).sub(None,9).sub(None, 14).sub(None, 8)
tree4.down().right().right().sub(None,5).sub(None,2).sub(None, 12).sub(None, 16)
tree4.down().right().right().right().sub(None,15).sub(None,6).sub(None, 1).sub(None, 3)

# If max goes first, 4 is the minimax score, and alpha-beta prunes 3 nodes.
# If min goes first, 11 is the minimax score, and alpha-beta prunes 5 nodes.
# [[[7],[11],[3],[10]],[[4],[9],[14],[8]], [[5],[2],[12],[16]], [[15],[6],[1],[13]]]

def toytree_is_game_over(tree) :
    return tree.children == []

def toytree_generate_next_states(tree) :
    return tree.children

def toytree_endgame_score_fn(tree, is_current_player_maximizer) :
    return tree.score


GAME1 = AbstractGameState(tree4,
                          toytree_is_game_over,
                          toytree_generate_next_states,
                          toytree_endgame_score_fn)




def toytree_heuristic_fn(tree, is_current_player_maximizer) :
    return tree.score


# 2013 final part 1D
tree5 = ToyTree("A",10) # static values at all levels
tree5.sub("B",11).sub("C",2).sub("D",3).sub("E",6)
tree5.down().sub("F",10).sub("G",12)
tree5.down().down().right().sub("K",7).sub("L",11)
tree5.down().right().sub("H",9).sub("I",12)
tree5.down().right().down().right().sub("M",12).sub("N",13)
tree5.down().right().right().right().sub("J",7).down().sub("O",8)

GAME_STATIC_ALL_LEVELS = AbstractGameState(tree5,
                                           toytree_is_game_over,
                                           toytree_generate_next_states,
                                           toytree_endgame_score_fn)

tree6 = ToyTree("A")
tree6.sub("B").sub("C")
tree6.down().sub("D").sub("E")
tree6.down().right().sub("F").sub("G")
tree6.down().down().sub("H").sub("I")
tree6.down().down().right().sub("J").sub("K")
tree6.down().right().down().sub("L").sub("M")
tree6.down().right().down().right().sub("N")
tree6.down().down().down().sub("O",3).sub("P",17)
tree6.down().down().down().right().sub("Q",2).sub("R",12)
tree6.down().down().right().down().sub("S",15)
tree6.down().down().right().down().right().sub("T",25).sub("U",0)
tree6.down().right().down().down().sub("V",2).sub("W",5)
tree6.down().right().down().down().right().sub("X",3)
tree6.down().right().down().right().down().sub("Y",2).sub("Z",14)

# A tree that checks exit condition of alpha = beta.
GAME_EQUALITY_PRUNING = AbstractGameState(tree6,
                         toytree_is_game_over,
                         toytree_generate_next_states,
                         toytree_endgame_score_fn)

