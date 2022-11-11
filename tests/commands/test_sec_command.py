from time import sleep

import pytest


@pytest.mark.skip("dpytest is broken")
def test_sec_gme():
    # await dpytest.message("$sec GME 8-k")

    # assert discord_message_equals("**Searching EDGAR database... :mag_right:**")
    sleep(5)
    # assert dpytest.get_embed() is not None
