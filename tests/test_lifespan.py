from unittest.mock import patch

import pytest

from async_asgi_testclient import TestClient


import fedispam.database
from fedispam.main import app, lifespan, filtering_model

from data import MODEL_EXPORT

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


async def test_start_and_stop(tmp_path):
    with patch.object(fedispam.database, "DB_DIR", str(tmp_path)):
        async with lifespan(app):
            client = TestClient(app)

            model_db_content = filtering_model.model_db.extract_db()
            assert model_db_content == {}

            resp = await client.post("/model/import", json=MODEL_EXPORT)
            assert resp.status_code == 200
            assert resp.json() == {"success": True}
            assert filtering_model.nb_samples == [2, 1]

            model_db_content = filtering_model.model_db.extract_db()
            assert model_db_content != {}

            feature_counts_before_stop = filtering_model.feature_counts.copy()
            assert feature_counts_before_stop != {}

            prob_before_stop = filtering_model.log_posterior
            assert prob_before_stop != {}

        # Simulate system reboot (i.e., reset to default values)
        filtering_model.log_prior = None
        filtering_model.log_posterior = None
        filtering_model.log_default_prob = None
        filtering_model.nb_samples = None
        filtering_model.feature_counts = None

        async with lifespan(app):
            recovered_model_db_content = filtering_model.model_db.extract_db()
            # Verify that we recover the pre-shutdown state
            assert recovered_model_db_content == model_db_content
            assert filtering_model.nb_samples == [2, 1]
            assert filtering_model.feature_counts == feature_counts_before_stop
            assert filtering_model.log_posterior == prob_before_stop
