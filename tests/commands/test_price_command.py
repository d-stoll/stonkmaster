import discord.ext.test as dpytest
import pytest

from stonkmaster.util.market_utils import is_market_closed
from tests.assertions import discord_message_matches, discord_message_equals


@pytest.mark.asyncio
async def test_price_gme(bot):
    await dpytest.message("$price GME")

    matching_regex = ("The market price of \\*\\*GameStop Corp\\. \\(GME\\)\\*\\* is \\*\\*\\d+(\\.\\d{1,2})?"
                      "\\$\\*\\* \\((\\+|\\-)\\d+\\.\\d{1,2}\\%\\).*"
                      )
    assert discord_message_matches(matching_regex)

    if is_market_closed():
        assert discord_message_equals("Market is currently **closed** :lock:")
    else:
        assert discord_message_equals("Wennst ned woasd, wannst GME vakaffa wuisd, kosd de do orientiern: " +
                                        "<https://gmefloor.com/> :moneybag:")
        assert discord_message_equals("Weitere Infos findst do: <https://gme.crazyawesomecompany.com/> :bulb:")


@pytest.mark.asyncio
async def test_price_amc(bot):
    await dpytest.message("$price AMC")

    matching_regex = ("The market price of \\*\\*AMC Entertainment Holdings, Inc\\. \\(AMC\\)\\*\\* is \\*\\*"
                      "\\d+(\\.\\d{1,2})?\\$\\*\\* \\((\\+|\\-)\\d+\\.\\d{1,2}\\%\\).*"
                      )
    assert discord_message_matches(matching_regex)

    if is_market_closed():
        assert discord_message_equals("Market is currently **closed** :lock:")
