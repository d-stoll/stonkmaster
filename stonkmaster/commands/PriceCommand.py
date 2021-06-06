import yfinance as yf
from stonkmaster.util.market_utils import is_market_closed


class PriceCommand:
    def __init__(self):
        self.emoji_up = "<:stonks:785565572300800050>"
        self.emoji_down = "<:notstonks:847892457138946128>"
        self.emoji_error = "<:ThomasPassAuf:788838985878994964>"

    async def run(self, ctx, arg):
        try:
            ticker = yf.Ticker(arg)
            info = ticker.info
            current = info['regularMarketPrice']
            previous = info['previousClose']
            symbol = info['symbol']
            change = ((current - previous) / previous) * 100
            emoji = self.emoji_up if change >= 0 else self.emoji_down


            if 'longName' in info:
                msg = (f"The market price of **{info['longName']} ({symbol})** is **{round(current, 2)}$** "
                       f"({'{0:+.2f}'.format(change)}%)  {emoji}")
            else:
                msg = (f"The market price of **{symbol}** is **{round(current, 2)}$** "
                       f"({'{0:+.2f}'.format(change)}%)  {emoji}")

            await ctx.send(msg)

            if is_market_closed():
                await ctx.send("Market is currently **closed**")
            elif symbol == 'GME':
                await ctx.send("Wennst ned woasd, wannst GME vakaffa wuisd, kosd de do orientiern: <https://gmefloor.com/>")
        except:
            await ctx.send(f"{arg.upper()} gibt's ned oida! {self.emoji_error}")
