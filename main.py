import discord
import os
from dotenv import load_dotenv

load_dotenv()  # Loads the .env file into environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

bot.run(BOT_TOKEN)