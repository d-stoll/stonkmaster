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

            term = "+".join(keywords)
            url = f"https://www.investopedia.com/search?q={term}"
            soup = BeautifulSoup(requests.get(url).text,
                                 "html.parser")
            title = soup.find("h3", id="search-results__title_1-0")
            if title is None:
                await ctx.send(
                    f"Check no amoi dein Suchterm ob oder schau selber noch du faule Sau: "
                    f"<https://www.investopedia.com/> {self.config['emojis']['NotFound']}")
                return

            url = soup.find("div", id="search-results__url_1-0").text.strip()
            soup = BeautifulSoup(requests.get(url).text,
                                 "html.parser")

            required_data = None
            for item in soup.select("#mntl-sc-page_1-0"):
                required_data = item.select("p")[0].text.strip()

            msg = discord.Embed(title=title.text.strip(), url=url, description=required_data)
            await ctx.send(embed=msg)

        except Exception as ex:
            logging.exception(f"Exception in WikiCommand: {ex}")
            await ctx.send(f"Do hod wos ned bassd, I bin raus. {self.config['emojis']['Error']}")
