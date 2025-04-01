def runEvents():
    from main import bot
    
    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready and online!")