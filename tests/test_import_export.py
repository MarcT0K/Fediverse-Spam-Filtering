import pytest

from fedispam.main import filtering_model

from data import TRAINING_DATA, MODEL_EXPORT

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


async def test_data_import(test_client):
    resp = await test_client.post("/training_data/import")
    assert resp.json() == {"success": False, "error": "Missing data"}
    assert resp.status_code == 400

    resp = await test_client.post("/training_data/import", json=["Invalid", "input"])
    assert resp.json() == {"success": False, "error": "Invalid data format"}
    assert resp.status_code == 400

    resp = await test_client.post(
        "/training_data/import", json=[[{"Invalid": "status"}, 0]]
    )
    assert resp.json() == {"success": False, "error": "Invalid data format"}
    assert resp.status_code == 400

    assert filtering_model.nb_samples == [0, 0]
    assert filtering_model.log_posterior is not None
    log_prob_before = filtering_model.log_posterior.copy()

    resp = await test_client.post("/training_data/import", json=TRAINING_DATA)
    assert resp.json() == {"success": True}
    assert resp.status_code == 200

    assert filtering_model.nb_samples == [2, 1]
    assert log_prob_before != filtering_model.log_posterior


async def test_model_export(test_client):
    resp = await test_client.get("/model/export")
    assert resp.status_code == 200
    assert resp.json() == {
        "feature_counts": {},
        "nb_samples": [
            0,
            0,
        ],
    }

    resp = await test_client.post("/training_data/import", json=TRAINING_DATA)
    assert resp.json() == {"success": True}
    assert resp.status_code == 200

    assert filtering_model.nb_samples == [2, 1]

    resp = await test_client.get("/model/export")
    assert resp.status_code == 200
    assert resp.json() == MODEL_EXPORT


async def test_model_import(test_client):
    assert filtering_model.nb_samples == [0, 0]
    resp = await test_client.post(
        "/model/import",
        json={},
    )
    assert resp.status_code == 400
    assert resp.json() == {"error": "Invalid model", "success": False}
    assert filtering_model.nb_samples == [0, 0]

    assert filtering_model.nb_samples == [0, 0]
    resp = await test_client.post(
        "/model/import",
        json={
            "feature_counts": {},
            "nb_samples": [
                0,
                0,
            ],
        },
    )
    assert resp.status_code == 200
    assert resp.json() == {"success": True}
    assert filtering_model.nb_samples == [0, 0]

    resp = await test_client.post("/model/import", json=MODEL_EXPORT)
    assert resp.status_code == 200
    assert resp.json() == {"success": True}
    assert filtering_model.nb_samples == [2, 1]
