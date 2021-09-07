import discord.ext.test as dpytest
import pytest

from discord import Intents

from stonkmaster.core.bot import create_bot
from stonkmaster.core.config import get_config


@pytest.fixture
def bot(event_loop):
    config = get_config(["--config", "../../default.ini"])
    bot = create_bot(config, intents=Intents(members=True), loop=event_loop)
    dpytest.configure(bot)

    return bot
