import discord

def runCommands():
    from main import bot
    from playerStats import Player
    from buttons import KitsButton

    playersDic = {}

    @bot.slash_command(name="hello", description="Say hello to the bot")
    async def hello(ctx: discord.ApplicationContext):
        await ctx.respond("Hey!")

    @bot.slash_command(name="health", description="Get your health")
    async def health(ctx: discord.ApplicationContext):
        if ctx.author.id not in playersDic:
            playersDic[ctx.author.id] = Player(id=ctx.author.id, name=ctx.author.display_name)
        player = playersDic[ctx.author.id]

        await ctx.respond(f"{player.name}'s health is {player.health}, and his damage is {player.damage}")

    @bot.slash_command(name="startgame", description="Start the TheBridge game")
    async def startgame(ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="TheBridge Simulation",
            description="You've just started a simulation of a TheBridge game, choose a kit to start.",
            color=discord.Colour.blurple(),
        )
        embed.add_field(name="TANK <:chainmailChestplate:1356637063570653466>", value="is tanky.", inline=True)
        embed.add_field(name="HERO <:stoneSword:1356638920271724614>", value="is deadly.", inline=True)
        embed.add_field(name="MEDIC <:poppy:1356637107384488027>", value="is supportive.", inline=True)
        await ctx.respond(embed=embed, view=KitsButton())