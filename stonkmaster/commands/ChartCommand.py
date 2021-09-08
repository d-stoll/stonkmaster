import configparser
import datetime as dt
import logging
import re

import discord
import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf
from discord.ext import commands

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
                diff = dt.timedelta(days=int(range.removesuffix('d')))
            elif months_pattern.match(range):
                diff = dt.timedelta(days=int(range.removesuffix('m')) * 30)
            elif years_pattern.match(range):
                diff = dt.timedelta(days=int(range.removesuffix('y')) * 365)
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

            end = dt.datetime.now()
            start = end - diff

            if diff.days > 60:
                interval = "1d"
            elif diff.days > 30:
                interval = "90m"
            elif diff.days > 14:
                interval = "60m"
            elif diff.days > 7:
                interval = "30m"
            elif diff.days > 3:
                interval = "15m"
            else:
                interval = "5m"

            ticker_data = yf.download([symbol], group_by="Ticker", start=start, end=end, interval=interval)

            candlestick = go.Figure(data=[go.Candlestick(x=ticker_data.index,
                                                         open=ticker_data['Open'],
                                                         high=ticker_data['High'],
                                                         low=ticker_data['Low'],
                                                         close=ticker_data['Close'])])

            if 'longName' in info:
                chart_title = f"{info['longName']} ({info['symbol']})"
            else:
                chart_title = info['symbol']

            rangebreaks = [dict(bounds=["sat", "mon"])]
            if interval != "1d":
                rangebreaks += [dict(bounds=[16, 9.5], pattern="hour")]

            candlestick.update_layout(title=chart_title)
            candlestick.update_xaxes(
                rangeslider_visible=False,
                rangebreaks=rangebreaks
            )
            candlestick.update_yaxes(tickprefix='$')

            candlestick.write_image(f"{self.config['stonkmaster']['TmpFolder']}/{info['symbol']}-{range}.png")
            with open(f"{self.config['stonkmaster']['TmpFolder']}/{info['symbol']}-{range}.png", 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)

            await ctx.send(f"Fia an bessern Graph schaust moi do vorbei: <https://finance.yahoo.com/chart/{info['symbol']}/>")

        except Exception as ex:
            logging.exception(f"Exception in ChartCommand: {ex}")
            await ctx.send(f"Do hod wos ned bassd, I bin raus. {self.config['emojis']['Error']}")
