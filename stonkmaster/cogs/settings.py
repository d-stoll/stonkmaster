import configparser

from discord.ext import commands

from stonkmaster.cogs.base import BaseCog
from stonkmaster.commands.config import ConfigCommand


class SettingsCog(BaseCog, name="Setting Commands"):

    def __init__(self, bot: commands.Bot, config: configparser.ConfigParser):
        super().__init__(bot, config)
        self.config_command = ConfigCommand(self.config)

    @commands.command(name="config")
    async def _config(self, ctx: commands.Context, cmd: str, *args: str):
        """Manage internal configurations of the bot."""
        await self.config_command.execute(ctx, cmd, *args)