import yfinance as yf
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='$')


@bot.command(name='price')
async def _price(ctx, arg):
    try:
        ticker = yf.Ticker(arg)
        await ctx.send(
            f"The market price of **{ticker.info['longName']} ({ticker.info['symbol']})** is **{round(ticker.info['regularMarketPrice'], 2)}$**  <:stonks:785565572300800050>")
    except:
        await ctx.send(f"{arg.upper()} gibts ned oida?! <:ThomasPassAuf:788838985878994964>")

bot.run(os.environ['DISCORD_TOKEN'])
