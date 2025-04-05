from game.gameBase import GameBase
import asyncio

class OptionsSelection(GameBase):
    def __init__(self, channel=None, optionsEmbed=None, **kwargs):
        super().__init__(**kwargs)
        self.channel = channel
        self.optionsEmbed = optionsEmbed

    async def sendOptions(self):
        await self.optionsEmbed.setDescription(description=f"Choose your option, you're in {self.state["place"]}")
        await self.optionsEmbed.addField(value=f"Option1", inline=True)
        await self.optionsEmbed.addField(value=f"Option2", inline=True)
        await self.optionsEmbed.addField(value=f"Option3", inline=True)
        await self.channel.send(embed=self.optionsEmbed.embed)
        await asyncio.sleep(4)