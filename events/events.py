import discord

def runEvents():
    from main import bot
    
    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready and online!")
    
    @bot.before_invoke
    async def on_application_command(interaction: discord.Interaction):
        await interaction.response.defer() 
        await createUser(interaction)

async def createUser(interaction):
    from commands.game.data.playerStats import Player, players
    if interaction.user.id not in players:
        players[interaction.user.id] = Player(id=interaction.user.id, name=interaction.user.display_name)    