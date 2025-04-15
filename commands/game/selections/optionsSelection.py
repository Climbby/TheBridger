import discord
from discord.ui import Button, View
from commands.game.data.playerStats import players
import asyncio

class OptionsSelection():
    def __init__(self, optionsEmbed, eventsEmbed, state, doNextEvent, events, user, channel):
        self.optionsEmbed = optionsEmbed
        self.eventsEmbed = eventsEmbed
        self.state = state
        self.doNextEvent = doNextEvent
        self.events = events
        self.user = user
        self.channel = channel

    async def sendOptions(self):
        optionsDic = {
            "goOurBase": ["getResourcesBase", "defend"],
            "goMid": ["goOurBase", "fight", "getResourcesMid", "goEnemyBase"],
            "goEnemyBase": ["goMid", "breakNexus", "fight", "stealResources"]
        }

        if self.state["minute"] >= 3:
            optionsDic["goOurBase"].append("goMid")

        if players[self.user.id].resources["base"] > 0:
            optionsDic["goOurBase"].append("doBasicGear")

        if players[self.user.id].resources["mid"] > 0:
            optionsDic["goOurBase"].append("doAdvancedGear")

        optionsDisplayName = {
            "goOurBase_place": "your Base",
            "goMid_place": "the Middle",
            "goEnemyBase_place": "Enemy's Base",
            "goOurBase": "Go To Base",
            "goMid": "To the Middle!",
            "goEnemyBase": "Rush Enemy's Base!",
            "getResourcesBase": "Get Resources",
            "doBasicGear" : "Craft basic Gear",
            "doAdvancedGear" : "Craft ADVANCED Gear",
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
        view = OptionsButtons(self.state, self.channel, self.eventsEmbed, self.doNextEvent, self.events, optionsDisplayName, listOfOptions)
        await self.channel.send(embed=self.optionsEmbed.embed, view=view)
        await view.done.wait()


class OptionsButtons(View):
        
    def __init__(self, state, channel, eventsEmbed, doNextEvent, events, optionsDisplayName, listOfOptions):
        super().__init__(timeout=120)
        self.state = state
        self.channel = channel
        self.eventsEmbed = eventsEmbed
        self.doNextEvent = doNextEvent
        self.events = events
        self.optionsDisplayName = optionsDisplayName
        self.listOfOptions = listOfOptions
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

        # await getattr(self.events, optionChosen)()

        match optionChosen:
            case "doBasicGear": 
                await getattr(self.events, optionChosen)()

            case "doAdvancedGear": 
                await getattr(self.events, optionChosen)()

        #     case "goEnemyBase": 
        #         print("B")

        #     case "getResourcesBase": 
        #         print("B")

        #     case "defend": 
        #         print("B")

        #     case "fight": 
        #         print("B")

        #     case "getResourcesMid": 
        #         print("B")

        #     case "breakNexus": 
        #         print("B")

        #     case "stealResources": 
        #         print("B")

        await self.eventsEmbed.addField(name="Action Taken:", value=f"Option Chosen was: {optionChosen}")