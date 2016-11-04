# MIT 6.034 Lab 5: k-Nearest Neighbors and Identification Trees

from api import *

################################################################################
############################# IDENTIFICATION TREES #############################
################################################################################
IDTNode = IdentificationTreeNode

# 2014 Q2: Oak or Maple?
tree_data = [\
    {"name":"Tree1", "tree_type":"Oak", "has_leaves":"Yes", "orange_foliage":"Yes", "leaf_shape":"Pointy", "bark_texture":"Glossy"},
    {"name":"Tree2", "tree_type":"Oak", "has_leaves":"Yes", "orange_foliage":"No", "leaf_shape":"Pointy", "bark_texture":"Furrowed"},
    {"name":"Tree3", "tree_type":"Oak", "has_leaves":"Yes", "orange_foliage":"No", "leaf_shape":"Rounded", "bark_texture":"Furrowed"},
    {"name":"Tree4", "tree_type":"Maple", "has_leaves":"Yes", "orange_foliage":"Yes", "leaf_shape":"Pointy", "bark_texture":"Furrowed"},
    {"name":"Tree5", "tree_type":"Maple", "has_leaves":"Yes", "orange_foliage":"Yes", "leaf_shape":"Pointy", "bark_texture":"Smooth"},
    {"name":"Tree6", "tree_type":"Maple", "has_leaves":"Yes", "orange_foliage":"No", "leaf_shape":"Pointy", "bark_texture":"Smooth"}
]

tree_data_furrowed = [\
    {"name":"Tree2", "tree_type":"Oak", "has_leaves":"Yes", "orange_foliage":"No", "leaf_shape":"Pointy", "bark_texture":"Furrowed"},
    {"name":"Tree3", "tree_type":"Oak", "has_leaves":"Yes", "orange_foliage":"No", "leaf_shape":"Rounded", "bark_texture":"Furrowed"},
    {"name":"Tree4", "tree_type":"Maple", "has_leaves":"Yes", "orange_foliage":"Yes", "leaf_shape":"Pointy", "bark_texture":"Furrowed"},
]

tree_data_furrowed_pointy = [\
    {"name":"Tree2", "tree_type":"Oak", "has_leaves":"Yes", "orange_foliage":"No", "leaf_shape":"Pointy", "bark_texture":"Furrowed"},
    {"name":"Tree4", "tree_type":"Maple", "has_leaves":"Yes", "orange_foliage":"Yes", "leaf_shape":"Pointy", "bark_texture":"Furrowed"},
]

tree_classifiers = [\
    feature_test("bark_texture"),
    feature_test("has_leaves"),
    feature_test("leaf_shape"),
    feature_test("orange_foliage"),
]

_ft_tt = feature_test("tree_type")
_ft_class = feature_test("class")
_ft_Classification = feature_test("Classification")

#manually encode greedy ID tree for classifying trees
def get_tree_tree():
    tree = IDTNode(_ft_tt)._ssc(tree_classifiers[0], tree_data)
    branches = tree.get_branches()
    branches["Glossy"].set_node_classification("Oak")
    branches["Smooth"].set_node_classification("Maple")
    subnode = branches["Furrowed"]._ssc(tree_classifiers[3], tree_data_furrowed)
    subbranches = subnode.get_branches()
    subbranches["Yes"].set_node_classification("Maple")
    subbranches["No"].set_node_classification("Oak")
    return tree

def get_tree_tree_impossible():
    tree = IDTNode(_ft_tt)._ssc(tree_classifiers[0], tree_data)
    branches = tree.get_branches()
    branches["Glossy"].set_node_classification("Oak")
    branches["Smooth"].set_node_classification("Maple")
    subnode = branches["Furrowed"]._ssc(tree_classifiers[2], tree_data_furrowed)
    subbranches = subnode.get_branches()
    subbranches["Rounded"].set_node_classification("Oak")
    return tree

tree_classifiers_reverse = [\
    feature_test("has_leaves"),
    feature_test("leaf_shape"),
    feature_test("orange_foliage"),
    feature_test("tree_type"),
]

