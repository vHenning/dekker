class ProcessState:
    def __init__(self):
        self.pWants = False
        self.qWants = False
        self.turn = 1

        # Yes, we do start counting at 1 to be consistent with lecture notes
        self.pProgramCounter = 1
        self.qProgramCounter = 1

    def boolToString(self, bool):
        if (bool == True):
            return "t"
        if (bool == False):
            return "f"

        raise ValueError("Did not get Bool!")

    # Returns a unique string for this process state
    def toString(self):
        return "P" + "{:02d}".format(self.pProgramCounter) + " Q" + "{:02d}".format(self.qProgramCounter) + " " + self.boolToString(self.pWants) + self.boolToString(self.qWants) + str(self.turn)
