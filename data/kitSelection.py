import discord
from discord.ui import Button, View
from game.gameLogic import gameLogic
from utils.utils import findWeapon

class KitsButton(View):

    def __init__(self, player):
        super().__init__(timeout=30)
        self.player = player
        
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
        kit_type = interaction.data['custom_id'].split('_')[1]
        self.player.reset()
        self.player.kit = kit_type

        if kit_type == "TANK":
            await self.process_tank(interaction)
        elif kit_type == "HERO":
            await self.process_hero(interaction)
        elif kit_type == "MEDIC":
            await self.process_medic(interaction)
        
        # GAME LOGIC !!!!!!!!!!!!!!
        await gameLogic(interaction)

    async def process_tank(self, interaction):
        self.player.maxHealth = 30
        self.player.health = self.player.maxHealth
        await interaction.response.send_message("Tank kit activated!")

    async def process_hero(self, interaction):
        self.player.weapon = findWeapon("stoneSword")
        await interaction.response.send_message("Hero kit activated!")

    async def process_medic(self, interaction):
        self.player.weapon = findWeapon("healingBow")
        await interaction.response.send_message("Medic kit activated!")