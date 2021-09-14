import configparser

from discord.ext import commands

from stonkmaster.cogs.fundamentals import FundamentalsCog
from stonkmaster.cogs.technicals import TechnicalsCog


def create_bot(config: configparser.ConfigParser, intents=None, loop=None):
    help_command = commands.DefaultHelpCommand(no_category="Other Commands")

    bot = commands.Bot(command_prefix=config["discord.py"]["CommandPrefix"],
                       description=config["discord.py"]["description"],
                       help_command=help_command,
                       intents=intents,
                       loop=loop)

    bot.add_cog(FundamentalsCog(bot, config))
    bot.add_cog(TechnicalsCog(bot, config))

    return bot
