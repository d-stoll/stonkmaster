import logging

from discord.ext import commands

from stonkmaster.commands.base import BaseCommand


class ConfigCommand(BaseCommand):
    async def execute(self, ctx: commands.Context, cmd: str, *args: str):
        try:
            if cmd == "set":
                key, value = args
                section, option = ".".split(key)
                if section == "discord.py":
                    await ctx.send(f"Discord.py configurations can not be changed at runtime. "
                                   f"{self.config['emojis']['Error']}")
                else:
                    self.config.set(section, option, value)
                    await ctx.send(f"**Setting {key} to {value}** {self.config['emojis']['Tools']}")
        except Exception as ex:
            logging.exception(f"Exception in ConfigCommand: {ex}")
            await ctx.send(f"Error during execution of command. {self.config['emojis']['Error']}")
