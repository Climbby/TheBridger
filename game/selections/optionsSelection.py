import discord
from discord.ui import Button, View
from game.data.probabilitiesTable import Probabilities
import asyncio

class OptionsSelection():
    def __init__(self, optionsEmbed, state, doNextEvent, channel):
        self.optionsEmbed = optionsEmbed
        self.state = state
        self.doNextEvent = doNextEvent
        self.channel = channel

    async def sendOptions(self):
        optionsDic = {
            "goOurBase": ["getResourcesBase", "defend"],
            "goMid": ["goOurBase", "fight", "getResourcesMid", "goEnemyBase"],
            "goEnemyBase": ["goMid", "breakNexus", "fight", "stealResources"]
        }

        if self.state["minute"] >= 5:
            optionsDic["goOurBase"].append("goMid")

        optionsDisplayName = {
            "goOurBase_place": "your Base",
            "goMid_place": "the Middle",
            "goEnemyBase_place": "Enemy's Base",
            "goOurBase": "Go To Base",
            "goMid": "To the Middle!",
            "goEnemyBase": "Rush Enemy's Base!",
            "getResourcesBase": "Get Resources",
            "defend": "Lets Defend",
            "fight": "Fight Them!",
            "getResourcesMid": "Get Resources",
            "breakNexus": "Break The Nexus!",
            "stealResources": "Steal Their Items"
        }
        listOfOptions = [option for option in optionsDic[self.state["place"]]]
        await self.optionsEmbed.setDescription(description=f"Choose your option, you're in {optionsDisplayName[f"{self.state["place"]}_place"]}")
        for i in range(len(listOfOptions)):
            await self.optionsEmbed.addField(name=f"**Option {i+1}:**", value=optionsDisplayName[listOfOptions[i]])
        view = OptionsButtons(self.state, self.channel, self.doNextEvent, optionsDisplayName, listOfOptions)
        await self.channel.send(embed=self.optionsEmbed.embed, view=view)
        await view.done.wait()


class OptionsButtons(View):
        
    def __init__(self, state, channel, doNextEvent, optionsDisplayName, listOfOptions):
        super().__init__(timeout=120)
        self.state = state
        self.channel = channel
        self.optionsDisplayName = optionsDisplayName
        self.listOfOptions = listOfOptions
        self.doNextEvent = doNextEvent
        self.done = asyncio.Event()
        for option in listOfOptions:
            btn = Button(label=optionsDisplayName[option], style=discord.ButtonStyle.blurple, custom_id=option)
            btn.callback = self.handleSelection
            self.add_item(btn)

    async def handleSelection(self, interaction):
        await interaction.response.defer(ephemeral=True)
        match (interaction.custom_id):
            case "goOurBase":
                self.state["place"] = "goOurBase"
                self.state["spot"] = "goOurBase"

            case "goMid":
                self.state["place"] = "goMid"
                self.state["spot"] = "goMid"

            case "goEnemyBase":
                self.state["place"] = "goEnemyBase"
                self.state["spot"] = "goEnemyBase"

            case _:
                self.state["spot"] = interaction.data["custom_id"]
                await self.doEvent(interaction.data["custom_id"])

        await self.doNextEvent()

        for item in self.children:
            item.disabled = True
        await interaction.edit_original_response(view=self)
        self.done.set()
        
    async def doEvent(self, optionChosen):

        match optionChosen:
            case "goOurBase": 
                print("B")

            case "goMid": 
                print("B")

            case "goEnemyBase": 
                print("B")

            case "getResourcesBase": 
                print("B")

            case "defend": 
                print("B")

            case "fight": 
                print("B")

            case "getResourcesMid": 
                print("B")

            case "breakNexus": 
                print("B")

            case "stealResources": 
                print("B")

        await self.channel.send(f"Option Chosen was: {optionChosen}")