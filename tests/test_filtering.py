from unittest.mock import patch

import pytest

from async_asgi_testclient import TestClient

import fedispam
import fedispam.database
from fedispam.main import app, lifespan

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


@pytest.fixture
async def mock_app(tmp_path):
    with patch.object(fedispam.database, "DB_DIR", str(tmp_path)):
        async with lifespan(app):
            yield


async def test_app(mock_app):
    client = TestClient(app)
