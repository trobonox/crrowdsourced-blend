import os
import sys
import discord
import logging
import traceback

from utils import config, db
from discord.ext import commands

# Bot version
__version__ = "0.1.0"

# Load external JSON config
config = config.config()
# Extend default logging configuration
logging.basicConfig(
    format=" %(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d - %H:%M:%S",
    level=logging.INFO,
)

# Client setup
## Privileged gateway intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

## Activity status
activity = discord.Activity(type=discord.ActivityType.listening, name=config.status)

## Client init
bot = commands.Bot(command_prefix=config.prefix, intents=intents, activity=activity)


@bot.event
async def on_ready():
    logging.info(
        f"Bot v{__version__} started and logged in as {bot.user}. Running discord.py version {discord.__version__}."
    )

    db.init_db()

    await bot.load_extension("help")
    await loadModules()

async def loadModules():
    for filename in os.listdir("./modules"):
        if filename.endswith(".py"):
            await bot.load_extension(f"modules.{filename[:-3]}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply("Error: You do not have permissions to do that!")
        return

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(
            f"Error: Please provide the required argument `{error.param.name}`! Use `{config.prefix}help [category]` for more info."
        )
        return

    elif isinstance(error, commands.BadArgument):
        await ctx.reply(
            f'Error: Invalid argument, please check if your arguments are correct! *Make sure you use quotes ("") for names or a text that has a space in it!*\n Use `{config.prefix}help [category]` for more info.'
        )
        return

    elif isinstance(error, commands.CheckFailure):
        return

    else:
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return

    await bot.process_commands(message)


bot.run(config.token)
