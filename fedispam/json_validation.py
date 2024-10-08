# Reference https://docs.joinmastodon.org/entities/Status/


def mastodon_status_validation(status):
    """Minimal status validation checking the existence of useful fields"""
    try:
        assert isinstance(status, dict)
        assert isinstance(status["id"], str)
        assert isinstance(status["content"], str)
        assert isinstance(status["spoiler_text"], str)
        assert isinstance(status["media_attachments"], list)
        assert isinstance(status["tags"], list)
        assert isinstance(status["mentions"], list)
        assert isinstance(status["sensitive"], bool)
        assert isinstance(status["language"], str)
    except (AssertionError, KeyError):
        return False

    return True


def decisions_validation(list_of_decisions):
    """Minimal validation to check the list of decisions"""

    try:
        assert isinstance(list_of_decisions, list)
        for tup in list_of_decisions:
            assert isinstance(tup, list)
            assert len(tup) == 2
            obj_id, decision = tup
            assert isinstance(obj_id, str)
            assert decision in [0, 1]
    except AssertionError:
        return False

    return True


def model_validation(model):
    """Minimal validation to check the model"""
    try:
        assert isinstance(model, dict)
        assert "nb_samples" in model
        assert "feature_counts" in model
        assert isinstance(model["nb_samples"], list)
        assert len(model["nb_samples"]) == 2
        assert isinstance(model["feature_counts"], dict)
    except AssertionError:
        return False

    return True
