import configparser
import logging

import discord
import yfinance as yf
from discord.ext import commands, tasks

from stonkmaster.core.market import get_price_and_change


class WatchCommand(commands.Cog,
                   name="Watch",
                   description="Displays the price and change of a ticker in the status."):
    def __init__(self, bot: commands.Bot, config: configparser.ConfigParser):
        self.bot = bot
        self.config = config
        self.current_ticker = "GME"
        self.update_status.start()

    @commands.command(name="watch")
    async def _watch(self, ctx, ticker):
        try:
            yf_ticker = yf.Ticker(ticker)
            info = yf_ticker.info

            if len(info) <= 1:
                logging.info(f"{ctx.author.display_name} tried to watch invalid ticker {ticker}")
                await ctx.send(f"{ticker.upper()} gibt's ned oida! {self.config['emojis']['NotFound']}")
                return

            if 'longName' in info:
                msg = f"Alright, i'm watching **{info['longName']} ({info['symbol']})** now. " + \
                      self.config['emojis']['Eyes']
            else:
                msg = f"Alright, i'm watching **{info['symbol']}** now. {self.config['emojis']['Eyes']}"

            logging.info(f"{ctx.author.display_name} set watched ticker to {info['symbol']}")
            self.current_ticker = info['symbol']
            await self.update_status()
            await ctx.send(msg)

        except Exception as ex:
            logging.exception(f"Exception in WatchCommand: {ex}")
            await ctx.send(f"Do hod wos ned bassd, I bin raus. {self.config['emojis']['Error']}")

    @tasks.loop(seconds=10.0)
    async def update_status(self):
        price, change = get_price_and_change(self.current_ticker)
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching,
                                      name=f"{self.current_ticker}: {round(price, 2)}$ ({'{0:+.2f}'.format(change)}%)"))

    @update_status.before_loop
    async def wait_until_ready(self):
        await self.bot.wait_until_ready()