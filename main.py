import yfinance as yf
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='$')


@bot.command(name='price')
async def _price(ctx, arg):
    try:
        ticker = yf.Ticker(arg)
        current = ticker.info['regularMarketPrice']
        previous = ticker.info['previousClose']
        change = ((current - previous) / previous) * 100
        sign = "+" if change >= 0 else ""
        msg = (f"The market price of **{ticker.info['longName']} ({ticker.info['symbol']})** is "
               f"**{round(current, 2)}$** ({sign}{round(change, 2)}%)"
               "  <:stonks:785565572300800050>")
        await ctx.send(msg)
    except:
        await ctx.send(f"{arg.upper()} gibts ned oida! <:ThomasPassAuf:788838985878994964>")


bot.run(os.environ['DISCORD_TOKEN'])

# test