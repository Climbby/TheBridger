from commands.game.data.playerStats import players

class Probabilities():

    def __init__(self, state, user, events):
        self.state = state
        self.user = user
        self.events = events
        self.changePerMinute = None
        self.probabilitiesTable = None

    async def set_table(self):
        """Defines the probabilities table"""    

        self.probabilitiesTable = self._check_area()
        await self._check_spot()
    
    def _check_area(self):
        """Adjust probabilities based on the area you're in"""

        # if in our base and before minute 5
        pTable = {"minutePass" : 100, "breakMyNexus": 0, "breakEnemyNexus": 0}

        if self.state.place == "goOurBase" and self.state.minute >= 5:
            pTable = {"minutePass" : 70, "fight" : 10, "breakMyNexus": 10, "breakEnemyNexus": 10}
        elif self.state.place == "goMid":
            pTable = {"minutePass" : 50, "fight" : 30, "breakMyNexus": 10, "breakEnemyNexus": 10}
        elif self.state.place == "goEnemyBase":
            pTable = {"minutePass" : 30, "fight" : 50, "breakMyNexus": 10, "breakEnemyNexus": 10}

        return pTable

    async def _check_spot(self):
        """Does actions based on the current spot."""

        match self.state.spot:
            case "getResourcesBase":
                players[self.user.id].resources["base"] += 1
            
            case "getResourcesMid":
                players[self.user.id].resources["mid"] += 1

            case "doBasicGear":
                players[self.user.id].resources["base"] -= 3
            
            case "doAdvancedGear":
                players[self.user.id].resources["mid"] -= 3

            case "fight":
                await self.events.fight()
                self.probabilitiesTable["breakMyNexus"] -= 5
                self.probabilitiesTable["minutePass"] += 5 

            case "defend":
                self.probabilitiesTable["breakMyNexus"] -= 10   
                self.probabilitiesTable["minutePass"] += 10  

            case "stealResources":
                self.probabilitiesTable["breakMyNexus"] -= 10   
                self.probabilitiesTable["breakEnemyNexus"] += 10  

            case "breakNexus":
                if self.changePerMinute == None:
                    self.probabilitiesTable["breakEnemyNexus"] = self.probabilitiesTable["fight"]
                    self.probabilitiesTable["fight"] = self.probabilitiesTable["minutePass"]
                    self.probabilitiesTable["minutePass"] = 0
                else:        
                    self.probabilitiesTable["breakEnemyNexus"] -= self.changePerMinute
                    self.probabilitiesTable["fight"] += self.changePerMinute
                self.changePerMinute = 0.1 * self.probabilitiesTable["breakEnemyNexus"]