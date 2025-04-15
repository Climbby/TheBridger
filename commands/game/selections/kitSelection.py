import discord
from commands.game.data.weapons import WEAPONS
from commands.game.data.kits import KITS
from commands.game.startGames import startGame

class KitsButton(discord.ui.View):

    def __init__(self, player, owner_id):
        super().__init__(timeout=120)
        self.player = player
        self.owner_id = owner_id
        
        for kit in KITS:
            btn = discord.ui.Button(
                label=kit["label"],
                style=kit["style"],
                emoji=kit["emoji"],
                custom_id=kit["label"]
            )
            btn.callback = self.handleSelection
            self.add_item(btn)

    async def handleSelection(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message("❌ Only the command user can select the kit!", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        kit_type = interaction.custom_id
        channel = interaction.channel
        user = interaction.user
        thread = await channel.create_thread(
            name=f"{interaction.user.name}'s Game",
            type=discord.ChannelType.private_thread
        )
        await thread.add_user(user)
        self.player.reset()
        self.player.kit = kit_type

        if kit_type == "TANK":
            await self.process_tank(thread)
        elif kit_type == "HERO":
            await self.process_hero(thread)
        elif kit_type == "MEDIC":
            await self.process_medic(thread)
        
        for item in self.children:
            item.disabled = True
        await interaction.edit_original_response(view=self)

        await startGame(thread, user) ############### START GAME!!

    async def process_tank(self, channel):
        self.player.maxHealth = 30
        self.player.health = self.player.maxHealth
        await channel.send("Tank kit activated!")

    async def process_hero(self, channel):
        self.player.weapon = WEAPONS["stoneSword"]
        await channel.send("Hero kit activated!")

    async def process_medic(self, channel):
        self.player.weapon = WEAPONS["healingBow"]
        await channel.send("Medic kit activated!")