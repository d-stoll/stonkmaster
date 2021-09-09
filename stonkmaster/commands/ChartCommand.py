import configparser
import datetime as dt
import logging
import os
import re
import urllib.parse

import discord
import plotly.graph_objects as go
import plotly.io as pio
import requests
import yfinance as yf
from discord.ext import commands
import pandas as pd

pio.templates.default = 'plotly_dark'


def datetime_to_timestamp(datetime):
    return round(dt.datetime.timestamp(datetime))


class ChartCommand(commands.Cog,
                   name="Chart",
                   description="Generates a chart showing the price development of the share in the last months."):
    def __init__(self, bot: commands.Bot, config: configparser.ConfigParser):
        self.bot = bot
        self.config = config
        self.yahooBaseUrl = "https://query2.finance.yahoo.com/v7/finance/download"

    def get_ticker_data(self, ticker: str, start, end, interval):
        response = requests.get(f"{self.yahooBaseUrl}/{urllib.parse.quote(ticker)}", stream=True, params={
            'period1': datetime_to_timestamp(start),
            'period2': datetime_to_timestamp(end),
            'interval': interval
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
                days = int(range.removesuffix('d'))
                diff = dt.timedelta(days=days)
                range_str = f"{days} days" if days > 1 else "day"
            elif months_pattern.match(range):
                months = int(range.removesuffix('m'))
                diff = dt.timedelta(days=months * 30)
                range_str = f"{months} months" if months > 1 else "month"
            elif years_pattern.match(range):
                years = int(range.removesuffix('y'))
                diff = dt.timedelta(days=years * 365)
                range_str = f"{years} years" if years > 1 else "year"
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

            await ctx.send(f"**Generating chart of {symbol} for the last {range_str}... " +
                           f"{self.config['emojis']['Chart']}**")

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

            # ticker_data = yf.download([symbol], group_by="Ticker", start=start, end=end, interval=interval,
            #                          threads=False, prepost=False, rounding=True)

            ticker_data = self.get_ticker_data(symbol, start, end, interval=interval)

            candlestick = go.Figure(data=[go.Candlestick(x=ticker_data['Date'],
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

            path = f"{self.config['stonkmaster']['TmpFolder']}/{info['symbol']}-{range}.png"
            candlestick.write_image(path)
            with open(path, 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)

            os.remove(path)

        except Exception as ex:
            logging.exception(f"Exception in ChartCommand: {ex}")
            await ctx.send(f"Do hod wos ned bassd, I bin raus. {self.config['emojis']['Error']}")
