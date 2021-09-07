import configparser
import logging

import discord
import yfinance as yf
from discord.ext import commands
from secedgar.filings import Filing, FilingType


class SecCommand(commands.Cog, name="SEC", description="Fetches the latest SEC company filings from EDGAR."):
    def __init__(self, bot: commands.Bot, config: configparser.ConfigParser):
        self.bot = bot
        self.config = config

    @commands.command(name="sec")
    async def _sec(self, ctx, ticker, type):
        try:
            yf_ticker = yf.Ticker(ticker)
            type = type.lower()
            info = yf_ticker.info

            if len(info) <= 1:
                logging.info(f"{ctx.author.display_name} tried to request sec filings for invalid ticker '{ticker}'")
                await ctx.send(f"{ticker.upper()} gibt's ned oida! {self.config['emojis']['NotFound']}")
                return

            logging.info(f"{ctx.author.display_name} requests sec filings of type '{type}' for ticker '{ticker}'")
            await ctx.send(f"**Searching EDGAR database... {self.config['emojis']['Search']}**")
            filings = Filing(cik_lookup=yf_ticker.info['symbol'].lower(), filing_type=FilingType(type))

            filings_embed = discord.Embed(
                title=f"Latest SEC filings of {yf_ticker.info['longName']} ({yf_ticker.info['symbol']})",
                description=(f"List of {type} filings recently submitted by {yf_ticker.info['longName']} "
                             f"({yf_ticker.info['symbol']}) to the United States Securities and Exchange Commission "
                             "(SEC)"),
                color=0x00ff00)
            urls = filings.get_urls()
            logging.info(f"Found {len(urls)} filings of type '{type}' for ticker '{ticker}' requested by " +
                         f"{ctx.author.display_name}")
            for i, url in enumerate(urls[yf_ticker.info['symbol'].lower()][:5]):
                accession_number = filings.get_accession_number(url)[:-4]
                html_link = url[:-4] + "-index.html"
                filings_embed.add_field(name=f"{i + 1} - {accession_number}", value=html_link, inline=False)
            await ctx.send(embed=filings_embed)

        except Exception as ex:
            logging.error(ex)
            await ctx.send(f"Do hod wos ned bassd, I bin raus. {self.config['emojis']['Error']}")
