from fedispam.json_validation import mastodon_status_validation, decisions_validation

from data import TRAINING_DATA


def test_status_validation():
    assert not mastodon_status_validation({})

    status = TRAINING_DATA[0][0].copy()
    assert mastodon_status_validation(status)
    status["sensitive"] = "test"
    assert not mastodon_status_validation(status)
    del status["sensitive"]
    assert not mastodon_status_validation(status)
