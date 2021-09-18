import shutil
import tempfile

import discord.ext.test as dpytest
import pytest
from discord import Intents

from stonkmaster.core.bot import create_bot
from stonkmaster.core.config import get_config
from stonkmaster.core.setup import create_data_dir, delete_data_dir


@pytest.fixture
def config():
    conf = get_config([])
    tmp_dir = tempfile.mkdtemp()
    conf['stonkmaster']['TmpFolder'] = tmp_dir
    return conf


@pytest.fixture
def bot(config, event_loop):
    delete_data_dir(config)
    create_data_dir(config)
    bot = create_bot(config, intents=Intents(members=True), loop=event_loop)
    dpytest.configure(bot)
    return bot


@pytest.fixture
def cleanup(config):
    yield
    shutil.rmtree(config['stonkmaster']['TmpFolder'])