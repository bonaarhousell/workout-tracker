from fastapi.testclient import TestClient
from app.main import app
from app.database.setup_db import get_db
from tests.test_db import override_get_db
from uuid import uuid4

app.dependency_overrides[get_db] = override_get_db 

client = TestClient(app)

def test_login_success():
    unique = str(uuid4())[:8]
    client.post(
        "/register",
        json={
            "username": f"test_{unique}",
            "email": f"test{unique}@gmail.com",
            "password": "123456",
        }
    )
    response = client.post(
        "/login",
        data={
            "username": f"test_{unique}",
            "password": "123456"
        }
    )

    print(response.json())
    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data

def test_register_success():
    unique = str(uuid4())[:8]
    response = client.post(
        "/register",
        json={
            "username": f"test_{unique}",
            "email": f"test{unique}@gmail.com",
            "password": "123456",
        }
    )
    print(response.json())
    assert response.status_code == 201

def test_login_wrong_password():
    unique = str(uuid4())[:8]
    client.post(
        "/register",
        json={
            "username": f"test_{unique}",
            "email": f"test{unique}@gmail.com",
            "password": "1278999",
        }
    )
    response = client.post(
        "/login",
        data={
            "username": f"test_{unique}",
            "password": "TETOTTTT"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert response.json()["detail"] == "Invalid Username or Password"

    assert "access_token" not in data
    assert "token_type" not in data