import configparser
import logging

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands


class WikiCommand(commands.Cog,
                  name="Wiki",
                  description="Searches investopedia for a definition of the keyword."):
    def __init__(self, bot: commands.Bot, config: configparser.ConfigParser):
        self.bot = bot
        self.config = config

    @commands.command(name="wiki")
    async def _wiki(self, ctx, *keywords):
        try:

            term = "".join(keywords)
            url = f"https://www.investopedia.com/terms/{term[0]}/{term}.asp"
            soup = BeautifulSoup(requests.get(url).text,
                                 "html.parser")
            for item in soup.select("#mntl-sc-page_1-0"):
                required_data = item.select("p")[0].text.strip()

            msg = discord.Embed(title=" ".join(keywords).title(), url=url, description=required_data)
            await ctx.send(embed=msg)

        except Exception as ex:
            logging.exception(f"Exception in WikiCommand: {ex}")
            await ctx.send(f"Do hod wos ned bassd, I bin raus. {self.config['emojis']['Error']}")
            await ctx.send(
                f"Check eventuell no amoi dein Suchterm ob. {self.config['emojis']['Error']} oder schau selber noch "
                f"du faule Sau: <https://www.investopedia.com/>")
