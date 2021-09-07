import configparser
import datetime as dt
import logging
import re

import discord
import pandas_datareader.data as web
import plotly.graph_objects as go
import yfinance as yf
from discord.ext import commands


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
                diff = dt.timedelta(days=int(range.removesuffix('m')))
            elif years_pattern.match(range):
                diff = dt.timedelta(days=int(range.removesuffix('y')))
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

            end = dt.datetime.now()
            start = end - diff

            stocks = web.DataReader([ticker], 'yahoo', start, end)
            candlestick = go.Figure(data=[go.Candlestick(x=stocks.index,
                                                         open=stocks[('Open', ticker)],
                                                         high=stocks[('High', ticker)],
                                                         low=stocks[('Low', ticker)],
                                                         close=stocks[('Close', ticker)])])

            chart_title = f"Chart of {info['longName']} ({info['symbol']})"
            candlestick.update_layout(xaxis_rangeslider_visible=False, title=chart_title)
            candlestick.update_yaxes(tickprefix='$')

            candlestick.write_image(f"{self.config['stonkmaster']['TmpFolder']}/{info['symbol']}.png")
            with open(f"{self.config['stonkmaster']['TmpFolder']}/{info['symbol']}.png", 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)

            await ctx.send(f"Fia an bessern Graph schaust moi do vorbei: <https://finance.yahoo.com/chart/{info['symbol']}/>")

        except Exception as ex:
            logging.error(ex)
            await ctx.send(f"Do hod wos ned bassd, I bin raus. {self.config['emojis']['Error']}")
