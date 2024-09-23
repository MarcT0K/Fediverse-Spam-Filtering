import pytest

from fedispam.main import filtering_model

from data import TRAINING_DATA, MODEL_EXPORT, OUTLIAR, FEATURE_COUNTS

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


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

    features = filtering_model._extract_features_from_status(TRAINING_DATA[1][0])
    assert features == {
        "content#56": 1,
        "content#according": 1,
        "content#also": 1,
        "content#announced": 1,
        "content#arab": 1,
        "content#belarus": 1,
        "content#blocklist": 1,
        "content#bloomberg": 1,
        "content#censorship": 1,
        "content#comes": 1,
        "content#company": 1,
        "content#countries": 1,
        "content#democratic": 1,
        "content#egypt": 1,
        "content#emirates": 1,
        "content#eritrea": 1,
        "content#government": 1,
        "content#helping": 1,
        "content#investigations": 1,
        "content#leaving": 1,
        "content#maker": 1,
        "content#mass": 1,
        "content#move": 1,
        "content#new": 1,
        "content#non": 1,
        "content#put": 1,
        "content#sandvine": 1,
        "content#sold": 1,
        "content#surveillance": 1,
        "content#tech": 1,
        "content#u": 1,
        "content#united": 1,
        "content#uzbekistan": 1,
        "media": 0,
        "mentions": 0,
        "sensitive": 0,
        "tag#tech": 1,
        "tag#test": 1,
        "urls#": 1,
    }

    features = filtering_model._extract_features_from_status(TRAINING_DATA[2][0])
    assert features == {
        "content#appears": 1,
        "content#company": 1,
        "content#counting": 1,
        "content#days": 1,
        "content#export": 1,
        "content#related": 1,
        "content#sand": 1,
        "content#totally": 1,
        "content#vine": 1,
        "media": 0,
        "mentions": 1,
        "sensitive": 0,
        "urls#": 0,
    }


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


async def test_filter(test_client):
    resp = await test_client.post("/model/import", json=MODEL_EXPORT)
    assert resp.status_code == 200
    assert resp.json() == {"success": True}
    assert filtering_model.nb_samples == [2, 1]

    resp = await test_client.post("/filter", json=TRAINING_DATA[0][0])
    assert resp.status_code == 200
    assert resp.json() == {"decision": 0, "id": "113171648429213722"}

    resp = await test_client.post("/filter", json=TRAINING_DATA[2][0])
    assert resp.status_code == 200
    assert resp.json() == {"decision": 1, "id": "113171206365051746"}


async def test_outliar(test_client):
    resp = await test_client.post("/model/import", json=MODEL_EXPORT)
    assert resp.status_code == 200
    assert resp.json() == {"success": True}
    assert filtering_model.nb_samples == [2, 1]

    resp = await test_client.get("/outliers")
    assert resp.status_code == 200
    assert resp.json() == []

    resp = await test_client.post("/filter", json=OUTLIAR)
    assert resp.status_code == 200
    assert resp.json() == {"decision": -1, "id": "113181206365051836"}

    resp = await test_client.get("/outliers")
    assert resp.status_code == 200
    assert resp.json() == ["113181206365051836"]

    assert filtering_model.feature_counts == FEATURE_COUNTS
    assert filtering_model.log_posterior is not None
    log_prob_before = filtering_model.log_posterior.copy()

    resp = await test_client.post(
        "/outliers/classify", json=[["113181206365051836", True]]
    )
    assert resp.status_code == 200
    assert resp.json() == {"success": True}
    assert filtering_model.nb_samples == [2, 2]

    assert filtering_model.feature_counts != FEATURE_COUNTS
    assert log_prob_before != filtering_model.log_posterior

    resp = await test_client.get("/outliers")
    assert resp.status_code == 200
    assert resp.json() == []

    resp = await test_client.post("/filter", json=OUTLIAR)
    assert resp.status_code == 200
    assert resp.json() == {"decision": 1, "id": "113181206365051836"}
