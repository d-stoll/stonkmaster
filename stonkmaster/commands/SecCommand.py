import discord
import yfinance as yf
from secedgar.filings import Filing, FilingType


class SecCommand:
    def __init__(self):
        self.emoji_error = "<:ThomasPassAuf:788838985878994964>"
        self.emoji_search = ":mag_right:"

    async def run(self, ctx, ticker, type):
        try:
            await ctx.send(f"**Searching EDGAR database... {self.emoji_search}**")
            yf_ticker = yf.Ticker(ticker)
            filings = Filing(cik_lookup=yf_ticker.info['symbol'], filing_type=FilingType(type))

            filings_embed = discord.Embed(title=f"SEC filings for {yf_ticker.info['longName']}({yf_ticker.info['symbol']})",
                                      color=0x00ff00)
            urls = filings.get_urls()
            for i, url in enumerate(urls[yf_ticker.info['symbol']][:5]):
                filings_embed.add_field(name=f"{i}:", value=url, inline=False)
            await ctx.send(embed=filings_embed)
        except:
            await ctx.send(f"{ticker.upper()} gibt's ned oida! {self.emoji_error}")