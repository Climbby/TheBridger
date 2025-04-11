class Probabilities():

    def __init__(self, state):
        self.state = state
        self.probabilitiesTable = self.setTable() 

    def setTable(self):
        if self.state["spot"] == "breakNexus":
            return {"breakEnemyNexus" : 100}
        else:
            return {"minutePass" : 100}