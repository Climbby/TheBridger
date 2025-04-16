import asyncio
import discord
from commands.game.data.playerStats import players

OPTIONS_DISPLAY_NAME = {
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

class OptionsSelection():
    def __init__(self, optionsEmbed, eventsEmbed, state, doNextEvent, events, user, channel):
        self.optionsEmbed = optionsEmbed
        self.eventsEmbed = eventsEmbed
        self.state = state
        self.doNextEvent = doNextEvent
        self.events = events
        self.user = user
        self.channel = channel
        self.options_available = {
            "goOurBase": ["getResourcesBase", "defend"],
            "goMid": ["goOurBase", "fight", "getResourcesMid", "goEnemyBase"],
            "goEnemyBase": ["goMid", "breakNexus", "fight", "stealResources"]
        }
        self.list_of_options = None

    async def sendOptions(self):
        """Sends the embed with the options available and the respective buttons."""
        self._check_available_options()
        view = await self._prepare_options_embed()
        await self.channel.send(embed=self.optionsEmbed.embed, view=view)
        await view.done.wait()

    def _check_available_options(self):

        #avoids duplicates
        for option in ["goMid", "doBasicGear", "doAdvancedGear"]:
            if option in self.options_available["goOurBase"]:
                continue

        #checks specific cases
        if self.state.minute >= 3:
            self.options_available["goOurBase"].append("goMid")

        if players[self.user.id].resources["base"] > 0:
            self.options_available["goOurBase"].append("doBasicGear")

        if players[self.user.id].resources["mid"] > 0:
            self.options_available["goOurBase"].append("doAdvancedGear")

        self.list_of_options = [option for option in self.options_available[self.state.place]]

    async def _prepare_options_embed(self):
        await self.optionsEmbed.setDescription(
            description=f"Choose your option, you're in {OPTIONS_DISPLAY_NAME[f"{self.state.place}_place"]}"
        )

        for i in range(len(self.list_of_options)):
            await self.optionsEmbed.addField(name=f"**Option {i+1}:**", value=OPTIONS_DISPLAY_NAME[self.list_of_options[i]])

        view = OptionsButtons(self.state, self.channel, self.eventsEmbed, self.doNextEvent, self.events, self.list_of_options)
        return view      


class OptionsButtons(discord.ui.View):
    def __init__(self, state, channel, eventsEmbed, doNextEvent, events, listOfOptions):
        super().__init__(timeout=300)
        self.state = state
        self.channel = channel
        self.eventsEmbed = eventsEmbed
        self.doNextEvent = doNextEvent
        self.events = events
        self.list_of_options = listOfOptions
        self.interaction = None
        self.done = asyncio.Event()
        self._setup_buttons()

    def _setup_buttons(self):
        """Creates the buttons for the options view."""

        for option in self.list_of_options:
            btn = discord.ui.Button(label=OPTIONS_DISPLAY_NAME[option], style=discord.ButtonStyle.blurple, custom_id=option)
            btn.callback = self.handle_selection
            self.add_item(btn)

    async def _check_option_place(self):

        if self.interaction.custom_id in ["goOurBase", "goMid", "goEnemyBase"]:
            self.state.place = self.interaction.custom_id
            self.state.spot = self.interaction.custom_id

        else:
            self.state.spot = self.interaction.data["custom_id"]
            await self.do_event(self.interaction.data["custom_id"]) 

    async def _disable_buttons(self):

        for item in self.children:
            item.disabled = True

        await self.interaction.edit_original_response(view=self)

    async def handle_selection(self, interaction):
        self.interaction = interaction
        await interaction.response.defer(ephemeral=True)
        await self._check_option_place()
        await self.doNextEvent()
        await self._disable_buttons()
        self.done.set()

    async def do_event(self, chosen_option):
        """Does specific event cases."""

        if chosen_option == "doBasicGear" or chosen_option == "doAdvancedGear": 
            await getattr(self.events, chosen_option)

        await self.eventsEmbed.addField(name="Action Taken:", value=f"Option Chosen was: {chosen_option}")

    async def on_timeout(self):
        await self.channel.delete()