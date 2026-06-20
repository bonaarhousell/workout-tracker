from fastapi.testclient import TestClient
from app.database.setup_db import get_db
from tests.test_db import override_get_db
from tests.helpers import get_token, create_workout_test
from app.main import app

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_workout():
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post(
        "/workout",
        json={
            "title": "push day",
            "schedule_at": "2026-06-19T08:30:00",
            "comment": "Chest and triceps"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()
    
    assert data["message"] == "Workout created"
    assert "id_workout" in data


def test_remove_workout():
    workout_data = create_workout_test()
    headers = {
        "Authorization": f"Bearer {workout_data['token']}"
    }
    response = client.delete(
        f"/workout/{workout_data['id_workout']}",headers=headers
    )

    assert response.status_code == 200
    
    data = response.json()

    assert data["message"] == "Workout removed"

def test_workout_to_exercise():
    workout_data = create_workout_test()
    headers = {
        "Authorization": f"Bearer {workout_data['token']}"
    }
    response = client.post(
        f"/workout/{workout_data['id_workout']}/exercise",
        json={
            "id_exercise": 16,
            "sets": 3,
            "reps": 15,
            "weight": 20
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Exercise added succesfully to Workout"

def test_get_workout():
    workout_data = create_workout_test()
    headers = {
        "Authorization": f"Bearer {workout_data['token']}"
    }

    response = client.get(
        "/workout",headers=headers
    )

    assert response.status_code == 200
    
    data = response.json()

    assert len(data) > 0

def test_get_workout_detail():
    workout_data = create_workout_test()
    headers = {
        "Authorization": f"Bearer {workout_data['token']}"
    }
    client.post(
        f"/workout/{workout_data['id_workout']}/exercise",
        json={
            "id_exercise": 3,
            "sets": 4,
            "reps": 20,
            "weight": 40
        },headers=headers
    )
    response = client.get(
        f"/workout/{workout_data['id_workout']}",headers=headers
    )

    assert response.status_code == 200
    
    data = response.json()

    assert len(data["exercise"]) == 1
    assert data["exercise"][0]["sets"] == 4
    assert data["exercise"][0]["reps"] == 20

def test_get_workout_by_status():
    workout_data = create_workout_test()
    headers = {
        "Authorization": f"Bearer {workout_data['token']}"
    }

    response = client.get(
        "/workout/status/pending",headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert any(
        workout["id_workout"] == workout_data["id_workout"]
        for workout in data
    )

def test_update_workout():
    workout_data = create_workout_test()
    headers = {
        "Authorization": f"Bearer {workout_data['token']}"
    }

    response = client.put(
        f"/workout/{workout_data['id_workout']}",
        json={
            "new_title": "Grow arms V2",
            "new_schedule": "2026-06-26T08:30:00",
            "new_comment": "update",
        },
        headers=headers,
    )   

    assert response.status_code == 200
    
    detail = client.get(
        f"/workout/{workout_data['id_workout']}",headers=headers
    )

    data = detail.json()

    assert data["title"] == "Grow arms V2"
    assert data["comment"] == "update"

def test_update_status_workout():
    workout_data = create_workout_test()
    headers = {
        "Authorization": f"Bearer {workout_data['token']}"
    }

    response = client.put(
        f"/workout/{workout_data['id_workout']}/status",
        json={"status": "completed"},
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Status updated!"

    detail = client.get(
        f"/workout/{workout_data['id_workout']}",headers=headers
    )
    print(detail.json())
    data = detail.json()

    assert data["status"] == "completed"
