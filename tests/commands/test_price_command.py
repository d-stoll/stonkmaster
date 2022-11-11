import pytest

from stonkmaster.core.market import is_market_closed


@pytest.mark.skip("dpytest is broken")
def test_price_gme(context, config):
    # cmd = PriceCommand(config)
    # await cmd.execute(context, "GME")

    # matching_regex = ("The market price of \\*\\*GameStop Corp\\. \\(GME\\)\\*\\* is \\*\\*\\d+(\\.\\d{1,2})?"
    #                  "\\$\\*\\* \\((\\+|\\-)\\d+\\.\\d{1,2}\\%\\).*"
    #                  )
    # assert discord_message_matches(matching_regex)

    if is_market_closed():
        # assert discord_message_equals("Market is currently **closed** :lock:")
        pass
    else:
        # assert discord_message_equals("Wennst ned woasd, wannst GME vakaffa wuisd, kosd de do orientiern: " +
        #                              "<https://gmefloor.com/> :moneybag:")
        # assert discord_message_equals("Weitere Infos findst do: <https://gme.crazyawesomecompany.com/> :bulb:")
        pass


@pytest.mark.skip("dpytest is broken")
def test_price_amc(context, config):
    # cmd = PriceCommand(config)
    # await cmd.execute(context, "AMC")

    # matching_regex = ("The market price of \\*\\*AMC Entertainment Holdings, Inc\\. \\(AMC\\)\\*\\* is \\*\\*"
    #                  "\\d+(\\.\\d{1,2})?\\$\\*\\* \\((\\+|\\-)\\d+\\.\\d{1,2}\\%\\).*"
    #                  )
    # assert discord_message_matches(matching_regex)

    if is_market_closed():
        pass
        # assert discord_message_equals("Market is currently **closed** :lock:")
