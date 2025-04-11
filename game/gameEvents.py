from game.data.playerStats import playersDic

class GameEvents():
    def __init__(self, eventsEmbed, state, user):
        self.eventsEmbed = eventsEmbed
        self.state = state
        self.user = user

    async def minutePass(self):
        pass 

    async def breakEnemyNexus(self):
        self.state["enemyNexusHP"] -= 1
        await self.eventsEmbed.addField(value=f"Enemy's nexus was broken and now has {self.state["enemyNexusHP"]} HP")
        
    async def breakMyNexus(self):
        self.state["myNexusHP"] -= 1
        await self.eventsEmbed.addField(value=f"Our nexus was broken and now has {self.state["myNexusHP"]} HP")

    async def suddenDeathDamage(self):
        await self.eventsEmbed.addField(value="\n") 
        await self.eventsEmbed.addField(value=f"**Sudden death is dealing 1 damage to each nexus**") 
        await self.breakEnemyNexus()
        await self.breakMyNexus()

    async def hitEnemy(self):
        self.state["enemy"].health -= playersDic[self.user.id].weapon["damage"]
        await self.eventsEmbed.addField(value=f"You have hit the enemy for {playersDic[self.user.id].weapon["damage"]} damage")

    async def getHit(self):
        playersDic[self.user.id].health -= self.state["enemy"].weapon["damage"]
        await self.eventsEmbed.addField(value=f"You have been hit for {self.state["enemy"].weapon["damage"]} damage")