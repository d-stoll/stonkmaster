import configparser
import datetime as dt
import logging
import re
import urllib.parse

import discord
import plotly.graph_objects as go
import pandas as pd
import requests
import yfinance as yf
from discord.ext import commands

yf.pdr_override()


def datetime_to_timestamp(datetime):
    return round(dt.datetime.timestamp(datetime))


class ChartCommand(commands.Cog,
                   name="Chart",
                   description="Generates a chart showing the price development of the share in the last months."):
    def __init__(self, bot: commands.Bot, config: configparser.ConfigParser):
        self.bot = bot
        self.config = config
        self.yahooBaseUrl = "https://query1.finance.yahoo.com/v7/finance/download"

    def get_ticker_data(self, ticker: str, start, end):
        response = requests.get(f"{self.yahooBaseUrl}/{urllib.parse.quote(ticker)}", stream=True, params={
            'period1': datetime_to_timestamp(start),
            'period2': datetime_to_timestamp(end),
            'interval': '1d',
            'frequency': '1d',
            'events': 'history'
        }, headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 ' +
                          '(KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36'
        })
        response.raise_for_status()
        return pd.read_csv(response.raw)

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

            ticker_data = self.get_ticker_data(symbol, start, end)
            candlestick = go.Figure(data=[go.Candlestick(x=ticker_data['Date'],
                                                         open=ticker_data['Open'],
                                                         high=ticker_data['High'],
                                                         low=ticker_data['Low'],
                                                         close=ticker_data['Close'])])

            chart_title = f"{info['longName']} ({info['symbol']})"
            candlestick.update_layout(xaxis_rangeslider_visible=False, title=chart_title)
            candlestick.update_yaxes(tickprefix='$')

            candlestick.write_image(f"{self.config['stonkmaster']['TmpFolder']}/{info['symbol']}-{range}.png")
            with open(f"{self.config['stonkmaster']['TmpFolder']}/{info['symbol']}-{range}.png", 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)

            await ctx.send(f"Fia an bessern Graph schaust moi do vorbei: <https://finance.yahoo.com/chart/{info['symbol']}/>")

        except Exception as ex:
            logging.error(ex)
            await ctx.send(f"Do hod wos ned bassd, I bin raus. {self.config['emojis']['Error']}")