tree_test_point = {"name":"Tree7", "has_leaves":"Yes", "orange_foliage":"Yes", "leaf_shape":"Rounded", "bark_texture":"Furrowed"}


# Test what happens if it's not possible to complete the tree
tree_classifiers_impossible = [\
    feature_test("bark_texture"),
    feature_test("has_leaves"),
    feature_test("leaf_shape"),
]


# 2012 Q2: Angel or Not Angel?

angel_data = [\
    {"name":"Statue1", "Classification":"Angel", "Height":7, "Shape":"Human", "Material":"Stone"},
    {"name":"Statue2", "Classification":"Angel", "Height":2.5, "Shape":"Human", "Material":"Stone"},
    {"name":"Statue3", "Classification":"Not Angel", "Height":7, "Shape":"Human", "Material":"Copper"},
    {"name":"Statue4", "Classification":"Not Angel", "Height":3, "Shape":"Animal", "Material":"Copper"},
    {"name":"Statue5", "Classification":"Not Angel", "Height":8, "Shape":"Animal", "Material":"Stone"},
    {"name":"Statue6", "Classification":"Angel", "Height":305, "Shape":"Human", "Material":"Copper"},
]

angel_classifiers = [\
    feature_test("Shape"),
    threshold_test("Height", 7),
    feature_test("Material"),
]

_branches_yesno = ["No","Yes"]

# manually encode greedy ID tree
def get_angel_tree():
    tree = IDTNode(_ft_Classification)._ssc(angel_classifiers[0], angel_data)
    branches = tree.get_branches()

    branches["Animal"].set_node_classification("Not Angel")
    branches = branches["Human"].set_classifier_and_expand(angel_classifiers[2], ["Stone","Copper"]).get_branches()

    branches["Stone"].set_node_classification("Angel")
    branches = branches["Copper"].set_classifier_and_expand(angel_classifiers[1], _branches_yesno).get_branches()

    branches["No"].set_node_classification("Not Angel")
    branches["Yes"].set_node_classification("Angel")
    return tree

# 2013 Q2: Numeric ID tree

numeric_pre_data = {\
    "A": [(0.5, 1.5), (1.5, 0.5), (1.5, 1.5), (2.5, 0.5), (2.5, 2.5), (3.5, 0.5)],
    "B": [(0.5, 3.5), (2.5, 1.5), (3.5, 2.5)]
}
numeric_data0 = [[{"name":str((x,y)), "class":A_or_B, "X":x, "Y":y}
                  for (x,y) in points]
                 for (A_or_B, points) in numeric_pre_data.items()]
numeric_data = numeric_data0[0] + numeric_data0[1]

numeric_classifiers = [\
    threshold_test("X", 1),
    threshold_test("X", 2),
    threshold_test("X", 3),
    threshold_test("Y", 1),
    threshold_test("Y", 2),
    threshold_test("Y", 3),
]

# manually encode greedy ID tree
def get_numeric_tree():
    tree = IDTNode(_ft_class)._ssc(numeric_classifiers[3], numeric_data)
    branches = tree.get_branches()

    branches["No"].set_node_classification("A")
    branches = branches["Yes"].set_classifier_and_expand(numeric_classifiers[2],_branches_yesno).get_branches()

    branches["Yes"].set_node_classification("B")
    branches = branches["No"].set_classifier_and_expand(numeric_classifiers[5],_branches_yesno).get_branches()

    branches["Yes"].set_node_classification("B")
    branches = branches["No"].set_classifier_and_expand(numeric_classifiers[1],_branches_yesno).get_branches()

    branches["No"].set_node_classification("A")
    branches = branches["Yes"].set_classifier_and_expand(numeric_classifiers[4],_branches_yesno).get_branches()

    branches["No"].set_node_classification("B")
    branches["Yes"].set_node_classification("A")

    return tree

