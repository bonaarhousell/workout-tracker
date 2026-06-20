from fastapi.testclient import TestClient
from app.main import app
from app.database.setup_db import get_db
from tests.test_db import override_get_db
from uuid import uuid4

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def get_token():
    unique = str(uuid4())[:8]

    client.post(
        "/register",
        json= {
            "username": f"test_{unique}",
            "email": f"test{unique}@gmail.com",
            "password": "123456j",
        }
    )

    response = client.post(
        "/login",
        data= {
            "username": f"test_{unique}",
            "password": "123456j"
        }
    )

    return  response.json()["access_token"]
 
def get_token_admin():
    #note: I already regis with username adminbonar, and on postgres i change the role to admin
    response = client.post(
        "/login",
        data= {
            "username": "adminbonar",
            "password": "bonar9999"
        }
    )

    return  response.json()["access_token"]

def create_workout_test():
    token = get_token()
    headers = {
        "Authorization" : f"bearer {token}"
    }
    response = client.post(
        "/workout",
        json={
            "title": "Grow arms",
            "schedule_at": "2026-06-23T08:30:00",
            "comment": "with trainer david"
        },
        headers=headers
    )
    data = response.json()

    return {
        "id_workout": data["id_workout"],
        "token": token,
    }