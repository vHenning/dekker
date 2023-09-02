import copy

class ProcessState:
    def __init__(self):
        self.pWants = False
        self.qWants = False
        self.turn = 1

        # Yes, we do start counting at 1 to be consistent with lecture notes
        self.pProgramCounter = 1
        self.qProgramCounter = 1

    # Returns the next process state if p's program counter advances.
    # Returns the same process state if p cannot advance
    def pStep(self):
        newState = copy.deepcopy(self)
        if (self.pProgramCounter == 1):
            newState.pProgramCounter = 2
        if (self.pProgramCounter == 2):
            newState.pProgramCounter = 3
            newState.pWants = True
        if (self.pProgramCounter == 3):
            if (self.qWants == True):
                newState.pProgramCounter = 4
            else:
                newState.pProgramCounter = 8
        if (self.pProgramCounter == 4):
            if (self.turn == 2):
                newState.pProgramCounter = 5
            else:
                newState.pProgramCounter = 3
        if (self.pProgramCounter == 5):
            newState.pProgramCounter = 6
            newState.pWants = False
        if (self.pProgramCounter == 6):
            if (self.turn == 1):
                newState.pProgramCounter = 7
        if (self.pProgramCounter == 7):
            newState.pProgramCounter = 3
            newState.pWants = True
        if (self.pProgramCounter == 8):
            newState.pProgramCounter = 9
        if (self.pProgramCounter == 9):
            newState.pProgramCounter = 10
            newState.turn = 2
        if (self.pProgramCounter == 10):
            newState.pProgramCounter = 1
            newState.pWants = False
        return newState

    # Returns the next process state if q's program counter advances.
    # Returns the same process state if q cannot advance
    def qStep(self):
        newState = copy.deepcopy(self)
        if (self.qProgramCounter == 1):
            newState.qProgramCounter = 2
        if (self.qProgramCounter == 2):
            newState.qProgramCounter = 3
            newState.qWants = True
        if (self.qProgramCounter == 3):
            if (self.pWants == True):
                newState.qProgramCounter = 4
            else:
                newState.qProgramCounter = 8
        if (self.qProgramCounter == 4):
            if (self.turn == 1):
                newState.qProgramCounter = 5
            else:
                newState.qProgramCounter = 3
        if (self.qProgramCounter == 5):
            newState.qProgramCounter = 6
            newState.qWants = False
        if (self.qProgramCounter == 6):
            if (self.turn == 2):
                newState.qProgramCounter = 7
        if (self.qProgramCounter == 7):
            newState.qProgramCounter = 3
            newState.qWants = True
        if (self.qProgramCounter == 8):
            newState.qProgramCounter = 9
        if (self.qProgramCounter == 9):
            newState.qProgramCounter = 10
            newState.turn = 1
        if (self.qProgramCounter == 10):
            newState.qProgramCounter = 1
            newState.qWants = False
        return newState

    def boolToString(self, bool):
        if (bool == True):
            return "t"
        if (bool == False):
            return "f"

        raise ValueError("Did not get Bool!")

    # Returns a unique string for this process state
    def toString(self):
        return "P" + "{:02d}".format(self.pProgramCounter) + " Q" + "{:02d}".format(self.qProgramCounter) + " " + self.boolToString(self.pWants) + self.boolToString(self.qWants) + str(self.turn)
