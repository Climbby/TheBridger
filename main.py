import discord  
import os
from dotenv import load_dotenv
from commands.commands import runCommands
from events.events import runEvents

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = discord.Bot()

runEvents()
runCommands()


bot.run(BOT_TOKEN)