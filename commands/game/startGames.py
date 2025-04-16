import commands.game.gameLogic as gameLogic
import asyncio

active_games = {}
GAME_TICK_INTERVAL = 2
SELF_DESTRUCT_DELAY = 60

async def startGame(thread, user):
    """Start and manage a game session in a thread."""
    try:
        game = gameLogic.TheBridgeGame(thread, user)
        active_games[thread.id] = game
        await run_game_loop(game)

        # After game ends
        await thread.send("⏳ The game has ended and will self-destruct in a minute...")
        await asyncio.sleep(SELF_DESTRUCT_DELAY)
        
    finally:
        active_games.pop(thread.id)
        await thread.delete()

async def run_game_loop(game: gameLogic.TheBridgeGame):
    """Run the game loop until one nexus is destroyed."""
    while game.state.my_nexus_hp > 0 and game.state.enemy_nexus_hp > 0:
        await asyncio.sleep(GAME_TICK_INTERVAL)
        await game.passTime()