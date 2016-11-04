# MIT 6.034 Lab 5: k-Nearest Neighbors and Identification Trees

from api import *

features = [\
    "Age", #int
    "Sex", #M or F
    "Chest pain type", #typical angina, atypical angina, non-anginal pain, asymptomatic (note angina = chest pain)
    "Resting blood pressure", #int
    "Cholesterol level", #int
    "Is fasting blood sugar < 120 mg/dl", #Yes or No
    "Resting EKG type", #normal, wave abnormality, ventricular hypertrophy
    "Maximum heart rate", #int
    "Does exercise cause chest pain?", #Yes or No
    "ST depression induced by exercise", #int
    "Slope type", #up, flat, down
    "# of vessels colored", #float, ?
    "Thal type", #normal, fixed defect, reversible defect, unknown
    "Heart disease presence", #healthy or diseased
    "Heart disease level", #int 0 (healthy, no presence) to 4
]

intify = lambda s: int(float(s))

heart_training_data = []
patient_number = 1

with open('cleveland_medical_data.txt') as f:
    for line in f:
        if (not line) or line[0] in "\n\r\n" or line[0] == "%":
            continue
        values = line.strip("\n\r").split()
        if len(values) < 15:
            print 'Error: line shorter than expected; skipping line...'
            continue
        person = {}
        person["name"] = "patient" + str(patient_number)
        person["Age"] = intify(values[0]) #int (in years)
        person["Sex"] = {"male":"M", "fem":"F"}[values[1]] #M or F
        person["Chest pain type"] = {"angina":"typical angina", "abnang":"atypical angina",
                                     "notang":"non-anginal pain", "asympt":"asymptomatic"}[values[2]]
                                     #typical angina, atypical angina, non-anginal pain, asymptomatic (note angina = chest pain)
        person["Resting blood pressure"] = intify(values[3]) #int (in mm Hg)
        person["Cholesterol level"] = intify(values[4]) #int (in mg/dl)
        person["Is fasting blood sugar < 120 mg/dl"] = {"true":"Yes", "fal":"No"}[values[5]] #Yes or No
        person["Resting EKG type"] = {"norm":"normal", "abn":"wave abnormality",
                                      "hyp":"ventricular hypertrophy"}[values[6]]
                                      #normal, wave abnormality, ventricular hypertrophy
        person["Maximum heart rate"] = intify(values[7]) #int
        person["Does exercise cause chest pain?"] = {"true":"Yes", "fal":"No"}[values[8]] #Yes or No
        person["ST depression induced by exercise"] = intify(values[9]) #int "ST depression induced by exercise relative to rest"
        person["Slope type"] = values[10] #up, flat, down
        person["# of vessels colored"] = "?" if values[11] == "?" else float(values[11]) #float or ? #number of major vessels (0-3) colored by flourosopy
        person["Thal type"] = {"norm":"normal", "fix":"fixed defect", "rev":"reversible defect", "?":"unknown"}[values[12]]
            #normal, fixed defect, reversible defect, unknown
        person["Heart disease presence"] = {"buff":"healthy", "sick":"diseased"}[values[13]] #healthy or diseased
        person["Heart disease level"] = {"H":0, "S1":1, "S2":2, "S3":3, "S4":4}[values[14]] #int 0 (healthy, no presence) to 4
        heart_training_data.append(person)
        patient_number += 1


heart_classifiers = [\
    feature_test(features[1]),
    feature_test(features[2]),
    feature_test(features[5]),
    feature_test(features[6]),
    feature_test(features[8]),
    feature_test(features[10]),
    feature_test(features[12]),
]

def threshold_test_with_unknown(feature, threshold) :
    def classify_function(pt):
        val = pt.get(feature)
        if val == '?':
            return '?'
        if maybe_number(val) > threshold:
            return 'Yes'
        return 'No'
    return Classifier(feature + " > " + str(threshold) + " (or ?)", classify_function)

def all_midpoint_tests(feature_name, data):
    """Creates threshold tests for the feature, one for each midpoint value.
    If '?' is a value, creates 3-option threshold tests with Yes/No/?.
    Returns a list of Classifier objects."""
    test_making_fn = threshold_test
    tests = []
    values = sorted(set([p[feature_name] for p in data]))
    if '?' in values:
        values.remove('?')
        test_making_fn = threshold_test_with_unknown
    for (v1,v2) in zip(values[:-1], values[1:]):
        tests.append(test_making_fn(feature_name, (v1+v2)/2.))
    return tests

heart_classifiers.extend(all_midpoint_tests(features[0], heart_training_data))
heart_classifiers.extend(all_midpoint_tests(features[3], heart_training_data))
heart_classifiers.extend(all_midpoint_tests(features[4], heart_training_data))
heart_classifiers.extend(all_midpoint_tests(features[7], heart_training_data))
heart_classifiers.extend(all_midpoint_tests(features[9], heart_training_data))
heart_classifiers.extend(all_midpoint_tests(features[11], heart_training_data))


heart_target_classifier_binary = feature_test(features[13])
heart_target_classifier_discrete = feature_test(features[14])


