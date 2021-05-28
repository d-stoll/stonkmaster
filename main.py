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
        long_name = ticker.info['longName']
        symbol = ticker.info['symbol']
        change = ((current - previous) / previous) * 100
        emoji = "<:stonks:785565572300800050>" if change >= 0 else "<:stonks:785565572300800050>"
        msg = (f"The market price of **{long_name} ({symbol})** is **{round(current, 2)}$** "
               f"({'{0:+.2f}'.format(change)}%)  {emoji}")
        await ctx.send(msg)
    except:
        await ctx.send(f"{arg.upper()} gibts ned oida! <:ThomasPassAuf:788838985878994964>")


bot.run(os.environ['DISCORD_TOKEN'])