import logging

import discord
from discord.ext import commands
from secedgar import filings, FilingType

from stonkmaster.commands.base import BaseCommand
from stonkmaster.core.language import get_text
from stonkmaster.core.market import get_info


class SecCommand(BaseCommand):

    async def execute(self, ctx: commands.Context, ticker: str, type: str):
        try:
            type = type.upper()
            info = get_info(ticker)

            if len(info) <= 1:
                logging.info(f"{ctx.author.display_name} tried to request sec filings for invalid ticker '{ticker}'")
                await ctx.send(f"{ticker.upper()} gibt's ned oida! {self.config['emojis']['NotFound']}")
                return

            logging.info(f"{ctx.author.display_name} requests sec filings of type '{type}' for ticker '{ticker}'")
            await ctx.send(f"**Searching EDGAR database... {self.config['emojis']['Search']}**")
            sec_filings = filings(cik_lookup=info['symbol'].lower(), filing_type=FilingType(type),
                                  user_agent="Daniel Stoll (daniel@stoll.cloud)")

            filings_embed = discord.Embed(
                title=f"Latest SEC filings of {info['longName']} ({info['symbol']})",
                description=(f"List of {type} filings recently submitted by {info['longName']} "
                             f"({info['symbol']}) to the United States Securities and Exchange Commission "
                             "(SEC)"),
                color=0x00ff00)
            urls = sec_filings.get_urls()
            logging.info(f"Found {len(urls)} filings of type '{type}' for ticker '{ticker}' requested by " +
                         f"{ctx.author.display_name}")
            for i, url in enumerate(urls[info['symbol'].lower()][:5]):
                accession_number = sec_filings.get_accession_number(url)[:-4]
                html_link = url[:-4] + "-index.html"
                filings_embed.add_field(name=f"{i + 1} - {accession_number}", value=html_link, inline=False)
            await ctx.send(embed=filings_embed)

        except Exception as ex:
            logging.exception(f"Exception in SecCommand: {ex}")
            await ctx.send(get_text("ErrorMsg", self.config).format(self.config['emojis']['Error']))
