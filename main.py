import settings
import discord
from discord.ext import commands
from cogs.truco_cog import TrucoCog



logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents, activity=discord.Game(name="Truco Argentino"))

    @bot.event
    async def on_ready():
        logger.info(f"{bot.user} connected to Discord.)")
        await bot.add_cog(TrucoCog(bot))
        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync(guild=settings.GUILDS_ID)
    
    bot.run(settings.DISCORD_BOT_TOKEN, root_logger=True)
    
if __name__ == "__main__":
    run()

