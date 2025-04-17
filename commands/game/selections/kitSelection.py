import asyncio
import discord
from commands.game.data.weapons import WEAPONS
from commands.game.data.kits import KITS
from commands.game.startGames import startGame

class KitsButton(discord.ui.View):
    def __init__(self, player, owner):
        super().__init__(timeout=300)
        self.player = player
        self.owner = owner
        self.interaction = None
        self.thread = None
        
        for kit in KITS:
            btn = discord.ui.Button(
                label=kit["label"],
                style=kit["style"],
                emoji=kit["emoji"],
                custom_id=kit["label"]
            )
            btn.callback = self.handle_selection
            self.add_item(btn)

    async def handle_selection(self, interaction):
        """Key/Main function that runs everything to start the game"""

        await interaction.response.defer(ephemeral=True)
        self.interaction = interaction

        if not await self._check_is_owner():
            return

        self.thread = await self._create_thread()
        self.player.reset()
        self.player.kit = interaction.custom_id
        await self._process_kit_choice()
        await self._disable_buttons()
        await startGame(self.thread, self.interaction.channel, interaction.user)

    async def _check_is_owner(self):
        """Checks if interaction user is the one who ran the command."""

        if self.interaction.user.id != self.owner.id:
            await self.interaction.channel.send("❌ Only the command user can select the kit!", ephemeral=True)
            return False 
        
        return True      

    async def _disable_buttons(self):

        for item in self.children:
            item.disabled = True

        await self.interaction.edit_original_response(view=self)

    async def _create_thread(self):
        """Create the game thread."""
        thread = await self.interaction.channel.create_thread(
            name=f"{self.interaction.user.display_name}'s Game",
            type=discord.ChannelType.private_thread
        )
        await thread.add_user(self.interaction.user) 
        return thread       
    
    async def _process_kit_choice(self):
        from commands.commands import create_stats_embed

        getattr(self, f"process_{self.player.kit.lower()}")()
        for kit in KITS:
            if kit["label"] == self.player.kit:
                stats_embed = create_stats_embed(self.player, self.owner.display_name, color=kit["color"])
                await self.thread.send(content=f"# __{kit["label"]}__ {kit["emoji"]} Activated!", embed=stats_embed)
                await asyncio.sleep(1)
                await self.thread.send("_(you can do /mystats during the game)_")

    def process_tank(self):
        self.player.max_health = 30
        self.player.health = self.player.max_health

    def process_hero(self):
        self.player.weapon = WEAPONS["stoneSword"]

    def process_medic(self):
        self.player.weapon = WEAPONS["healingBow"]
        
    async def on_timeout(self):

        for item in self.children:
            item.disabled = True
            
        await self.message.edit(view=self)
        await asyncio.sleep(3600)
        await self.message.edit(view=None)