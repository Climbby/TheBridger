import discord
from game.data.playerStats import players
from game.selections.kitSelection import KitsButton

def runCommands():
    from main import bot

    @bot.slash_command(name="mystats", description="Get your health")
    async def mystats(ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s stats",
            color=discord.Colour.blurple(),
        )
        player = players[ctx.author.id]
        player.display_stats(embed)

        await ctx.respond(embed=embed)

    @bot.slash_command(name="startgame", description="Start the TheBridge game")
    async def startgame(ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="TheBridge Simulation",
            description="You've just started a simulation of a TheBridge game, choose a kit to start.",
            color=discord.Colour.blurple(),
        )
        roles = {
            "TANK <:chainmailChestplate:1356637063570653466>" : "is tanky",
            "HERO <:stoneSword:1356638920271724614>" : "is deadly.",
            "MEDIC <:poppy:1356637107384488027>" : "is supportive."
        }
        for name, desc in roles.items():
            embed.add_field(name=name, value=desc, inline=True)

        await ctx.respond(content=ctx.author.mention, embed=embed, view=KitsButton(player=players[ctx.author.id], ownerId=ctx.author.id))