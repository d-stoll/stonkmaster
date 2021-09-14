import configparser

import discord
from discord.ext import commands

from stonkmaster.core.market import get_price_and_change
from stonkmaster.tasks.base import BaseTask


class UpdateStatusTask(BaseTask):
    def __init__(self, bot: commands.Bot, config: configparser.ConfigParser):
        super().__init__(bot, config)
        self.current_ticker = "GME"
        self.color_roles = []

    async def loop(self):
        price, change = get_price_and_change(self.current_ticker)
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching,
                                      name=f"{self.current_ticker}: {round(price, 2)}$ ({'{0:+.2f}'.format(change)}%)"))

        for role in self.color_roles:
            color = discord.Color.green() if change >= 0 else discord.Color.red()
            if role.color != color:
                await role.edit(color=color)

    async def before_loop(self):
        await self.bot.wait_until_ready()
        for guild in self.bot.guilds:
            color_role = discord.utils.get(guild.roles, name="Stonkmaster")
            if color_role is None:
                color_role = await guild.create_role(name="Stonkmaster")
            await guild.get_member(self.bot.user.id).add_roles(color_role)
            self.color_roles += [color_role]
