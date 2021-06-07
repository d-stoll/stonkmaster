import re
import pytest
from stonkmaster.commands.PriceCommand import PriceCommand
from stonkmaster.util.market_utils import is_market_closed
from tests.utils import DiscordContextMock


@pytest.mark.asyncio
async def test_price_gme():
    discord_ctx = DiscordContextMock()
    price_cmd = PriceCommand()

    await price_cmd.run(ctx=discord_ctx, arg="GME")
    matching_regex = ("The market price of \\*\\*GameStop Corp\\. \\(GME\\)\\*\\* is \\*\\*\\d+\\.\\d{1,2}\\$\\*\\* "
                      "\\((\\+|\\-)\\d+\\.\\d{1,2}\\%\\).*"
                      )
    if is_market_closed():
        assert discord_ctx.messages.pop() == "Market is currently **closed**"
    else:
        gme_special_msg = "Wennst ned woasd, wannst GME vakaffa wuisd, kosd de do orientiern: <https://gmefloor.com/>"
        assert gme_special_msg == discord_ctx.messages.pop()

    assert re.match(matching_regex, discord_ctx.messages.pop())


@pytest.mark.asyncio
async def test_price_amc():
    discord_ctx = DiscordContextMock()
    price_cmd = PriceCommand()

    await price_cmd.run(ctx=discord_ctx, arg="AMC")
    matching_regex = ("The market price of \\*\\*AMC Entertainment Holdings, Inc\\. \\(AMC\\)\\*\\* is \\*\\*"
                      "\\d+\\.\\d{1,2}\\$\\*\\* \\((\\+|\\-)\\d+\\.\\d{1,2}\\%\\).*"
                      )

    if is_market_closed():
        assert discord_ctx.messages.pop() == "Market is currently **closed**"

    assert re.match(matching_regex, discord_ctx.messages.pop())
