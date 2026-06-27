import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = copy.deepcopy(app_module.activities)


@pytest.fixture
def client():
    return TestClient(app_module.app)


def test_unregister_participant_removes_from_activity(client):
    response = client.delete(
        "/activities/Chess Club/participants/michael@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"

    updated = client.get("/activities").json()
    assert "michael@mergington.edu" not in updated["Chess Club"]["participants"]


def test_unregister_participant_returns_404_for_unknown_participant(client):
    response = client.delete(
        "/activities/Chess Club/participants/not-a-student@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
