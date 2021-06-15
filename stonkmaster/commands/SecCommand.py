import discord
import yfinance as yf
from secedgar.filings import Filing, FilingType


class SecCommand:
    def __init__(self):
        self.emoji_error = "<:ThomasPassAuf:788838985878994964>"
        self.emoji_search = ":mag_right:"

    async def run(self, ctx, ticker, type):
        try:
            await ctx.send(f"**Searching EDGAR database...  {self.emoji_search}**")
            yf_ticker = yf.Ticker(ticker)
            filings = Filing(cik_lookup=yf_ticker.info['symbol'].lower(), filing_type=FilingType(type))

            filings_embed = discord.Embed(
                title=f"Latest SEC filings of {yf_ticker.info['longName']} ({yf_ticker.info['symbol']})",
                description=(f"List of {type} filings recently submitted by {yf_ticker.info['longName']} "
                             f"({yf_ticker.info['symbol']}) to the United States Securities and Exchange Commission "
                             "(SEC)"),
                color=0x00ff00)
            urls = filings.get_urls()
            for i, url in enumerate(urls[yf_ticker.info['symbol'].lower()][:5]):
                accession_number = filings.get_accession_number(url).removesuffix(".txt")
                html_link = url.removesuffix(".txt") + "-index.html"
                filings_embed.add_field(name=f"{i + 1} - {accession_number}", value=html_link, inline=False)
            await ctx.send(embed=filings_embed)
        except:
            await ctx.send(f"{ticker.upper()} gibt's ned oida! {self.emoji_error}")
