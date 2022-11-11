from unittest.mock import MagicMock

import pytest


@pytest.fixture
def context():
    context = MagicMock()
    return context
