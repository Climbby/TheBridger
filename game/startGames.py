import discord
import game.gameLogic as gameLogic
import asyncio

activeGames = {}

async def startGame(thread):

    activeGames[thread.id] = gameLogic.TheBridgeGame(thread)
    game = activeGames.get(thread.id)

    while (game.state["myNexusHP"] > 0 and game.state["enemyNexusHP"] > 0):
        await asyncio.sleep(5)
        await game.passTime() ########################################## DO THE GAME!!!!!!!!!!
    await thread.send("⏳ This game thread will self-destruct in a minute...")
    await asyncio.sleep(60)
    await thread.delete()