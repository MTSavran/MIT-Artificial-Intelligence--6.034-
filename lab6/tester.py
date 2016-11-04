#!/usr/bin/env python2

# MIT 6.034 Lab 6: Neural Nets

import xmlrpclib
import traceback
import sys
import os
import tarfile

from neural_net_api import *
from lab6 import sigmoid, ReLU
from math import cos, e

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

python_version = sys.version_info
is_windows = sys.platform in ["win32", "cygwin"]
if python_version < (2, 3) or python_version >= (2, 8):
    raise Exception("Illegal version of Python for 6.034 lab. Detected Python "
                    + "version is: " + str(sys.version))
elif is_windows and python_version >= (2, 6, 5) and python_version < (2, 7, 4):
    raise Exception("Illegal version of Python for 6.034 lab. On Windows, "
        +"Python versions between 2.6.5 and 2.7.3 (inclusive) are incompatible "
        +"with our server. Detected Python version is: " + str(sys.version))

try:
    sys.path.append('..')
    from key import USERNAME as username, PASSWORD as password, XMLRPC_URL as server_url
except ImportError:
    print "Error: Can't find your 'key.py' file!  Please go download one from"
    print "<https://ai6034.mit.edu/labs/key.py>"
    sys.exit(1)

def test_summary(dispindex, ntests):
    return "Test %d/%d" % (dispindex, ntests)

def show_result(testsummary, testcode, correct, got, expected, verbosity):
    """ Pretty-print test results """
    if correct:
        if verbosity > 0:
            print "%s: Correct." % testsummary
        if verbosity > 1:
            print_testcode(testcode)
            print
    else:
        print "%s: Incorrect." % testsummary
        print_testcode(testcode)
        print "Got:     ", got, "\n"
        print "Expected:", expected, "\n"

def print_testcode(testcode):
    if isinstance(testcode, (tuple, list)) and len(testcode) >= 3:
        print '\t', testcode[2]
    else:
        print '\t', testcode

def show_exception(testsummary, testcode):
    """ Pretty-print exceptions (including tracebacks) """
    print "%s: Error." % testsummary
    print "While running the following test case:"
    print_testcode(testcode)
    print "Your code encountered the following error:"
    traceback.print_exc()
    print


def get_lab_module():
    # Try the easy way first
    try:
        from tests import lab_number as labnum
    except ImportError:
        labnum = None

    if labnum != None:
        lab = __import__('lab%s' % labnum)
    else:
        lab = None
        for labnum in xrange(10):
            try:
                lab = __import__('lab%s' % labnum)
                break
            except ImportError:
                pass

    if lab == None:
        raise ImportError, "Cannot find your lab; or, error importing it.  Try loading it by running 'python labN.py' (for the appropriate value of 'N')."

    if not hasattr(lab, "LAB_NUMBER"):
        lab.LAB_NUMBER = labnum

    return lab

# encode/decode objects
def encode_Wire(wire):
    return [wire.startNode, wire.endNode, wire.weight]
def decode_Wire(args):
    return Wire(*args)

def encode_NeuralNet(net):
    return [net.inputs, net.neurons, map(encode_Wire, net.wires)]
def decode_NeuralNet(inputs, neurons, wires_encoded):
    return NeuralNet(inputs, neurons, map(decode_Wire, wires_encoded))


# decode functions received from server
fns=[lambda x,y,z:5*x+3*y**3+cos(e-z**2),lambda x,y,z:y+z-x,lambda a,b,c:0,lambda a,b,c:c*a-b]
function_dict = {'sigmoid': sigmoid, 'ReLU': ReLU, 'fn0': fns[0], 'fn1': fns[1], 'fn2': fns[2], 'fn3': fns[3]}


def type_decode(arg, lab):
    """
    XMLRPC can only pass a very limited collection of types.
    Frequently, we want to pass a subclass of 'list' in as a test argument.
    We do that by converting the sub-type into a regular list of the form:
    [ 'TYPE', (data) ] (ie., AND(['x','y','z']) becomes ['AND','x','y','z']).
    This function assumes that TYPE is a valid attr of 'lab' and that TYPE's
    constructor takes a list as an argument; it uses that to reconstruct the
    original data type.
    """
    if isinstance(arg, dict):
        # hack to decode dictionary keys that were originally non-strings
        return {(-1 if k=='-1' else k):arg[k] for k in arg}
    if isinstance(arg, list) and len(arg) >= 1: # There is no future magic for tuples.
        if arg[0] == 'NeuralNet' and isinstance(arg[1], list):
            return decode_NeuralNet(*arg[1])
        if arg[0] == 'Wire' and isinstance(arg[1], list):
            return decode_Wire(arg[1])
        elif arg[0] == 'callable':
            try:
                return function_dict[arg[1]]
            except KeyError:
                error_string = "Error: invalid function name received from server: " + str(arg[1])
                print error_string + ". Please contact a TA if you continue to see this error."
                return error_string
        else:
            try:
                mytype = arg[0]
                data = arg[1:]
                return getattr(lab, mytype)([ type_decode(x, lab) for x in data ])
            except (AttributeError, TypeError):
                return [ type_decode(x, lab) for x in arg ]
    else:
        return arg


