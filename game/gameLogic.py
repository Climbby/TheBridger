from data.probabilitiesTable import probabilitiesTable
from data.playerStats import Player
from game.selections.optionsSelection import OptionsSelection 
from game.gameEvents import GameEvents
from game.gameEmbed import GameEmbed
from random import randint

class TheBridgeGame(GameEvents, OptionsSelection):
    def __init__(self, channel):
        super().__init__(
            state={
                "enemyNexusHP" : 5,
                "myNexusHP" : 5,
                "minute" : 0,
                "enemyCount" : 0,
                "enemy" : Player(0, "guest"),
                "place" : "goOurBase"
            },
            eventsEmbed=GameEmbed(),
            channel=channel,
            optionsEmbed=GameEmbed()
        )
    
    async def passTime(self):
        if (self.state["myNexusHP"] <= 0 or self.state["enemyNexusHP"] <= 0):
            await self.gameOver()
            return

        await self.eventsEmbed.resetEmbed()
        await self.optionsEmbed.resetEmbed()
        self.state["minute"] += 1
        if self.state["minute"] >= 5:
            await self.suddenDeathDamage()
        await self.sendOptions()
        await self.nextEvent()
        await self.eventsEmbed.setDescription(f"**This is minute {self.state["minute"]}**")
        await self.channel.send(embed=self.eventsEmbed.embed)

        if (self.state["myNexusHP"] <= 0 or self.state["enemyNexusHP"] <= 0):
            await self.gameOver()

    async def nextEvent(self):
        randomProbability = randint(1,100)
        cumulativeProbability = 0

        for event, probability in probabilitiesTable[self.state["minute"]].items():
            cumulativeProbability += probability
            if randomProbability <= cumulativeProbability:
                await getattr(self, event)()
                break

    async def gameOver(self):
        await self.channel.send("# Game ENDED!")

        if (self.state["myNexusHP"] <= 0 and self.state["enemyNexusHP"] <= 0):
            await self.channel.send("ITS A TIE!")
        elif self.state["myNexusHP"] <= 0:
            await self.channel.send("you lost.....")
        else:
            await self.channel.send("you WON!!!!!!")

    async def minutePass(self):
        pass 