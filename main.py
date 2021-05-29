import yfinance as yf
from discord.ext import commands
import os
import datetime as dt
import pandas_datareader.data as web
import plotly.graph_objects as go
import discord

bot = commands.Bot(command_prefix='$')


@bot.command(name='price')
async def _price(ctx, arg):
    try:
        ticker = yf.Ticker(arg)
        info = ticker.info
        current = info['regularMarketPrice']
        previous = info['previousClose']
        symbol = info['symbol']
        change = ((current - previous) / previous) * 100
        emoji = "<:stonks:785565572300800050>" if change >= 0 else "<:notstonks:847892457138946128>"

        if 'longName' in info:
            msg = (f"The market price of **{info['longName']} ({symbol})** is **{round(current, 2)}$** "
                   f"({'{0:+.2f}'.format(change)}%)  {emoji}")
        else:
            msg = (f"The market price of **{symbol}** is **{round(current, 2)}$** "
                   f"({'{0:+.2f}'.format(change)}%)  {emoji}")

        await ctx.send(msg)
        if symbol == 'GME':
            await ctx.send("Wennst ned woast, wannst GME vakaffa wuisd, kosd de do orientiern: https://gmefloor.com/")
    except:
        await ctx.send(f"{arg.upper()} gibts ned oida! <:ThomasPassAuf:788838985878994964>")


@bot.command(name='shorts')
async def _shorts(ctx, arg):
    try:
        ticker = yf.Ticker(arg)
        info = ticker.info
        symbol = info['symbol']

        if 'sharesShort' not in info or 'shortPercentOfFloat' not in info:
            await ctx.send(f"{symbol} ko ned geshorted werdn, du Hosnbiesla! <:GanslSuffkoma:819901005193019392>")
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
            msg = msg + f" This corresponds to **{short_percent_of_float}%** of shares available."

        await ctx.send(msg)

        if symbol == 'GME' or symbol == 'AMC':
            await ctx.send("Real SI may be much higher -> Hedgies are fucked.")
    except:
        await ctx.send(f"{arg.upper()} gibts ned oida! <:ThomasPassAuf:788838985878994964>")


@bot.command(name='chart')
async def _chart(ctx, arg):
    try:
        start = dt.datetime(2021, 1, 1)
        end = dt.datetime.now()

        stocks = web.DataReader([arg], 'yahoo', start, end)
        candlestick = go.Figure(data=[go.Candlestick(x=stocks.index,
                                                     open=stocks[('Open', arg)],
                                                     high=stocks[('High', arg)],
                                                     low=stocks[('Low', arg)],
                                                     close=stocks[('Close', arg)])])

        stock = yf.Ticker(arg)
        info = stock.info
        chart_title = f"Chart of {info['longName']} ({info['symbol']})"
        candlestick.update_layout(xaxis_rangeslider_visible=False, title=chart_title)
        candlestick.update_yaxes(tickprefix='$')

        candlestick.write_image(f"/tmp/the-stonk-master/{info['symbol']}.png")
        with open(f"/tmp/the-stonk-master/{info['symbol']}.png", 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)

    except:
        await ctx.send(f"{arg.upper()} gibts ned oida! <:ThomasPassAuf:788838985878994964>")


bot.run(os.environ['DISCORD_TOKEN'])
