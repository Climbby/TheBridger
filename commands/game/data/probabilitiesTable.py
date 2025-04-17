from commands.game.data.playerStats import players

class Probabilities():

    def __init__(self, state, user, events_embed, events):
        self.state = state
        self.user = user
        self.events_embed = events_embed
        self.events = events
        self.nexus_open = False 
        self.changePerMinute = None
        self.probabilitiesTable = None

    async def set_table(self):
        """Defines the probabilities table"""    
        self.probabilitiesTable = self._check_area()
        await self._check_option()
    
    def _check_area(self) -> dict:
        """Adjust probabilities based on the area you're in"""
        game_minute = self.state.minute

        if game_minute < 5:
            return {"minute_pass" : 100}
            
        probabilitiesTable = {"break_my_nexus": game_minute, "break_enemy_nexus" : game_minute}

        if self.state.area == "goOurBase":
            probabilitiesTable["minute_pass"] = 95 - 2 * game_minute
            probabilitiesTable["whos_fighting"] = 5

        elif self.state.area == "goMid":
            probabilitiesTable["minute_pass"] = 70 - 2 * game_minute
            probabilitiesTable["whos_fighting"] = 30

        elif self.state.area == "goEnemyBase":
            probabilitiesTable["minute_pass"] = 40 - 2 * game_minute
            probabilitiesTable["whos_fighting"] = 60

        return probabilitiesTable

    async def _check_option(self):
        """Does actions based on the current option."""

        match self.state.spot:
            case "getResourcesBase":
                await self.events_embed.addField(name="__Action Taken:__", value=f"You just got +1 BASIC resources") 
                players[self.user.id].resources["base"] += 1
            
            case "getResourcesMid":
                await self.events_embed.addField(name="__Action Taken:__", value=f"You just got +1 **ADVANCED** resources") 
                players[self.user.id].resources["mid"] += 1

            case "doBasicGear":
                await self.events_embed.addField(name="__Action Taken:__", value=f"You've crafted the BASIC gear")
                players[self.user.id].resources["base"] -= 3
                self.events.doBasicGear()                
            
            case "doAdvancedGear":
                await self.events_embed.addField(name="__Action Taken:__", value=f"You've crafted some **ADVANCED** gear")
                players[self.user.id].resources["mid"] -= 3
                self.events.doAdvancedGear()                

            case "fight":
                await self.events_embed.addField(name="__Action Taken:__", value=f"You have fought the enemy.")
                await self.events.whos_fighting("me") 

            case "defend":
                if not self.nexus_open:
                    await self.events_embed.addField(name="__Action Taken:__", value=f"You've opened the nexus area")
                    self.nexus_open = True
                    self.events.open_nexus() # DOESNT EXIST YET!!!!!!!!!!!!!!!!!!
                else:
                    await self.events_embed.addField(name="__Action Taken:__", value=f"You're defending the nexus")
                    self.events.defend_nexus() # DOESNT EXIST YET!!!!!!!!!!!!!!!!!!

            case "stealResources":
                await self.events_embed.addField(name="__Action Taken:__", value=f"Their resources have been stolen")
                self.probabilitiesTable["break_my_nexus"] -= 5
                # TAKE THEIR WEAPON AND ARMOR, enemy = default homeless player with random kit
                self.events.steal_resources() # to do

            case "breakNexus":
                await self.events_embed.addField(name="__Action Taken:__", value=f"Someone has broken the enemy nexus")
                await self.events.break_enemy_nexus()