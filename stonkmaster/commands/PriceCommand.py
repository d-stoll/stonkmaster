import configparser

import yfinance as yf
from discord.ext import commands

from stonkmaster.util.market_utils import is_market_closed


class PriceCommand(commands.Cog):
    def __init__(self, bot: commands.Bot, config: configparser.ConfigParser):
        self.bot = bot
        self.config = config
        self.emoji_up = "<:stonks:785565572300800050>"
        self.emoji_down = "<:notstonks:847892457138946128>"
        self.emoji_not_found = "<:ThomasPassAuf:788838985878994964>"
        self.emoji_error = ":flag_white:"
        self.emoji_closed = ":lock:"
        self.emoji_money = ":moneybag:"
        self.emoji_bulb = ":bulb:"

    @commands.command(name="price",
                      description="Shows the current price of the stonk, as well as its daily change.")
    async def _price(self, ctx, ticker):
        try:
            yf_ticker = yf.Ticker(ticker)
            info = yf_ticker.info

            if len(info) <= 1:
                await ctx.send(f"{ticker.upper()} gibt's ned oida! {self.emoji_not_found}")
                return

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
                await ctx.send(f"Market is currently **closed** {self.emoji_closed}")
            elif symbol == 'GME':
                await ctx.send(f"Wennst ned woasd, wannst GME vakaffa wuisd, kosd de do orientiern: <https://gmefloor.com/> {self.emoji_money}")
                await ctx.send(f"Weitere Infos findst do: <https://gme.crazyawesomecompany.com/> {self.emoji_bulb}")

        except Exception as ex:
            print(ex)
            await ctx.send(f"Do hod wos ned bassd, I bin raus. {self.emoji_error}")
