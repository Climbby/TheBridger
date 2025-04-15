from game.data.playerStats import Player
from game.data.playerStats import players
from game.data.probabilitiesTable import Probabilities
from game.selections.optionsSelection import OptionsSelection 
from game.gameEvents import GameEvents
from game.gameEmbed import GameEmbed
from random import randint

class TheBridgeGame():
    def __init__(self, channel, user):
        self.state = {
            "enemyNexusHP" : 15,
            "myNexusHP" : 15,
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
        self.options = OptionsSelection(self.optionsEmbed, self.eventsEmbed, self.state, self.nextEvent, self.events, user, channel)
    
    async def passTime(self):
        if (self.state["myNexusHP"] <= 0 or self.state["enemyNexusHP"] <= 0):
            await self.gameOver()
            return
        
        await self.regenHealth(5) #regenarate some health each round
        await self.eventsEmbed.resetEmbed()  #each round has it's embed
        await self.optionsEmbed.resetEmbed() #each round has it's embed
        self.state["minute"] += 1
        await self.options.sendOptions()
        if (self.state["myNexusHP"] <= 0 or self.state["enemyNexusHP"] <= 0):
            await self.eventsEmbed.setDescription(f"**This is minute {self.state["minute"]}**")
            await self.channel.send(embed=self.eventsEmbed.embed)
            await self.gameOver()
            return
        if self.state["minute"] >= 10:
            await self.events.suddenDeathDamage()
        await self.eventsEmbed.setDescription(f"**This is minute {self.state["minute"]}**")
        await self.channel.send(embed=self.eventsEmbed.embed)

    async def nextEvent(self):
        randomProbability = randint(1,100)
        cumulativeProbability = 0
        probabilities = Probabilities(self.state, self.user, self.events) 
        await probabilities.setTable()

        for event, probability in probabilities.probabilitiesTable.items():
            cumulativeProbability += probability
            if randomProbability <= cumulativeProbability:
                if event == "fight":
                    probabilities.probabilitiesTable["fight"] *= 0.2
                await getattr(self.events, event)()
                break


    async def regenHealth(self, rHealth):
        if rHealth + players[self.user.id].health > players[self.user.id].maxHealth:
            players[self.user.id].health = players[self.user.id].maxHealth
        else: 
            players[self.user.id].health += rHealth

    async def gameOver(self):
        await self.channel.send("# Game ENDED!")

        if (self.state["myNexusHP"] <= 0 and self.state["enemyNexusHP"] <= 0):
            await self.channel.send("ITS A TIE!")
        elif self.state["myNexusHP"] <= 0:
            await self.channel.send("you lost.....")
        else:
            await self.channel.send("you WON!!!!!!")