# If you want to try using k-nearest neighbors on this data, uncomment the lines
# below.  Note that one of the numeric features (# of vessels colored) is not
# included due to the possible '?' value.  Also note that you'll probably need
# to normalize the data for each feature, e.g. by dividing by the standard
# deviation of that feature's values, in order to get results that consider
# all features relatively equally.

#knn_heart_training_data = []
#numeric_features = [features[i] for i in [0,3,4,7,9]] #note: feature 11 (# of vessels colored) not included due to non-numeric '?'
#for person in heart_training_data:
#    point = Point([person[attr] for attr in numeric_features], #todo: normalize data for each feature
#                  classification=person[features[13]], #or 14 for discrete classification
#                  name=person['name'])
#    knn_heart_training_data.append(point)
#
##print knn_heart_training_data[-1] #uncomment to print a sample Point


################################################################################
################################################################################

# ANSWERS TO QUESTIONS FROM LAB 5 WIKI PAGE:

# Q: Does this seem like the simplest possible tree?  If not, why not?
# A: No, it is probably overfitting and giving too much weight to outliers in
#    the data.  For example, many leaf nodes correspond to only 1-2 patients.

# Q: What could we change to make the tree simpler?
# A: One possible change is to modify the stopping condition.  Rather than
#    continuing to add classifiers until the data is perfectly separated, we
#    could stop when a node reaches some homogeneity threshold, such as 90%,
#    then assign the node the classification of the majority of the points.
#    This method would reduce overfitting, although in the extreme case, it
#    could result in underfitting (e.g. if you use a threshold of 51%, or 90%
#    but with a very small dataset).

# Q: What do you notice when you print the training data at the leaf nodes?
# A: One interesting observation is that there are many nodes that have only a
#    few training points, while there are a few nodes that have a large number
#    of training points.  The nodes with many training points are probably
#    reliable classifications, but those with few training points may be
#    misleading results due to overfitting.

# Q: Try using the other target classifier (binary or discrete).  Is the tree
#    simpler or more complicated?  Why?
# A: The binary-classification tree is simpler because it doesn't need to
#    separate the data as much.  The discrete-classification tree is more
#    complicated because nodes that contain only diseased patients don't count
#    as homogeneous if those patients have different levels of heart disease.

# Q: Try creating and classifying a few patients.  Are the results consistent
#    with your expectations?
# A: Expectations may vary, of course, but we've found that, in general,
#    patients who seem healthy (normal values for all features, as in the sample
#    test_patient) get classified as 'healthy', and patients who seem unhealthy
#    get classified as 'diseased'.  However, there are some exceptions...

# Q: What happens if a female patient has 'Thal type': 'unknown'?
# A: She gets classified as healthy (or 0) because the first test in the ID tree
#    is 'Thal type', and the first (and only) test for 'unknown' is 'Sex', with
#    'F' indicating healthy/0.

# Q: What happens if a male patient has 'Thal type': 'unknown'?
# A: He gets classified as diseased (or 2) because the first test in the ID tree
#    is 'Thal type', and the first (and only) test for 'unknown' is 'Sex', with
#    'M' indicating diseased/2.

# Q: What causes the surprising result with 'Thal type': 'unknown'?
# A: There are only two patients in the data set with 'Thal type': 'unknown'.
#    It just happens that one is female and healthy, while the other is male and
#    diseased.  This is an excellent example of overfitting.

# Q: What could we change to improve the classification accuracy of patients
#    with unknown Thal type?
# A: There are many possible changes, including (1) gather more data on patients
#    with unknown Thal type, or (2) ignore the 'Thal type' test altogether and
#    construct a tree using the remaining tests.

# Q: In the discrete classification tree, what happens if a patient has:
#        'Thal type': 'normal',
#        'Chest pain type': 'asymptomatic',
#        '# of vessels colored': '?'
#    ...and why does it happen?
# A: The first test in the ID tree is 'Thal type', the first test for 'normal'
#    is 'Chest pain type', and the first test for 'asymptomatic' is '# of
#    vessels colored > 0.5 (or ?)', but that node (# vessels) has only two
#    branches, 'Yes' and 'No', so the patient with '?' cannot be classified.
#    This problem arises because all of the patients in the training data with
#    'Thal type': 'normal' and 'Chest pain type': 'asymptomatic' also had a
#    known number of vessels colored (not '?').

# Q: Why might the issue with '# of vessels colored': '?' cause a problem for
#    classifying real patients?  What can we do to fix this issue?
# A: Many patients, especially healthy ones, may not have undergone the
#    procedure for determining how many major vessels are colored by flourosopy,
#    and it would be nice to be able to classify them without that information.
#    As with the 'Thal type' problem, solutions include (1) gathering more
#    information on patients with an unknown number of vessels colored, or (2)
#    ignoring the test altogether.  A third option is to assign these patients
#    the classification corresponding to the majority of patients who have 'Thal
#    type': 'normal' and 'Chest pain type': 'asymptomatic' (in this case,
#    healthy/0).
