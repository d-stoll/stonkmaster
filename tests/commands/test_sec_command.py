from time import sleep

import discord.ext.commands
import discord.ext.test as dpytest
import pytest

from tests.assertions import discord_message_equals


@pytest.mark.asyncio
async def test_sec_gme(bot: discord.ext.commands.Bot):
    await dpytest.message("$sec GME 8-k")

    assert discord_message_equals("**Searching EDGAR database... :mag_right:**")
    sleep(5)
    assert dpytest.get_embed() is not None
