import discord.ext.commands
import pytest


@pytest.mark.skip("dpytest is broken")
def test_wiki_direct(bot: discord.ext.commands.Bot):
    # await dpytest.message("$wiki short squeeze")
    pass
    # assert dpytest.get_embed() is not None


@pytest.mark.skip("dpytest is broken")
def test_wiki_search(bot: discord.ext.commands.Bot):
    # await dpytest.message("$wiki implied volatility")
    pass
    # assert dpytest.get_embed() is not None
