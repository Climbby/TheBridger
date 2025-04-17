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
        pTable = {"minute_pass" : 100, "break_my_nexus": 0, "break_enemy_nexus": 0}

        if self.state.place == "goOurBase" and self.state.minute >= 5:
            pTable = {"minute_pass" : 70, "fight" : 10, "break_my_nexus": 10, "break_enemy_nexus": 10}
        elif self.state.place == "goMid":
            pTable = {"minute_pass" : 50, "fight" : 30, "break_my_nexus": 10, "break_enemy_nexus": 10}
        elif self.state.place == "goEnemyBase":
            pTable = {"minute_pass" : 30, "fight" : 50, "break_my_nexus": 10, "break_enemy_nexus": 10}

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
                self.probabilitiesTable["break_my_nexus"] -= 5
                self.probabilitiesTable["minute_pass"] += 5 

            case "defend":
                self.probabilitiesTable["break_my_nexus"] -= 10   
                self.probabilitiesTable["minute_pass"] += 10  

            case "stealResources":
                self.probabilitiesTable["break_my_nexus"] -= 10   
                self.probabilitiesTable["break_enemy_nexus"] += 10  

            case "breakNexus":
                self.events.break_enemy_nexus()
                if self.changePerMinute == None:
                    self.probabilitiesTable["break_enemy_nexus"] = self.probabilitiesTable["fight"]
                    self.probabilitiesTable["fight"] = self.probabilitiesTable["minute_pass"]
                    self.probabilitiesTable["minute_pass"] = 0
                else:        
                    self.probabilitiesTable["break_enemy_nexus"] -= self.changePerMinute
                    self.probabilitiesTable["fight"] += self.changePerMinute
                self.changePerMinute = 0.1 * self.probabilitiesTable["break_enemy_nexus"]