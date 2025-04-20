import discord

class GameEmbed:
    def __init__(self, color=0xDEE0FC):
        self.embed = discord.Embed(
            title = "TheBridge Simulator Game",
            color = color
        )
        
    async def resetEmbed(self, color=0xDEE0FC):
        """Reset the embed (eg. at the beggining of each roud)"""
        self.embed = discord.Embed(
            title = "TheBridge Simulator Game",
            color = color
        )

    async def change_color(self, color: int):
        """Change the color of the embed."""
        new_embed = discord.Embed(
            title = self.embed.title,
            description = self.embed.description,
            color = color
        )

        for field in self.embed.fields:
            new_embed.add_field(
                name= field.name,
                value= field.value,
                inline= field.inline
            )

        self.embed = new_embed

    async def setDescription(self, description):
        self.embed.description = description

    async def addField(self, name="", value="", inline=False): 
        self.embed.add_field(name=name, value=value, inline=inline)