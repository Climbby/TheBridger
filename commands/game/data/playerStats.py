from typing import Dict
from commands.game.data.weapons import WEAPONS

players = {}
DEFAULT_WEAPON = "hand"
STAT_ORDER = ["health", "weapon", "kit", "resources"]

class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.max_health = 20
        self.health = self.max_health
        self.weapon = WEAPONS[DEFAULT_WEAPON]
        self.gear = None
        self.kit = None
        self.resources = {"base" : 0, "mid" : 0}
    
    def reset(self):
        """Useful for reseting stats (eg. on death)"""
        self.__init__(id=self.id, name=self.name)

    def get_stat_display(self, stat_name) -> Dict[str, str]:
        """Returns the formatted value of a stat for display."""
        match stat_name:
            case "health":
                return {"❤️ Health:"    : f"{self.health}/{self.max_health} HP"}
            
            case "weapon":
                return {"⚔️ Weapon:"    : self.weapon["name"].capitalize()
                        }
            case "kit":
                return {"🎒 Kit:"       : f"{self.kit} KIT"} 
            
            case "resources":
                return {"💰 Resources:" : f"{self.resources["base"]} (basic)\n"
                                          f"{self.resources["mid"]} (advanced)"}
        
    def display_stats(self, embed):
        """Adds all stats to a Discord embed."""

        for stat_name in STAT_ORDER:
            if stat_name == "kit" and self.kit == None:
                continue

            stat = self.get_stat_display(stat_name)
            for name, value in stat.items():
                embed.add_field(name=name, value=value, inline=False)