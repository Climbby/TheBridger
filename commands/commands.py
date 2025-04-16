import discord
from commands.game.data.playerStats import players
from commands.game.data.kits import KITS
from commands.game.selections.kitSelection import KitsButton

def runCommands():
    from main import bot

    @bot.slash_command(name="mystats", description="Get your health")
    async def mystats(ctx: discord.ApplicationContext):
        player = players[ctx.author.id]
        embed = create_stats_embed(player, ctx.author.display_name, color=0xDEE0FC)
        await ctx.respond(embed=embed)

    @bot.slash_command(name="startgame", description="Start the TheBridge game")
    async def startgame(ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="TheBridge Simulation",
            description="You've just started a simulation of a TheBridge game, choose a kit to start.",
            color=0xDEE0FC,
        )
        for kit in KITS:
            embed.add_field(
                name=f"{kit["label"]} {kit["emoji"]}", 
                value=kit["description"], 
                inline=True
            )

        await ctx.respond(content=ctx.author.mention, embed=embed, view=KitsButton(player=players[ctx.author.id], owner=ctx.author))

def create_stats_embed(player, display_name, color=discord.Colour.blurple()):
        embed = discord.Embed(
            title=f"{display_name}'s stats",
            color=color,
        )
        player.display_stats(embed)
        return embed