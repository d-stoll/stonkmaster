import yfinance as yf


class ShortsCommand:
    def __init__(self):
        self.emoji_no_short = "<:GanslSuffkoma:819901005193019392>"
        self.emoji_error = "<:ThomasPassAuf:788838985878994964>"
        self.emoji_kennyg = "<:kennyg:852146613220933653>"

    async def run(self, ctx, arg):
        try:
            ticker = yf.Ticker(arg)
            info = ticker.info
            symbol = info['symbol']

            if 'sharesShort' not in info or 'shortPercentOfFloat' not in info:
                await ctx.send(f"{symbol} ko ned geshorted werdn, du Hosnbiesla! {self.emoji_no_short}")
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
                msg = msg + f" This corresponds to **{short_percent_of_float}%** of available shares."

            await ctx.send(msg)

            if symbol == 'GME' or symbol == 'AMC':
                await ctx.send(f"Real SI may be much higher -> Hedgies are fucked. {self.emoji_kennyg}")
        except:
            await ctx.send(f"{arg.upper()} gibt's ned oida! {self.emoji_error}")
