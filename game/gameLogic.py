import discord
import game.gameEvents as gameEvents
import asyncio

async def gameLogic(interaction: discord.Interaction):

    channel = interaction.channel

    while (gameEvents.gameState["myNexusHP"] != 0 and gameEvents.gameState["enemyNexusHP"] != 0):
        await asyncio.sleep(5)
        await gameEvents.passTime(interaction)
    
    await channel.send("Game ENDED!")