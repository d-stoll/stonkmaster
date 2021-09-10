import configparser
import datetime as dt
import logging
import os
import re

import discord
import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf
from discord.ext import commands

from stonkmaster.core.market import daily, intraday

pio.templates.default = 'plotly_dark'


class ChartCommand(commands.Cog,
                   name="Chart",
                   description="Generates a chart showing the price development of the share in the last months."):
    def __init__(self, bot: commands.Bot, config: configparser.ConfigParser):
        self.bot = bot
        self.config = config

    @commands.command(name="chart")
    async def _chart(self, ctx: commands.Context, ticker: str, range: str):
        try:
            days_pattern = re.compile("[0-9]+d")
            months_pattern = re.compile("[0-9]+m")
            years_pattern = re.compile("[0-9]+y")

            if days_pattern.match(range):
                days = int(range.removesuffix('d'))
                diff = dt.timedelta(days=days)
                range_str = f"the last {days} days" if days > 1 else "today"
            elif months_pattern.match(range):
                months = int(range.removesuffix('m'))
                diff = dt.timedelta(days=months * 30)
                range_str = "the last" + (f"{months} months" if months > 1 else "month")
            elif years_pattern.match(range):
                years = int(range.removesuffix('y'))
                diff = dt.timedelta(days=years * 365)
                range_str = "the last" + (f"{years} years" if years > 1 else "year")
            else:
                logging.info(f"{ctx.author.display_name} tried to generate graph with invalid range {range}")
                await ctx.send("The time range must be specified in days (d), months (m) or years (m). " +
                               "Example: 7d (7 days)")
                return

            yf_ticker = yf.Ticker(ticker)
            info = yf_ticker.info

            if len(info) <= 1:
                logging.info(f"{ctx.author.display_name} tried to generate graph for invalid ticker {ticker}")
                await ctx.send(f"{ticker.upper()} gibt's ned oida! {self.config['emojis']['NotFound']}")
                return

            symbol = info['symbol']

            await ctx.send(f"**Generating chart of {symbol} for {range_str}... {self.config['emojis']['Chart']}**")

            if diff.days > 30:
                ticker_data = daily(symbol=symbol, days=diff.days)
            else:
                if diff.days > 14:
                    interval = "60min"
                elif diff.days > 7:
                    interval = "30min"
                elif diff.days > 3:
                    interval = "15min"
                elif diff.days > 1:
                    interval = "5min"
                else:
                    interval = "1min"

                ticker_data = intraday(symbol=symbol, interval=interval, days=diff.days)

            candlestick = go.Figure(data=[go.Candlestick(x=ticker_data.index,
                                                         open=ticker_data['open'],
                                                         high=ticker_data['high'],
                                                         low=ticker_data['low'],
                                                         close=ticker_data['close'])])

            if 'longName' in info:
                chart_title = f"{info['longName']} ({info['symbol']})"
            else:
                chart_title = info['symbol']

            rangebreaks = [dict(bounds=["sat", "mon"])]

            if diff.days <= 30:
                rangebreaks += [dict(bounds=[16, 9.5], pattern="hour")]

            candlestick.update_layout(title=chart_title)
            candlestick.update_xaxes(rangeslider_visible=False, rangebreaks=rangebreaks)
            candlestick.update_yaxes(tickprefix='$')

            path = f"{self.config['stonkmaster']['TmpFolder']}/{info['symbol']}-{range}.png"
            candlestick.write_image(path)
            with open(path, 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)

            os.remove(path)

        except Exception as ex:
            logging.exception(f"Exception in ChartCommand: {ex}")
            await ctx.send(f"Do hod wos ned bassd, I bin raus. {self.config['emojis']['Error']}")
