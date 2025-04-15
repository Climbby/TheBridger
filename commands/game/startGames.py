import commands.game.gameLogic as gameLogic
import asyncio

active_games = {}

async def startGame(thread, user):

    active_games[thread.id] = gameLogic.TheBridgeGame(thread, user)
    game = active_games.get(thread.id)

    while (game.state["myNexusHP"] > 0 and game.state["enemyNexusHP"] > 0):
        await asyncio.sleep(3)
        await game.passTime() ########################################## DO THE GAME!!!!!!!!!!
    await thread.send("⏳ This game thread will self-destruct in a minute...")
    await asyncio.sleep(60)
    await thread.delete()