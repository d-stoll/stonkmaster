import os

from discord.ext import commands


def alpha_vantage_command():
    return commands.check(lambda _: os.environ['ALPHA_VANTAGE_TOKEN'] is not None)
