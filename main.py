import settings
import discord
from discord.ext import commands
from discord import app_commands



logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"{bot.user} connected to Discord.)")
        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync(guild=settings.GUILDS_ID)

    bot.run(settings.DISCORD_BOT_TOKEN, root_logger=True)
    
if __name__ == "__main__":
    run()

