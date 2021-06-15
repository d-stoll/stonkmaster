import pytest

from stonkmaster.commands.SecCommand import SecCommand
from tests.utils import DiscordContextMock


@pytest.mark.asyncio
async def test_sec_gme():
    discord_ctx = DiscordContextMock()
    sec_cmd = SecCommand()

    await sec_cmd.run(ctx=discord_ctx, ticker='gme', type="10-k")

    assert len(discord_ctx.messages) > 0
    assert len(discord_ctx.embeds) > 0
