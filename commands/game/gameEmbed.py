import discord

class GameEmbed:
    def __init__(self):
        self.embed = discord.Embed(
            title = "TheBridge Simulator Game",
            color = 0xDEE0FC
        )
        
    async def resetEmbed(self):
        """Reset the embed (eg. at the beggining of each roud)"""
        self.embed = discord.Embed(
            title= "TheBridge Simulator Game",
            color= 0xDEE0FC
        )
        
    def set_color(self):
        pass

    async def setDescription(self, description):
        self.embed.description = description

    async def addField(self, name="", value="", inline=False): 
        self.embed.add_field(name=name, value=value, inline=inline)