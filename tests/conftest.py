from unittest.mock import patch

import pytest

from async_asgi_testclient import TestClient

import fedispam.database
from fedispam.filter import SpamFilter
from fedispam.main import app, lifespan, filtering_model


@pytest.fixture
async def test_client(tmp_path):
    with patch.object(fedispam.database, "DB_DIR", str(tmp_path)):
        global filtering_model
        filtering_model = SpamFilter()
        async with lifespan(app):
            client = TestClient(app)
            yield client
