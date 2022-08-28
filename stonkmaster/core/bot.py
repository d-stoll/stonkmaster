import configparser

from discord.ext import commands

from stonkmaster.cogs.price_chart import PriceChartCog
from stonkmaster.cogs.research import ResearchCog
from stonkmaster.cogs.settings import SettingsCog


def create_bot(config: configparser.ConfigParser, intents=None, loop=None):
    help_command = commands.DefaultHelpCommand(no_category="Other Commands")

    bot = commands.Bot(command_prefix=config["discord.py"]["CommandPrefix"],
                       description=config["discord.py"]["description"],
                       help_command=help_command,
                       intents=intents,
                       loop=loop)

    bot.add_cog(PriceChartCog(bot, config))
    bot.add_cog(ResearchCog(bot, config))
    bot.add_cog(SettingsCog(bot, config))

    return bot
