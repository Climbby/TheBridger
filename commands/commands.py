import discord
from commands.game.data.playerStats import players
from commands.game.data.kits import KITS
from commands.game.selections.kitSelection import KitsButton

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
        for kit in KITS:
            embed.add_field(
                name=f"{kit["label"]} {kit["emoji"]}", 
                value=kit["description"], 
                inline=True
            )

        await ctx.respond(content=ctx.author.mention, embed=embed, view=KitsButton(player=players[ctx.author.id], owner_id=ctx.author.id))