import datetime as dt
import discord
import pandas_datareader.data as web
import plotly.graph_objects as go
import yfinance as yf


class ChartCommand:
    def __init__(self):
        self.emoji_not_found = "<:ThomasPassAuf:788838985878994964>"
        self.emoji_error = ":flag_white:"

    async def run(self, ctx, ticker):
        try:
            yf_ticker = yf.Ticker(ticker)
            info = yf_ticker.info

            if len(info) <= 1:
                await ctx.send(f"{ticker.upper()} gibt's ned oida! {self.emoji_not_found}")
                return

            start = dt.datetime(2021, 1, 1)
            end = dt.datetime.now()

            stocks = web.DataReader([ticker], 'yahoo', start, end)
            candlestick = go.Figure(data=[go.Candlestick(x=stocks.index,
                                                         open=stocks[('Open', ticker)],
                                                         high=stocks[('High', ticker)],
                                                         low=stocks[('Low', ticker)],
                                                         close=stocks[('Close', ticker)])])

            chart_title = f"Chart of {info['longName']} ({info['symbol']})"
            candlestick.update_layout(xaxis_rangeslider_visible=False, title=chart_title)
            candlestick.update_yaxes(tickprefix='$')

            candlestick.write_image(f"/tmp/{info['symbol']}.png")
            with open(f"/tmp/{info['symbol']}.png", 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)

            await ctx.send(f"Fia an bessern Graph schaust moi do vorbei: <https://finance.yahoo.com/chart/{info['symbol']}/>")

        except Exception as ex:
            print(ex)
            await ctx.send(f"Do hod wos ned bassd, I bin raus. {self.emoji_error}")
