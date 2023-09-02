import networkx as nx
import matplotlib.pyplot as plt

from ProcessState import ProcessState
import Test

# Test the tests
mutexUnitTestPass = Test.testMutex_unitTest()

print("Unit Test: Mutex: " + ("Passed" if mutexUnitTestPass else "Failed"))

if ((not mutexUnitTestPass)):
    exit(-1)

# Create a directed graph
g = nx.DiGraph()

# This is a recursive function.
# Makes sure the new process state is added properly to the process state graph.
# This includes all its children states (p progresses, q progresses)
# @param new New progress state
# @param parent Parent progress that produced new progress
# @param recursionCounter Not required, just for logging purposes
def newState(new: ProcessState, parent: ProcessState, recursionCounter=0):
    # Log recursion level
    recursionCounter += 1
    print("Recursion level " + str(recursionCounter))

    # If not already in graph, add node and its children
    if (not (new.toString() in g)):
        g.add_node(new.toString())
        newState(new.pStep(), new, recursionCounter)
        newState(new.qStep(), new, recursionCounter)

    # Add connection to parent in every case
    g.add_edge(parent.toString(), new.toString())

# Create our base state
state = ProcessState()
g.add_node(state.toString())

# Add its two children
print("Calculating first P step")
newState(state.pStep(), state)
print("Calculating first Q step")
newState(state.qStep(), state)

# Do the tests
mutexResult = Test.testMutex(g)
print("Mutex Test " + ("passed" if mutexResult else "failed"))

# Draw the graph
pos = nx.kamada_kawai_layout(g)
nx.draw(g, pos, with_labels=True, node_size=200, node_color="skyblue", font_size=5, font_color="black", arrows=True)

# Show the graph
plt.axis("off")
plt.show()
