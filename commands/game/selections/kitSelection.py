import discord
import asyncio
from commands.game.data.weapons import WEAPONS
from commands.game.data.kits import KITS
from commands.game.startGames import startGame

class KitsButton(discord.ui.View):
    def __init__(self, player, owner):
        super().__init__(timeout=300)
        self.player = player
        self.owner = owner
        
        for kit in KITS:
            btn = discord.ui.Button(
                label=kit["label"],
                style=kit["style"],
                emoji=kit["emoji"],
                custom_id=kit["label"]
            )
            btn.callback = self.handleSelection
            self.add_item(btn)
        
    async def on_timeout(self):

        for item in self.children:
            item.disabled = True
            
        await self.message.edit(view=self)
        await asyncio.sleep(3600)
        await self.message.edit(view=None)

    async def handleSelection(self, interaction: discord.Interaction):
        from commands.commands import create_stats_embed
        if interaction.user.id != self.owner.id:
            await interaction.response.send_message("❌ Only the command user can select the kit!", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        kit_type = interaction.custom_id
        channel = interaction.channel
        user = interaction.user

        #create a private thread for the game
        thread = await channel.create_thread(
            name=f"{interaction.user.display_name}'s Game",
            type=discord.ChannelType.private_thread
        )
        await thread.add_user(user)

        # reset player and apply kit
        self.player.reset()
        self.player.kit = kit_type

        # Process the selected kit dynamically
        process_method = getattr(self, f"process_{kit_type.lower()}")
        process_method()
        for kit in KITS:
            if kit["label"] == kit_type:
                stats_embed = create_stats_embed(self.player, self.owner.display_name, color=kit["color"])
                await thread.send(content=f"# __{kit["label"]}__ {kit["emoji"]} Activated!", embed=stats_embed)
                await asyncio.sleep(1)
                await thread.send("_(you can do /mystats during the game)_")
        
        # Disable all buttons after selection
        for item in self.children:
            item.disabled = True
        await interaction.edit_original_response(view=self)

        # Start the game
        await startGame(thread, user)

    def process_tank(self):
        self.player.max_health = 30
        self.player.health = self.player.max_health

    def process_hero(self):
        self.player.weapon = WEAPONS["stoneSword"]

    def process_medic(self):
        self.player.weapon = WEAPONS["healingBow"]
        