# toy data for ID trees
toy_data_1 = [\
    {"name":"toypoint1", "class":1, "attr1":2, "attr2":4, "attr3":6},
    {"name":"toypoint2", "class":-1, "attr1":3, "attr2":5, "attr3":7}
]

toy_classifiers_1 = [\
    feature_test("attr2"),
    feature_test("attr1"),
    feature_test("attr3"),
]

toy_data_2 = [\
    {"name":"p1", "class":"A", "flavor":"vanilla"},
    {"name":"p2", "class":"B", "flavor":"vanilla"},
    {"name":"p3", "class":"C", "flavor":"vanilla"},
    {"name":"p4", "class":"D", "flavor":"chocolate"},
    {"name":"p5", "class":"A", "flavor":"chocolate"},
    {"name":"p6", "class":"B", "flavor":"chocolate"},
]

toy_classifiers_2 = [feature_test("flavor")]

# binary XOR data and trees
binary_pre_data = [\
    (1,0,0,0,0),
    (2,0,0,0,1),
    (3,1,0,1,0),
    (4,1,0,1,1),
    (5,1,1,0,1),
    (6,1,1,0,1),
    (7,0,1,1,0),
]
binary_data = [{"name":"point"+str(i), "Classification":s, "A":a, "B":b, "C":c}
               for (i,s,a,b,c) in binary_pre_data]

binary_classifiers = [feature_test("A"), feature_test("B"), feature_test("C")]
(bcA, bcB, bcC) = binary_classifiers

_branches_01=[0,1]

def get_binary_tree_1():
    tree = IDTNode(_ft_Classification)._ssc(bcB, binary_data)
    branches = tree.get_branches()

    branches[1].set_node_classification(1)
    branches = branches[0].set_classifier_and_expand(bcA,_branches_01).get_branches()

    branches[0].set_node_classification(0)
    branches[1].set_node_classification(1)
    return tree

def get_binary_tree_2():
    tree = IDTNode(_ft_Classification)._ssc(bcA, binary_data)
    branches = tree.get_branches()

    branches0 = branches[0].set_classifier_and_expand(bcB,_branches_01).get_branches()
    branches1 = branches[1].set_classifier_and_expand(bcB,_branches_01).get_branches()

    branches0[0].set_node_classification(0)
    branches0[1].set_node_classification(1)
    branches1[0].set_node_classification(1)
    branches1[1].set_node_classification(0)
    return tree

def get_binary_tree_3():
    tree = IDTNode(_ft_Classification)._ssc(bcC, binary_data)
    branches = tree.get_branches()

    branches0 = branches[0].set_classifier_and_expand(bcA,_branches_01).get_branches()
    branches1 = branches[1].set_classifier_and_expand(bcA,_branches_01).get_branches()

    branches0[1].set_node_classification(0)
    branches00 = branches0[0].set_classifier_and_expand(bcB,_branches_01).get_branches()
    branches00[0].set_node_classification(0)
    branches00[1].set_node_classification(1)

    branches1[1].set_node_classification(1)
    branches10 = branches1[0].set_classifier_and_expand(bcB,_branches_01).get_branches()
    branches10[0].set_node_classification(0)
    branches10[1].set_node_classification(1)
    return tree

binary_tree_1 = get_binary_tree_1()
binary_tree_2 = get_binary_tree_2()
binary_tree_3 = get_binary_tree_3()

################################################################################
############################# k-NEAREST NEIGHBORS ##############################
################################################################################

# 2014 Q2: Oak or Maple?
knn_tree_data = [\
    Point((10,5), "Oak"),
    Point((20,15), "Oak"),
    Point((20,40), "Oak"), #outlier
    Point((30,20), "Oak"),
    Point((40,30), "Oak"),
    Point((5,10), "Maple"),
    Point((10,15), "Maple"),
    Point((20,30), "Maple"),
    Point((25,40), "Maple"),
]

knn_tree_test_point = Point((25,32))

# toy data for knn
knn_toy_data = [\
    Point([3], "A"),
    Point([3], "B"),
    Point([3], "B"),
    Point([3], "C"),
    Point([3], "D"),
]
