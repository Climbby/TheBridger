from random import choice
from commands.game.data.playerStats import players, Player
from commands.game.data.weapons import WEAPONS
from commands.game.data.kits import KITS

class GameEvents():
    def __init__(self, state, user, events_embed):
        self.state = state
        self.user = user
        self.events_embed = events_embed
        self.open_nexus_count = 0
        self.enemy = Player(0, "guest")
        choice(KITS)["handler"](self.enemy)

    async def break_enemy_nexus(self):
        self.state.enemy_nexus_hp -= 1
        await self.events_embed.addField(value=f"⛏️ THEIR NEXUS WAS BROKEN - {self.state.enemy_nexus_hp} HP ❤️")
        await self.events_embed.change_color(0xFF2B24)
        
    async def break_my_nexus(self):
        self.state.my_nexus_hp -= 1
        await self.events_embed.addField(value=f"⛏️ OUR NEXUS WAS BROKEN 🚨 - {self.state.my_nexus_hp} HP ❤️")
        await self.events_embed.change_color(0xFF2B24)

    async def sudden_death(self):
        """Removes 1 Health from each nexus per game tick."""
        await self.events_embed.addField(value="\n") 
        await self.events_embed.addField(value=f"**🚨 Sudden death is dealing 1 damage to each nexus🚨 **") 
        await self.break_my_nexus()
        await self.break_enemy_nexus()

    async def die(self):
        await self.events_embed.addField(value="💀 You have been defeated and have taken a minute to respawn")
        self.state.minute += 1
        self.state.area = "goOurBase"
        self.state.spot = "goOurBase"
        players[self.user.id].health = players[self.user.id].max_health
        players[self.user.id].gear = None
        players[self.user.id].resources["base"] = 0
        players[self.user.id].resources["mid"] = 0

    async def whos_fighting(self, fighter="enemy"):
        """Makes you fight the enemy, the fighter deals the first blow"""
        
        # fighter deals the first blow
        if fighter == "me":
            players[self.user.id].has_fought = True
            self.enemy.health -= players[self.user.id].weapon["damage"]
        else:
            players[self.user.id].health -= self.enemy.weapon["damage"]

        # we fight until the death 
        while self.enemy.health > 0 and players[self.user.id].health > 0:
            self.enemy.health -= players[self.user.id].weapon["damage"]  
            players[self.user.id].health -= self.enemy.weapon["damage"]          
        
        # checks which one is dead
        if players[self.user.id].health <= 0:
            players[self.user.id].is_dead = True
            await self.die()
        if self.enemy.health <= 0:
            await self.events_embed.addField(
                value=f"⚔️ You have defeated the enemy ⚔️\n \
                        Your Health: ❤️ {players[self.user.id].health}/{players[self.user.id].max_health} HP")

        players[self.user.id].has_stolen = False
        self.enemy = Player(0, "guest")
        choice(KITS)["handler"](self.enemy)

    async def open_nexus(self):
        self.open_nexus_count += 1
        await self.events_embed.addField(
            name="__Action Taken:__",
            value=f"⚒️ You've started to open the nexus area {self.open_nexus_count}/3 ⚒️"
        )
        if self.open_nexus_count == 3:
            await self.events_embed.change_color(0x2ECC71)
            return True

    def steal_resources(self):
        self.enemy.weapon = WEAPONS["hand"]
        players[self.user.id].has_stolen = True
        
    async def do_basic_gear(self):
        players[self.user.id].gear = "basic"
        players[self.user.id].weapon = WEAPONS["stoneSword"]
        players[self.user.id].max_health = 30
        await self.events_embed.change_color(0x2ECC71)

    async def do_advanced_gear(self):
        players[self.user.id].gear = "advanced"
        players[self.user.id].weapon = WEAPONS["diamondSword"]
        players[self.user.id].max_health = 50
        await self.events_embed.change_color(0x2ECC71)