def is_class_instance(obj, class_name):
    return hasattr(obj, '__class__') and obj.__class__.__name__ == class_name

def type_encode(arg):
    "Encode objects as lists in a way that the server expects"
    if isinstance(arg, (list, tuple, set)): #note that tuples and sets become lists
        return [type_encode(a) for a in arg]
    elif is_class_instance(arg, 'NeuralNet'):
        return ['NeuralNet', encode_NeuralNet(arg)]
    elif is_class_instance(arg, 'Wire'):
        return ['Wire', encode_Wire(arg)]
    elif isinstance(arg, dict):
        # hack to prevent xmlrpclib TypeError "dictionary key must be string"
        return {str(k):arg[k] for k in arg}
    else:
        return arg


def run_test(test, lab):
    """
    Takes a 'test' tuple as provided by the online tester
    (or generated by the offline tester) and executes that test,
    returning whatever output is expected (the variable that's being
    queried, the output of the function being called, etc)

    'lab' (the argument) is the module containing the lab code.

    'test' tuples are in the following format:
      'id': A unique integer identifying the test
      'type': One of 'VALUE', 'FUNCTION', 'MULTIFUNCTION', or 'FUNCTION_ENCODED_ARGS'
      'attr_name': The name of the attribute in the 'lab' module
      'args': a list of the arguments to be passed to the function; [] if no args.
      For 'MULTIFUNCTION's, a list of lists of arguments to be passed in
    """
    id, mytype, attr_name, args = test

    attr = getattr(lab, attr_name)

    if mytype == 'VALUE':
        return attr
    elif mytype == 'FUNCTION':
        return apply(attr, args)
    elif mytype == 'MULTIFUNCTION':
        return [ run_test( (id, 'FUNCTION', attr_name, FN), lab)
                for FN in type_decode(args, lab) ]
    elif mytype == 'FUNCTION_ENCODED_ARGS':
        return run_test( (id, 'FUNCTION', attr_name, type_decode(args, lab)), lab )
    else:
        raise Exception("Test Error: Unknown TYPE: " + str(mytype)
                        + ".  Please make sure you have downloaded the latest"
                        + "version of the tester script.  If you continue to "
                        + "see this error, contact a TA.")


def test_offline(verbosity=1):
    """ Run the unit tests in 'tests.py' """
    import tests as tests_module

    tests = tests_module.get_tests()
    ntests = len(tests)
    ncorrect = 0

    for index, (testname, getargs, testanswer, expected, fn_name, type) in enumerate(tests):
        dispindex = index+1
        summary = test_summary(dispindex, ntests)

        try:
            if callable(getargs):
                getargs = getargs()

            answer = run_test((index, type, fn_name, getargs), get_lab_module())
        except NotImplementedError:
            print "%d: (%s: Function not yet implemented, NotImplementedError raised)" % (dispindex, testname)
            continue
        except Exception:
            show_exception(summary, testname)
            continue

        # This prevents testanswer from throwing errors. eg, if return type is
        # incorrect, testanswer returns False instead of raising an exception.
        try:
            correct = testanswer(answer)
        except NotImplementedError:
            print "%d: (%s: No answer given, NotImplementedError raised)" % (dispindex, testname)
            continue
        except (KeyboardInterrupt, SystemExit): # Allow user to interrupt tester
            raise
        except Exception:
            #raise   # To debug tests by allowing them to raise exceptions, uncomment this
            correct = False

        show_result(summary, testname, correct, answer, expected, verbosity)
        if correct: ncorrect += 1

    print "Passed %d of %d tests." % (ncorrect, ntests)
    return ncorrect == ntests

def get_target_upload_filedir():
    """ Get, via user prompting, the directory containing the current lab """
    cwd = os.getcwd() # Get current directory.  Play nice with Unicode pathnames, just in case.

    print "Please specify the directory containing your lab,"
    print "or press Enter to use the default directory."
    print "Note that all files from this directory will be uploaded!"
    print "Labs should not contain large amounts of data; very-large"
    print "files will fail to upload."
    print
    print "The default path is '%s'" % cwd
    target_dir = raw_input("[%s] >>> " % cwd)

    target_dir = target_dir.strip()
    if target_dir == '':
        target_dir = cwd

    print "Ok, using '%s'." % target_dir

    return target_dir

