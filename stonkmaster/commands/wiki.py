import logging

import discord
import requests
from bs4 import BeautifulSoup

from stonkmaster.commands.base import BaseCommand
from stonkmaster.core.language import get_text


class WikiCommand(BaseCommand):

    async def execute(self, ctx, *keywords):
        try:
            term = "".join(keywords)
            url = f"https://www.investopedia.com/terms/{term[0]}/{term}.asp"
            soup = BeautifulSoup(requests.get(url).text,
                                 "html.parser")
            required_data = None
            for item in soup.select("#mntl-sc-page_1-0"):
                required_data = item.select("p")[0].text.strip()

            if required_data is not None:
                msg = discord.Embed(title=" ".join(keywords).title(), url=url, description=required_data)
                await ctx.send(embed=msg)
                return

            term = "+".join(keywords)
            url = f"https://www.investopedia.com/search?q={term}"
            soup = BeautifulSoup(requests.get(url).text,
                                 "html.parser")
            title = soup.find("h3", id="search-results__title_1-0")
            if title is None:
                await ctx.send(get_text("SearchTermNotFound", self.config).format(self.config['emojis']['NotFound']))
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
            await ctx.send(get_text("ErrorMsg", self.config).format(self.config['emojis']['Error']))
