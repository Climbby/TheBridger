from commands.game.data.playerStats import players

class Probabilities():

    def __init__(self, state, user, events):
        self.state = state
        self.user = user
        self.events = events
        self.changePerMinute = None
        self.probabilitiesTable = None

    async def setTable(self):

        probabilitiesTable = self.checkPlace()
        await self.checkSpot(probabilitiesTable)
        self.probabilitiesTable = probabilitiesTable
    
    def checkPlace(self):

        pTable = {"minutePass" : 100, "breakMyNexus": 0, "breakEnemyNexus": 0}

        if self.state["place"] == "goOurBase":
            if self.state["minute"] >= 3:
                pTable = {"minutePass" : 70, "fight" : 10, "breakMyNexus": 10, "breakEnemyNexus": 10}
        elif self.state["place"] == "goMid":
            pTable = {"minutePass" : 50, "fight" : 30, "breakMyNexus": 10, "breakEnemyNexus": 10}
        elif self.state["place"] == "goEnemyBase":
            pTable = {"minutePass" : 30, "fight" : 50, "breakMyNexus": 10, "breakEnemyNexus": 10}

        return pTable

    async def checkSpot(self, probabilitiesTable):

        match self.state["spot"]:
            case "getResourcesBase":
                players[self.user.id].resources["base"] += 1
            
            case "getResourcesMid":
                players[self.user.id].resources["mid"] += 1

            case "doBasicGear":
                players[self.user.id].resources["base"] -= 1
            
            case "doAdvancedGear":
                players[self.user.id].resources["mid"] -= 1

            case "fight":
                await self.events.fight()
                probabilitiesTable["breakMyNexus"] -= 5
                probabilitiesTable["minutePass"] += 5 

            case "defend":
                probabilitiesTable["breakMyNexus"] -= 10   
                probabilitiesTable["minutePass"] += 10  

            case "stealResources":
                probabilitiesTable["breakMyNexus"] -= 10   
                probabilitiesTable["breakEnemyNexus"] += 10  

            case "breakNexus":
                if self.changePerMinute == None:
                    probabilitiesTable["breakEnemyNexus"] = probabilitiesTable["fight"]
                    probabilitiesTable["fight"] = probabilitiesTable["minutePass"]
                    probabilitiesTable["minutePass"] = 0
                else:        
                    probabilitiesTable["breakEnemyNexus"] -= self.changePerMinute
                    probabilitiesTable["fight"] += self.changePerMinute
                self.changePerMinute = 0.1 * probabilitiesTable["breakEnemyNexus"]