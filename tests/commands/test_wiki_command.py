import discord.ext.commands
import discord.ext.test as dpytest
import pytest


@pytest.mark.asyncio
async def test_wiki_direct(bot: discord.ext.commands.Bot):
    await dpytest.message("$wiki short squeeze")

    assert dpytest.get_embed() is not None


@pytest.mark.asyncio
async def test_wiki_search(bot: discord.ext.commands.Bot):
    await dpytest.message("$wiki implied volatility")

    assert dpytest.get_embed() is not None
