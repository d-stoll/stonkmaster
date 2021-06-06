import os
from discord.ext import commands

from stonkmaster.commands.ChartCommand import ChartCommand
from stonkmaster.commands.PriceCommand import PriceCommand
from stonkmaster.commands.ShortsCommand import ShortsCommand

bot = commands.Bot(command_prefix='$')


@bot.command(name='price')
async def _price(ctx, arg):
    await PriceCommand().run(ctx, arg)


@bot.command(name='shorts')
async def _shorts(ctx, arg):
    await ShortsCommand().run(ctx, arg)


@bot.command(name='chart')
async def _chart(ctx, arg):
    await ChartCommand().run(ctx, arg)


if __name__ == "__main__":
    bot.run(os.environ['DISCORD_TOKEN'])
