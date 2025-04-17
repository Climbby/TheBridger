from commands.game.data.playerStats import players, Player
from commands.game.data.weapons import WEAPONS

class GameEvents():
    def __init__(self, state, user, eventsEmbed):
        self.state = state
        self.user = user
        self.eventsEmbed = eventsEmbed

    async def minute_pass(self):
        pass 

    async def break_enemy_nexus(self):
        self.state.enemy_nexus_hp -= 1
        await self.eventsEmbed.addField(value=f"Enemy's nexus was broken and now has {self.state.enemy_nexus_hp} HP")
        
    async def break_my_nexus(self):
        self.state.my_nexus_hp -= 1
        await self.eventsEmbed.addField(value=f"Our nexus was broken and now has {self.state.my_nexus_hp} HP")

    async def suddenDeathDamage(self):
        await self.eventsEmbed.addField(value="\n") 
        await self.eventsEmbed.addField(value=f"**Sudden death is dealing 1 damage to each nexus**") 
        await self.break_enemy_nexus()
        await self.break_my_nexus()

    async def die(self):
        self.state.place = "goOurBase"
        self.state.spot = "goOurBase"
        players[self.user.id].health = players[self.user.id].max_health
        players[self.user.id].resources["base"] = 0
        players[self.user.id].resources["mid"] = 0
        if self.state.minute >= 10:
            await self.suddenDeathDamage()

    async def fight(self):
        enemy = Player(0, "guest")

        while (enemy.health > 0 and players[self.user.id].health > 0):
            enemy.health -= players[self.user.id].weapon["damage"]  
            players[self.user.id].health -= enemy.weapon["damage"]          
        
        if enemy.health <= 0:
            await self.eventsEmbed.addField(value="You have defeated the enemy")
        else:
            self.state.minute += 1
            await self.eventsEmbed.addField(value="You have been defeated and have taken a minute to respawn")
            await self.die()
        
    def doBasicGear(self):
        players[self.user.id].weapon = WEAPONS["stoneSword"]
        players[self.user.id].max_health = 30

    def doAdvancedGear(self):
        players[self.user.id].weapon = WEAPONS["diamondSword"]
        players[self.user.id].max_health = 50