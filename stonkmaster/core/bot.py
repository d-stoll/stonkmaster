import configparser

from discord.ext import commands

from stonkmaster.commands.ChartCommand import ChartCommand
from stonkmaster.commands.PriceCommand import PriceCommand
from stonkmaster.commands.SecCommand import SecCommand
from stonkmaster.commands.ShortsCommand import ShortsCommand


def create_bot(config: configparser.ConfigParser, intents=None, loop=None):
    help_command = commands.DefaultHelpCommand(no_category="Other Commands")

    bot = commands.Bot(command_prefix=config["discord.py"]["CommandPrefix"],
                       description=config["discord.py"]["description"],
                       help_command=help_command,
                       intents=intents,
                       loop=loop)

    bot.add_cog(ChartCommand(bot, config))
    bot.add_cog(PriceCommand(bot, config))
    bot.add_cog(SecCommand(bot, config))
    bot.add_cog(ShortsCommand(bot, config))

    return bot
