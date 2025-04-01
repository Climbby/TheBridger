import discord

class KitsButton(discord.ui.View):
    @discord.ui.button(label="TANK", row=0, style=discord.ButtonStyle.green, emoji="<:chainmailChestplate:1356637063570653466>")
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message("You chose the tank kit!")

    @discord.ui.button(label="HERO", row=0, style=discord.ButtonStyle.red, emoji="<:stoneSword:1356638920271724614>")
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message("You chose the hero kit!")

    @discord.ui.button(label="MEDIC", row=0, style=discord.ButtonStyle.blurple, emoji="<:poppy:1356637107384488027>")
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_message("You chose the medic kit!")