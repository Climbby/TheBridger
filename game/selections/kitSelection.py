import discord
from discord.ui import Button, View
from game.startGames import startGame
from data.weaponsList import weaponsList

class KitsButton(View):

    def __init__(self, player, ownerId):
        super().__init__(timeout=30)
        self.player = player
        self.ownerId = ownerId
        
        kits = [
            {"label": "TANK", "style": discord.ButtonStyle.green, "emoji": "<:chainmailChestplate:1356637063570653466>"},
            {"label": "HERO", "style": discord.ButtonStyle.red, "emoji": "<:stoneSword:1356638920271724614>"},
            {"label": "MEDIC", "style": discord.ButtonStyle.blurple, "emoji": "<:poppy:1356637107384488027>"}
        ]
        for kit in kits:
            btn = Button(**kit, custom_id=f"kit_{kit['label']}")
            btn.callback = self.handleSelection
            self.add_item(btn)

    async def handleSelection(self, interaction: discord.Interaction):

        if interaction.user.id != self.ownerId:
            await interaction.response.send_message("❌ Only the command user can select the kit!", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        kit_type = interaction.data['custom_id'].split('_')[1]
        channel = interaction.channel
        thread = await channel.create_thread(
            name=f"{interaction.user.name}'s Game",
            type=discord.ChannelType.private_thread
        )
        await thread.add_user(interaction.user)
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

        await startGame(thread) ############### START GAME!!

    async def process_tank(self, channel):
        self.player.maxHealth = 30
        self.player.health = self.player.maxHealth
        await channel.send("Tank kit activated!")

    async def process_hero(self, channel):
        self.player.weapon = weaponsList["stoneSword"]
        await channel.send("Hero kit activated!")

    async def process_medic(self, channel):
        self.player.weapon = weaponsList["healingBow"]
        await channel.send("Medic kit activated!")