import configparser

from discord.ext import commands

from stonkmaster.cogs.base import BaseCog
from stonkmaster.commands.sec import SecCommand
from stonkmaster.commands.shorts import ShortsCommand
from stonkmaster.commands.wiki import WikiCommand


class ResearchCog(BaseCog, name="Research Commands"):

    def __init__(self, bot: commands.Bot, config: configparser.ConfigParser):
        super().__init__(bot, config)
        self.shorts_command = ShortsCommand(self.config)
        self.sec_command = SecCommand(self.config)
        self.wiki_command = WikiCommand(self.config)

    @commands.command(name="shorts")
    async def _shorts(self, ctx, ticker: str):
        """Provides currently known information on how heavily the stock is shorted."""
        await self.shorts_command.execute(ctx, ticker)

    @commands.command(name="sec")
    async def _sec(self, ctx: commands.Context, ticker: str, type: str):
        """Fetches the latest SEC company filings from EDGAR."""
        await self.sec_command.execute(ctx, ticker, type)

    @commands.command(name="wiki")
    async def _wiki(self, ctx: commands.Context, *keywords):
        """Searches investopedia for a definition of the term."""
        await self.wiki_command.execute(ctx, keywords)
