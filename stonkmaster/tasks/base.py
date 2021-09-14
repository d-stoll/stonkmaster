import configparser
from abc import ABC, abstractmethod

from discord.ext import commands


class BaseTask(ABC):
    def __init__(self, bot: commands.Bot, config: configparser.ConfigParser):
        self.bot = bot
        self.config = config

    @abstractmethod
    async def loop(self):
        pass

    @abstractmethod
    async def before_loop(self):
        pass
