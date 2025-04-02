import discord

def runCommands():
    from main import bot
    from playerStats import playersDic
    from kitSelection import KitsButton

    @bot.slash_command(name="mystats", description="Get your health")
    async def mystats(ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="Your stats",
            description="Here are your stats.",
            color=discord.Colour.blurple(),
        )
        for stat_name, stat_value in vars(playersDic[ctx.author.id]).items():
            if stat_name == "id": continue
            embed.add_field(name=stat_name, value=stat_value, inline=False)

        await ctx.respond(embed=embed)

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

        await ctx.respond(embed=embed, view=KitsButton(playersDic[ctx.author.id]))