def get_tarball_data(target_dir, filename):
    """ Return a binary String containing the binary data for a tarball of the specified directory """
    print "Preparing the lab directory for transmission..."

    data = StringIO()
    tar = tarfile.open(filename, "w|bz2", data)

    top_folder_name = os.path.split(target_dir)[1]

    def tar_filter(filename):
        """Returns True if we should tar the file.
        Avoid uploading .pyc files or the .git subdirectory (if any)"""
        if filename == ".git":
            return False
        if os.path.splitext(filename)[1] == ".pyc":
            return False
        return True

    def add_dir(currentDir, t_verbose=False):
        for currentFile in os.listdir(currentDir):
            fullPath=os.path.join(currentDir,currentFile)
            if t_verbose:
                print currentFile,
            if tar_filter(currentFile):
                if t_verbose:
                    print ""
                tar.add(fullPath,arcname=fullPath.replace(target_dir, top_folder_name,1),recursive=False)
                if os.path.isdir(fullPath):
                    add_dir(fullPath)
            elif t_verbose:
                print "....skipped"

    add_dir(target_dir)

    print "Done."
    print
    print "The following files have been added:"

    for f in tar.getmembers():
        print f.name

    tar.close()

    return data.getvalue()


def test_online(verbosity=1):
    """ Run online unit tests.  Run them against the 6.034 server via XMLRPC. """
    lab = get_lab_module()

    try:
        server = xmlrpclib.Server(server_url, allow_none=True)
        tests = server.get_tests(username, password, lab.__name__)
    except NotImplementedError: # Solaris Athena doesn't seem to support HTTPS
        print "Your version of Python doesn't seem to support HTTPS, for"
        print "secure test submission.  Would you like to downgrade to HTTP?"
        print "(note that this could theoretically allow a hacker with access"
        print "to your local network to find your 6.034 password)"
        answer = raw_input("(Y/n) >>> ")
        if len(answer) == 0 or answer[0] in "Yy":
            server = xmlrpclib.Server(server_url.replace("https", "http"))
            tests = server.get_tests(username, password, lab.__name__)
        else:
            print "Ok, not running your tests."
            print "Please try again on another computer."
            print "Linux Athena computers are known to support HTTPS,"
            print "if you use the version of Python in the 'python' locker."
            sys.exit(0)
    except xmlrpclib.Fault:
        print "\nError: Either your key.py file is out of date, or online "
        print "tests for " + lab.__name__ + " are not currently available."
        print "If you believe this is may be a mistake, please contact a TA.\n"
        sys.exit(0)

    ntests = len(tests)
    ncorrect = 0

    lab = get_lab_module()

    target_dir = get_target_upload_filedir()

    tarball_data = get_tarball_data(target_dir, "lab%s.tar.bz2" % lab.LAB_NUMBER)

    print "Submitting to the 6.034 Webserver..."

    server.submit_code(username, password, lab.__name__, xmlrpclib.Binary(tarball_data))

    print "Done submitting code."
    print "Running test cases..."

    for index, testcode in enumerate(tests):
        dispindex = index+1
        summary = test_summary(dispindex, ntests)

        try:  # Prevent errors from interrupting test execution
            answer = run_test(testcode, get_lab_module())
            correct, expected = server.send_answer(username, password, lab.__name__, testcode[0], type_encode(answer))
            show_result(summary, testcode, correct, answer, expected, verbosity)
            if correct: ncorrect += 1
        except Exception:
            show_exception(summary, testcode)
            continue

    response = server.status(username, password, lab.__name__)
    print response


def make_test_counter_decorator():
    tests = []
    def make_test(getargs, testanswer, expected_val, name = None, type = 'FUNCTION'):
        if name != None:
            getargs_name = name
        elif not callable(getargs):
            getargs_name = "_".join(getargs[:-8].split('_')[:-1])
            getargs = lambda: getargs
        else:
            getargs_name = "_".join(getargs.__name__[:-8].split('_')[:-1])

        tests.append( ( getargs_name,
                        getargs,
                        testanswer,
                        expected_val,
                        getargs_name,
                        type ) )

    def get_tests():
        return tests

    return make_test, get_tests


make_test, get_tests = make_test_counter_decorator()


if __name__ == '__main__':
    if 'submit' in sys.argv:
        test_online()
    elif test_offline():
        if "IDLE" in sys.executable:
            print "submitting and testing online..."
            test_online()
        else:
            print "Local tests passed! Run 'python %s submit' to submit your code and have it graded." % sys.argv[0]
