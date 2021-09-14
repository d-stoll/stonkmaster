import discord.ext.commands
import discord.ext.test as dpytest
import pytest


@pytest.mark.asyncio
async def test_sec_gme(bot: discord.ext.commands.Bot):
    await dpytest.message("$wiki short squeeze")

    assert dpytest.get_embed() is not None
