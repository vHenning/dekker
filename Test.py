import copy
import networkx as nx
from ProcessState import ProcessState

######################## Actual Tests ##############################################

# Tests mutual exclusion. Fails if graph contains process states that have both processes in the critical section
# @param g Graph whose nodes shall be checked for mutex violations
# @param logging Set false if you only want to get the return value without any logging output
# @return True if there are no mutex violations, False otherwise
def testMutex(g: nx.DiGraph, logging=True):
    for node in g.nodes:
        # Processes must not be in the critical section at the same time
        if (node.find("P08 Q08") != -1):
            if logging:
                print("Failed Mutex Test: Process State " + node)
            return False
    return True

# Tests deadlocks. Fails if graph contains dead ends (Deadlocks)
# @param g Graph whose nodes shall be checked for deadlocks
# @param logging Set false if you only want to get the return value without any logging output
# @return True if there are no deadlocks, False otherwise
def testDeadlock(g: nx.DiGraph, logging=True):
    for node in g.nodes:
        successors = list(g.successors(node))
        if (len(successors) == 0):
            if logging:
                print("Failed Deadlock Test: Found dead end (Process State " + node + ")")
            return False
        else:
            if (len(successors) == 1 and successors[0] == node):
                if logging:
                    print("Failed Deadlock Test: Found process state looping itself (Process State " + node + ")")
                return False

    return True

# Tests starvation. Fails if graph contains branches in which one process tries to
# get into the critical section (reaches P/Q2) but never gets access (never reaches P/Q8).
# @param g Graph whose nodes shall be checked for starvation
# @param logging Set false if you only want to get the return value without any logging output
# @return True if there is no starvation, False otherwise
def testStarvation(g: nx.DiGraph, logging=True):
    for node in g.nodes:
        if (node.find("P02") != -1):
            # P must eventually reach P8 (critical section) in one successor branch
            if (not reachesCriticalSection(g, node, "P08")):
                if logging:
                    print("Failed Starvation Test: Found pWants state that cannot result in a P8 state (Process State " + node + ")")
                return False
        if (node.find("Q02") != -1):
            # Q must eventually reach Q8 (critical section) in one successor branch
            if (not reachesCriticalSection(g, node, "P08")):
                if logging:
                    print("Failed Starvation Test: Found qWants state that cannot result in a Q8 state (Process State " + node + ")")
                return False

    return True

# Checks if given node or its successors in given graph reach the critical section defined by the critical trigger.
# @param g Graph containing node and its successors
# @param node Current node to check for critical section
# @param criticalTrigger String indicating critical section (e.g. P8)
# @param predecessors Not required, only used internally because this is a recursive function
# @return True if the critical section is reached, False otherwise
def reachesCriticalSection(g: nx.DiGraph, node: str, criticalTrigger: str, predecessors=set()):
    # We must create our own copy of predecessors because we do not want the next successor
    # in the for loop a few lines down from here to know about all predecessors of this function call
    newSet = copy.deepcopy(predecessors)
    newSet.add(node)

    # Check if this node is the critical section
    if (node.find(criticalTrigger) != -1):
        return True

    # Check if we checked this node already (in this case we are moving in a circle without having found the crit. sect.)
    if (node in predecessors):
        return False

    for successor in g.successors(node):
        if (reachesCriticalSection(g, successor, criticalTrigger, newSet)):
            return True

    # At this point we did not find any successors that reach the critical section (probably a dead end)
    return False

######################## Unit Tests (testing the tests) ############################

def testMutex_unitTest():
    g = nx.DiGraph()

    # Add state that does not violate mutex
    normalState = ProcessState()
    g.add_node(normalState.toString())

    # expect true
    if (not testMutex(g, False)):
        print("Mutex Unit Test Fail: Detected Mutex violation where there should not be one (False Positive)")
        return False

    # Add state that does violate mutex
    mutexState = ProcessState()
    mutexState.pProgramCounter = 8
    mutexState.qProgramCounter = 8
    g.add_node(mutexState.toString())

    # expect false
    if (testMutex(g, False)):
        print("Mutex Unit Test Fail: Did not detect Mutex violation (False Negative)")
        return False

    return True

def testDeadlock_unitTest():
    g = nx.DiGraph()

    # Add two states
    state1 = ProcessState()
    state2 = state1.pStep()

    g.add_node(state1.toString())
    g.add_node(state2.toString())

    # Only add one connection. This results in state2 not having any successors (dead end)
    g.add_edge(state1.toString(), state2.toString())

    # expect false
    result = testDeadlock(g, False)
    if (result):
        print("Deadlock Unit Test Fail: Did not detect Deadlock (False Positive)")
        return False

    # Add connection from last node to itself. This is still a deadlock.
    g.add_edge(state2.toString(), state2.toString())

    # expect false
    result = testDeadlock(g, False)
    if (result):
        print("Deadlock Unit Test Fail: Did not detect Deadlock (False Positive)")
        return False

    # Add connection from state2 back to state1. Now there is a circle, so no more dead ends
    g.add_edge(state2.toString(), state1.toString())

    # expect true
    result = testDeadlock(g, False)
    if (not result):
        print("Deadlock Unit Test Fail: Detected Deadlock where there should not be one (False Negative)")
        return False

    return True

def testStarvation_unitTest():
    g = nx.DiGraph()

    # For the first test we create two nodes with one connection (--> dead end)
    state1 = ProcessState()
    state2 = state1.pStep()

    g.add_node(state1.toString())
    g.add_node(state2.toString())
    g.add_edge(state1.toString(), state2.toString())

    # expect false
    result = testStarvation(g, False)
    if (result):
        print ("Starvation Unit Test Fail: Did not detect Starvation (False Positive)")
        return False

    # Now we add a second connection to create a circle. The test must still fail because we did not add a P8 state
    g.add_edge(state2.toString(), state1.toString())

    # expect false
    result = testStarvation(g, False)
    if (result):
        print ("Starvation Unit Test Fail: Did not detect Starvation (False Positive)")
        return False

    # Now we add the desired critical section. It is a dead end but we are not testing for that here
    state3 = ProcessState()
    state3.pProgramCounter = 8
    g.add_node(state3.toString())
    g.add_edge(state2.toString(), state3.toString())

    # expect true
    result = testStarvation(g, False)
    if (not result):
        print ("Starvation Unit Test Fail: Detected Starvation where there is none (False Negative)")
        return False

    return True