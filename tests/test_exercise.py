from app.main import app
from app.database.setup_db import get_db
from fastapi.testclient import TestClient
from tests.test_db import override_get_db
from tests.helpers import get_token, get_token_admin

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_exercise_role_user():
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post(
        "/exercise",
        json={
            "title": "Abdominal Brace",
            "description": "Core exercise",
            "category": "Core"
        },headers=headers
    )

    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == "only admin can create exercise!"
    assert "id_exercise" not in data

def test_create_exercise_role_admin():
    token = get_token_admin()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post(
        "/exercise",
        json={
            "title": "Abdominal Brace",
            "description": "Core exercise",
            "category": "Core"
        },headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Exercise created"
    assert "id_exercise" in data

def test_list_exercise():
    
    response = client.get(
        "/exercise"
    )

    assert response.status_code == 200
    assert len(response.json()) > 0

def test_filter_exercise_valid_endpoint():
    response = client.get(
        "/exercise/category/Leg"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    valid = True
    for exercise in data:
        if exercise["category"] != "Leg":
            valid = False

    assert valid

def test_filter_exercise_invalid_endpoint():
    response = client.get(
        "/exercise/category/random"
    )

    assert response.status_code == 422
    
    data = response.json()
    
    assert "detail" in data

    