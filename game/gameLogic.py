from data.probabilitiesTable import probabilitiesTable
from data.playerStats import Player
from game.gameEvents import GameEvents
from game.gameEmbed import GameEmbed
from random import randint

class TheBridgeGame(GameEvents):
    def __init__(self):
        self.state = {
            "enemyNexusHP" : 5,
            "myNexusHP" : 5,
            "minute" : 0,
            "enemyCount" : 0,
            "enemy" : Player(0, "guest") 
        }
        self.embed = GameEmbed()
        super().__init__(self.state, self.embed)
    
    async def minutePass(self):
        pass
    
    async def passTime(self, channel):
        await self.embed.resetEmbed()
        self.state["minute"] += 1
        if self.state["minute"] >= 5:
            await self.suddenDeathDamage()
        if (self.state["myNexusHP"] <= 0 or self.state["enemyNexusHP"]<= 0):
            await self.gameOver(channel)
            return
        
        await self.nextEvent(channel)
        await self.embed.setDescription(f"**This is minute {self.state["minute"]}**")
        await channel.send(embed=self.embed.embed)
        if (self.state["myNexusHP"] <= 0 or self.state["enemyNexusHP"]<= 0):
            await self.gameOver(channel)
            return

    async def nextEvent(self, channel):
        randomProbability = randint(1,100)
        cumulativeProbability = 0

        for event, probability in probabilitiesTable[self.state["minute"]].items():
            cumulativeProbability += probability
            if randomProbability <= cumulativeProbability:
                await getattr(self, event)()
                # await self.embed.setDescription(f"**This is minute {self.state["minute"]}**")
                # await channel.send(embed=self.embed.embed)
                break

    async def gameOver(self, channel):
        # await self.embed.setDescription(f"**This is minute {self.state["minute"]}**")
        # await channel.send(embed=self.embed.embed)
        await channel.send("# Game ENDED!")

        if (self.state["myNexusHP"] <= 0 and self.state["enemyNexusHP"] <= 0):
            await channel.send("ITS A TIE!")
        elif self.state["myNexusHP"] <= 0:
            await channel.send("you lost.....")
        else:
            await channel.send("you WON!!!!!!")