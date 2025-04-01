import os
import sys

commandsPath = os.path.abspath("commands")
eventsPath = os.path.abspath("events")

sys.path.append(commandsPath)
sys.path.append(eventsPath)

import discord
from dotenv import load_dotenv
from playerStats import Player
from commands import runCommands
from events import runEvents

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = discord.Bot()
player = Player()

runEvents()
runCommands()


bot.run(BOT_TOKEN)