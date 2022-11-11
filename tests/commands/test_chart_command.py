import os
from time import sleep

import pytest


@pytest.mark.skip(reason="Kaleido does not work in Github workflow'")
def test_chart_gme(bot, config):
    chart_file_path = f"{config['stonkmaster']['TmpFolder']}/GME-3m.png"

    if os.path.isfile(chart_file_path):
        os.remove(chart_file_path)

    # wait dpytest.message("$chart GME 3m")
    sleep(5)

    assert os.path.isfile(chart_file_path)
