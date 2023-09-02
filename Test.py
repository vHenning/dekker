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
        if (len(list(g.successors(node))) == 0):
            if logging:
                print("Failed Deadlock Test: Found dead end (Process State " + node + ")")
            return False

    return True

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

    # Add connection from state2 back to state1. Now there is a circle, so no more dead ends
    g.add_edge(state2.toString(), state1.toString())

    # expect true
    result = testDeadlock(g, False)
    if (not result):
        print("Deadlock Unit Test Fail: Detected Deadlock where there should not be one (False Negative)")
        return False

    return True