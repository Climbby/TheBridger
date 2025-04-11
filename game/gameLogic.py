from game.data.playerStats import Player
from game.data.probabilitiesTable import Probabilities
from game.selections.optionsSelection import OptionsSelection 
from game.gameEvents import GameEvents
from game.gameEmbed import GameEmbed
from random import randint

class TheBridgeGame():
    def __init__(self, channel, user):
        self.state = {
            "enemyNexusHP" : 5,
            "myNexusHP" : 5,
            "minute" : 0,
            "enemyCount" : 0,
            "enemy" : Player(0, "guest"),
            "place" : "goOurBase",
            "spot" : "goOurBase"
        }
        self.user = user
        self.channel = channel
        self.eventsEmbed = GameEmbed()
        self.optionsEmbed = GameEmbed()
        self.events = GameEvents(self.eventsEmbed, self.state, user)
        self.options = OptionsSelection(self.optionsEmbed, self.state, self.nextEvent, channel)
    
    async def passTime(self):
        if (self.state["myNexusHP"] <= 0 or self.state["enemyNexusHP"] <= 0):
            await self.gameOver()
            return

        await self.eventsEmbed.resetEmbed()  #each round has it's embed
        await self.optionsEmbed.resetEmbed() #each round has it's embed
        self.state["minute"] += 1
        await self.options.sendOptions()
        if (self.state["myNexusHP"] <= 0 or self.state["enemyNexusHP"] <= 0):
            await self.eventsEmbed.setDescription(f"**This is minute {self.state["minute"]}**")
            await self.channel.send(embed=self.eventsEmbed.embed)
            await self.gameOver()
            return
        if self.state["minute"] >= 5:
            await self.events.suddenDeathDamage()
        await self.eventsEmbed.setDescription(f"**This is minute {self.state["minute"]}**")
        await self.channel.send(embed=self.eventsEmbed.embed)

    async def nextEvent(self):
        randomProbability = randint(1,100)
        cumulativeProbability = 0
        probabilities = Probabilities(self.state) 

        for event, probability in probabilities.probabilitiesTable.items():
            cumulativeProbability += probability
            if randomProbability <= cumulativeProbability:
                await getattr(self.events, event)()
                break

    async def gameOver(self):
        await self.channel.send("# Game ENDED!")

        if (self.state["myNexusHP"] <= 0 and self.state["enemyNexusHP"] <= 0):
            await self.channel.send("ITS A TIE!")
        elif self.state["myNexusHP"] <= 0:
            await self.channel.send("you lost.....")
        else:
            await self.channel.send("you WON!!!!!!")