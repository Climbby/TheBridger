from commands.game.data.playerStats import Player
from commands.game.data.playerStats import players
from commands.game.data.probabilitiesTable import Probabilities
from commands.game.selections.optionsSelection import OptionsSelection 
from commands.game.gameEvents import GameEvents
from commands.game.gameEmbed import GameEmbed
from dataclasses import dataclass
from random import randint

INITIAL_NEXUS_HP = 15
REGEN_AMOUNT = 5
SUDDEN_DEATH_MINUTE = 10

@dataclass(slots=True)
class GameState:
    enemy_nexus_hp: int = INITIAL_NEXUS_HP
    my_nexus_hp: int = INITIAL_NEXUS_HP
    minute: int = 0
    enemy: Player = Player(0, "guest")
    area: str = "goOurBase"
    spot: str = "goOurBase"
    is_dead: bool = False    

class TheBridgeGame():
    def __init__(self, channel, user):
        self.state = GameState()
        self.channel = channel
        self.user = user
        self.events_embed = GameEmbed()
        self.options_embed = GameEmbed()
        self.events = GameEvents(self.state, user, self.events_embed)
        self.options = OptionsSelection(self.options_embed, self.events_embed, self.state, self.nextEvent, self.events, user, channel)
        self.probabilities = Probabilities(self.state, self.user, self.events_embed, self.events)
    
    async def passTime(self):
        """Where each game tick is processed."""
        await self.regenHealth(REGEN_AMOUNT)
        await self.events_embed.resetEmbed()
        await self.options_embed.resetEmbed()
        self.state.minute += 1
        await self.options.sendOptions()

        if self.state.my_nexus_hp <= 0 or self.state.enemy_nexus_hp <= 0:
            await self.events_embed.setDescription(f"**This is minute {self.state.minute}**")
            await self.channel.send(embed=self.events_embed.embed)
            await self.gameOver()
            return
        
        if self.state.is_dead:
            await self.nextEvent()
            if self.state.minute >= SUDDEN_DEATH_MINUTE:
                await self.events.sudden_death()

        if (self.state.my_nexus_hp <= 0 or self.state.enemy_nexus_hp <= 0):
            await self.events_embed.setDescription(f"**This is minute {self.state.minute}**")
            await self.channel.send(embed=self.events_embed.embed)
            await self.gameOver()
            return

        if self.state.minute >= SUDDEN_DEATH_MINUTE:
            await self.events.sudden_death()

        if (self.state.my_nexus_hp <= 0 or self.state.enemy_nexus_hp <= 0):
            await self.events_embed.setDescription(f"**This is minute {self.state.minute}**")
            await self.channel.send(embed=self.events_embed.embed)
            await self.gameOver()
            return

        try:
            await self.events_embed.setDescription(f"**This is minute {self.state.minute}**")
            await self.channel.send(embed=self.events_embed.embed)
        except Exception:
            pass

    async def nextEvent(self):
        """Where next event the next random event is calculated.""" 
        await self.probabilities.set_table()

        for event_name, probability in self.probabilities.probabilitiesTable.items():
            roll = randint(1,100)
            if roll <= probability:
                await getattr(self.events, event_name)()

    async def regenHealth(self, regenerated_health):
        """Regenerate some health each round."""
        players[self.user.id].health = min(
            players[self.user.id].health + regenerated_health,
            players[self.user.id].max_health
        )

    async def gameOver(self):
        """If the game is over, send the outcome feedback."""
        if self.state.my_nexus_hp <= 0 and self.state.enemy_nexus_hp <= 0:
            outcome = "ITS A TIE!"
        elif self.state.my_nexus_hp <= 0:
            outcome = "you lost....."
        else:
            outcome = "you WON!!!!!!"

        await self.channel.send(f"# Game ENDED!\n{outcome}")