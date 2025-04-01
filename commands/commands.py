import discord

def runCommands():
    from main import bot
    from main import player

    @bot.slash_command(name="hello", description="Say hello to the bot")
    async def hello(ctx: discord.ApplicationContext):
        await ctx.respond("Hey!")

    @bot.slash_command(name="health", description="Get your health")
    async def health(ctx: discord.ApplicationContext):
        await ctx.respond(f"{ctx.author.display_name}'s health is {player.health}")