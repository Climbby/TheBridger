from playerStats import Player, playersDic
from random import randint
import discord

gameState={
    "enemyNexusHP" : 3,
    "myNexusHP" : 3,
    "minute" : 1,
    "enemyCount" : 0,
    "enemy" : Player(0, "guest") 
}

async def minutePass():
    gameState["minute"] +=1
    return f"A minute has passed"

async def passTime(interaction):
    channel = interaction.channel
    await minutePass()
    await nextEvent(channel)

async def nextEvent(channel):
    from probabilitiesTable import probabilitiesTable
    randomProbability = randint(1, 100)
    cummulativeProbability = 0

    for event, prob in probabilitiesTable[0].items():
        cummulativeProbability += prob
        if randomProbability <= cummulativeProbability:
            message = await event()
            await channel.send(message)
            break

async def breakEnemyNexus():
    gameState["enemyNexusHP"] -= 1
    return f"Enemy's nexus was broken and now has {gameState["enemyNexusHP"]} HP"
    
async def breakMyNexus():
    gameState["myNexusHP"] -= 1
    return f"Our nexus was broken and now has {gameState["myNexusHP"]} HP"

async def suddenDeathDamage():
    gameState["enemyNexusHP"] -= 1
    gameState["myNexusHP"] -= 1

async def hitEnemy(interaction: discord.Interaction):
    gameState["enemy"].health -= playersDic[interaction.user.id].weapon["chars"]["damage"]

async def getHit(interaction: discord.Interaction):
    playersDic[interaction.user.id].health -= gameState["enemy"].weapon["chars"]["damage"]