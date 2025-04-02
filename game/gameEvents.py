from data.playerStats import playersDic

class GameEvents:
    def __init__(self, state, embed):
        self.state = state
        self.embed = embed

    async def breakEnemyNexus(self):
        self.state["enemyNexusHP"] -= 1
        await self.embed.addField(value=f"Enemy's nexus was broken and now has {self.state["enemyNexusHP"]} HP")
        
    async def breakMyNexus(self):
        self.state["myNexusHP"] -= 1
        await self.embed.addField(value=f"Our nexus was broken and now has {self.state["myNexusHP"]} HP")

    async def suddenDeathDamage(self):
        await self.embed.addField(value=f"**Sudden death is dealing 1 damage to each nexus**") 
        await self.breakEnemyNexus()
        await self.breakMyNexus()

    async def hitEnemy(self, interaction):
        self.state["enemy"].health -= playersDic[interaction.user.id].weapon["chars"]["damage"]
        await self.embed.addField(value=f"You have hit the enemy for {playersDic[interaction.user.id].weapon["chars"]["damage"]} damage")

    async def getHit(self, interaction):
        playersDic[interaction.user.id].health -= self.state["enemy"].weapon["chars"]["damage"]
        await self.embed.addField(value=f"You have been hit for {self.state["enemy"].weapon["chars"]["damage"]} damage")