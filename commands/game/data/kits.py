import discord
from commands.game.data.weapons import WEAPONS

def process_tank(player):
    player.max_health = 30
    player.health = player.max_health

def process_hero(player):
    player.weapon = WEAPONS["stoneSword"]

def process_medic(player):
    player.weapon = WEAPONS["healingBow"]  

KITS = [
    {
        "label": "TANK", 
        "style": discord.ButtonStyle.green, 
        "color": 0x33E302,
        "emoji": "<:chainmailChestplate:1356637063570653466>",
        "handler" : process_tank,
        "description": "is tanky"
    },
    {
        "label": "HERO", 
        "style": discord.ButtonStyle.red,  
        "color": 0xFF2B24,
        "emoji": "<:stoneSword:1356638920271724614>",
        "handler" : process_hero,
        "description": "is deadly."
    },
    {
        "label": "MEDIC", 
        "style": discord.ButtonStyle.blurple, 
        "color": 0x0F1FFF, 
        "emoji": "<:poppy:1356637107384488027>",
        "handler" : process_medic,
        "description": "is supportive"
    }
]