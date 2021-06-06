import datetime as dt
import discord
import pandas_datareader.data as web
import plotly.graph_objects as go
import yfinance as yf


class ChartCommand:
    def __init__(self):
        self.emoji_error = "<:ThomasPassAuf:788838985878994964>"

    async def run(self, ctx, arg):
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

            await ctx.send("Fia an bessern Graph schaust moi do vorbei: <https://finance.yahoo.com/chart/GME/>")

        except:
            await ctx.send(f"{arg.upper()} gibt's ned oida! {self.emoji_error}")