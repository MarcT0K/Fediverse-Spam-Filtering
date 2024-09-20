from unittest.mock import patch

import pytest

from async_asgi_testclient import TestClient

import fedispam
import fedispam.database
from fedispam.main import app, lifespan, filtering_model
from fedispam.json_validation import mastodon_status_validation, decisions_validation

from data import TRAINING_DATA

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


@pytest.fixture
async def test_client(tmp_path):
    with patch.object(fedispam.database, "DB_DIR", str(tmp_path)):
        async with lifespan(app):
            client = TestClient(app)
            yield client


def test_status_validation():
    assert not mastodon_status_validation({})

    status = TRAINING_DATA[0][0].copy()
    assert mastodon_status_validation(status)
    status["sensitive"] = "test"
    assert not mastodon_status_validation(status)
    del status["sensitive"]
    assert not mastodon_status_validation(status)


async def test_feature_extraction(test_client):
    features = filtering_model._extract_features_from_status(TRAINING_DATA[0][0])
    assert features == {}


async def test_data_import(test_client):
    resp = await test_client.post("/training_data/import", json=TRAINING_DATA)
    # TODO assert
