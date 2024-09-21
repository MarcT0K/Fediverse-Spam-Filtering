from unittest.mock import patch

import pytest

from async_asgi_testclient import TestClient

import fedispam
import fedispam.database
from fedispam.main import app, lifespan, filtering_model

from data import TRAINING_DATA

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


@pytest.fixture
async def test_client(tmp_path):
    with patch.object(fedispam.database, "DB_DIR", str(tmp_path)):
        async with lifespan(app):
            client = TestClient(app)
            yield client


async def test_feature_extraction(test_client):
    features = filtering_model._extract_features_from_status(TRAINING_DATA[0][0])
    assert features == {
        "content#beyond": 1,
        "content#center": 1,
        "content#control": 1,
        "content#efficient": 1,
        "content#emojis": 1,
        "content#features": 1,
        "content#guide": 1,
        "content#ios": 1,
        "content#makes": 1,
        "content#mind": 1,
        "content#never": 1,
        "content#new": 1,
        "content#power": 1,
        "content#quick": 1,
        "content#stuff": 1,
        "content#user": 1,
        "media": 1,
        "mentions": 0,
        "sensitive": 0,
        "tag#cool": 1,
        "tag#test": 1,
        "urls#": 1,
    }


async def test_data_import(test_client):
    resp = await test_client.post("/training_data/import", json=TRAINING_DATA)
    # TODO assert
