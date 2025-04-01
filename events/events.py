def runEvents():
    import discord
    from main import bot
    
    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready and online!")
    
    @bot.before_invoke
    async def on_application_command(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True) 
        await createUser(interaction)

async def createUser(interaction):
    from playerStats import Player, playersDic
    if interaction.user.id not in playersDic:
        playersDic[interaction.user.id] = Player(id=interaction.user.id, name=interaction.user.display_name)    