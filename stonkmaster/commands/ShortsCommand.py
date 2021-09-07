import configparser
import logging

import yfinance as yf
from discord.ext import commands


class ShortsCommand(commands.Cog,
                    name="Shorts",
                    description="Provides currently known information on how heavily the stonk is shorted."):
    def __init__(self, bot: commands.Bot, config: configparser.ConfigParser):
        self.bot = bot
        self.config = config

    @commands.command(name="shorts")
    async def _shorts(self, ctx, ticker):
        try:
            yf_ticker = yf.Ticker(ticker)
            info = yf_ticker.info

            if len(info) <= 1:
                await ctx.send(f"{ticker.upper()} gibt's ned oida! {self.config['emojis']['NotFound']}")
                return

            symbol = info['symbol']

            if 'sharesShort' not in info or 'shortPercentOfFloat' not in info:
                await ctx.send(f"{symbol} ko ned geshorted werdn, du Hosnbiesla! {self.config['emojis']['NoShort']}")
                return

            shares_short = info['sharesShort']

            if 'longName' in info:
                msg = (f"Currently **{'{:,}'.format(shares_short)} shares** of **{info['longName']} ({symbol})** "
                       f"are shorted.")
            else:
                msg = (f"Currently **{'{:,}'.format(shares_short)} shares** of **{symbol}** "
                       f"are shorted.")

            if info['shortPercentOfFloat'] is not None:
                short_percent_of_float = round(info['shortPercentOfFloat'] * 100, 2)
                msg = msg + f" This corresponds to **{short_percent_of_float}%** of available shares."

            await ctx.send(msg)

            if symbol == 'GME' or symbol == 'AMC':
                await ctx.send(f"Real SI may be much higher -> Hedgies are fucked. {self.config['emojis']['Kennyg']}")

        except Exception as ex:
            logging.error(ex)
            await ctx.send(f"Do hod wos ned bassd, I bin raus. {self.config['emojis']['Error']}")
