import configparser

from discord.ext import commands


class BaseCog(commands.Cog):

    def __init__(self, bot: commands.Bot, config: configparser.ConfigParser):
        self.bot = bot
        self.config = config
