from commands.game.data.playerStats import players

FIGHTING_COOLDOWN = 1

class Probabilities():

    def __init__(self, state, user, events_embed, events):
        self.state = state
        self.user = user
        self.events_embed = events_embed
        self.events = events
        self.opening_nexus_count = 0
        self.fighting_cooldown = 0
        self.nexus_open = False 
        self.probabilitiesTable = None

    async def set_table(self):
        """Defines the probabilities table"""    
        self.probabilitiesTable = self._check_area()
        await self._check_option()
    
    def _check_area(self) -> dict:
        """Adjust probabilities based on the area you're in"""
        game_minute = self.state.minute

        if game_minute < 5:
            return {}
            
        probabilitiesTable = {"break_my_nexus": game_minute * 2, "break_enemy_nexus": game_minute * 2 - 10}

        if self.state.area == "goOurBase":
            probabilitiesTable["whos_fighting"] = 5

        elif self.state.area == "goMid":
            probabilitiesTable["whos_fighting"] = 30

        elif self.state.area == "goEnemyBase":
            probabilitiesTable["whos_fighting"] = 60

        if self.nexus_open:
            probabilitiesTable["break_my_nexus"] += 10
            probabilitiesTable["break_enemy_nexus"] += 10

        if players[self.user.id].has_fought:
            probabilitiesTable["whos_fighting"] = 0
            players[self.user.id].has_fought = False

        return probabilitiesTable

    async def _check_option(self):
        """Does actions based on the current option."""

        match self.state.spot:
            case "getResourcesBase":
                await self.events_embed.addField(name="__Action Taken:__", value=f"⛏️ You just got +1 BASIC resources") 
                players[self.user.id].resources["base"] += 1
            
            case "getResourcesMid":
                await self.events_embed.addField(name="__Action Taken:__", value=f"✨ You just got +1 **ADVANCED** resources ✨") 
                players[self.user.id].resources["mid"] += 1

            case "doBasicGear":
                await self.events_embed.addField(
                    name="⚙️ __Crafting Complete__", 
                    value=f"• **Type:** 🛡️ Basic Gear \n \
                            • **Cost:** 💰 3 Basic resources \n \
                            • **Weapon:** ⚔️ Stone Sword \n \
                            • **HP:** ❤️ 30 HP"
                    )
                players[self.user.id].resources["base"] -= 3
                await self.events.do_basic_gear()                
            
            case "doAdvancedGear":
                await self.events_embed.addField(
                    name="⚙️ __Crafting Complete__", 
                    value=f"• **Type:** ✨ Advanced Gear ✨ \n \
                            • **Cost:** 💰 3 **ADVANCED** resources \n \
                            • **Weapon:** ⚔️ **Diamond Sword** \n \
                            • **HP:** ❤️ 30 HP"
                    )
                players[self.user.id].resources["mid"] -= 3
                await self.events.do_advanced_gear()                

            case "fight":
                await self.events_embed.addField(name="__Action Taken:__", value=f"⚔️ You have fought the enemy.")
                await self.events.whos_fighting("me") 

            case "defend":
                if self.nexus_open:
                    await self.events_embed.addField(name="__Action Taken:__", value=f"🏰 You're now defending the Nexus")
                    if self.state.minute >= 5:
                        self.probabilitiesTable["whos_fighting"] += self.probabilitiesTable["break_my_nexus"]
                        self.probabilitiesTable["break_my_nexus"] = 0
                if not self.nexus_open and await self.events.open_nexus():
                    await self.events_embed.addField(value=f"✨ **The Nexus is now OPEN!!! ✨**")
                    self.nexus_open = True

            case "stealResources":
                await self.events_embed.addField(name="__Action Taken:__", value=f"🦹 You've stolen the enemy's weapon")
                self.probabilitiesTable["break_my_nexus"] -= 5
                self.events.steal_resources()

            case "breakNexus":
                await self.events_embed.addField(name="__Action Taken:__", value=f"⛏️ You have Broken the Enemy Nexus ⛏️")
                await self.events.break_enemy_nexus()