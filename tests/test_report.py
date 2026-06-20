from fastapi.testclient import TestClient
from app.database.setup_db import get_db
from tests.test_db import override_get_db
from tests.helpers import create_workout_test
from app.main import app

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_get_report_pending():
    workout_data = create_workout_test()
    headers ={
        "Authorization": f"Bearer {workout_data['token']}"
    }

    response = client.get(
        "/report",headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_workout"] == 1
    assert data["pending_workout"] == 1
    assert data["completed_workout"] == 0
    assert data["cancelled_workout"] == 0

def test_get_report_completed():
    workout_data = create_workout_test()
    headers ={
        "Authorization": f"Bearer {workout_data['token']}"
    }
    update_response = client.put(
        f"/workout/{workout_data['id_workout']}/status",
        json={
            "status": "completed"
        },headers=headers
    )
    assert update_response.status_code == 200

    response = client.get(
        "/report",headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_workout"] == 1
    assert data["pending_workout"] == 0
    assert data["completed_workout"] == 1
    assert data["cancelled_workout"] == 0