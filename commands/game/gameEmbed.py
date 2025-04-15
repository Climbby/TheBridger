import discord

class GameEmbed:
    def __init__(self):
        self.embed = discord.Embed(
            title = "TheBridge Simulator Game",
            color = discord.Colour.blurple()
        )
        
    async def resetEmbed(self):
        self.embed = discord.Embed(
            title="TheBridge Simulator Game",
            color=discord.Colour.blurple()
        )
        
    async def setDescription(self, description):
        self.embed.description = description

    async def addField(self, name="", value="", inline=False): 
        self.embed.add_field(name=name, value=value, inline=inline)