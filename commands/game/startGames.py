from commands.game.gameLogic import TheBridgeGame
import asyncio

active_games = {}
GAME_TICK_INTERVAL = 2
SELF_DESTRUCT_DELAY = 60

class GameStarter:
    def __init__(self, thread, channel, user):
        self.thread = thread
        self.channel = channel
        self.user = user
        self.game = TheBridgeGame(thread, user)

    async def startGame(self):
        """Start and manage a game session in a thread."""
        try:
            active_games[self.thread.id] = self.game
            await self.run_game_loop()

            # After game ends
            await self.thread.send("⏳ The game has ended and will self-destruct in a minute...")
            await asyncio.sleep(SELF_DESTRUCT_DELAY)
            
        finally:
            active_games.pop(self.thread.id)
            await self.afk_detection()

    async def run_game_loop(self):
        """Run the game loop until one nexus is destroyed."""
        
        while self.game.state.my_nexus_hp > 0 and self.game.state.enemy_nexus_hp > 0:
            await asyncio.sleep(GAME_TICK_INTERVAL)
            await self.game.passTime()

    async def afk_detection(self):
        """If the player is afk, the thread will be deleted"""
        try:
            await self.thread.delete()
        except Exception as e:
            await self.channel.send(content="Game was deleted because you were afk.", ephemeral=True)   