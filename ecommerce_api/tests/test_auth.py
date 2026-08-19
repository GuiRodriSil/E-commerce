import uuid

import jwt
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_login_and_checkout_protected():
    unique_email = f"alice+{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "name": "Alice",
        "email": unique_email,
        "password": "senha123",
    }

    register_response = client.post("/register", json=payload)
    assert register_response.status_code == 201, register_response.text

    login_response = client.post(
        "/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert login_response.status_code == 200, login_response.text
    access_token = login_response.json()["access_token"]
    assert access_token
    user_id = int(jwt.decode(access_token, options={"verify_signature": False})["sub"])

    protected_response = client.post(
        "/orders",
        json={"user_id": user_id, "items": [{"product_id": 1, "quantity": 1}]},
    )
    assert protected_response.status_code == 401, protected_response.text

    auth_response = client.post(
        "/orders",
        json={"user_id": user_id, "items": [{"product_id": 1, "quantity": 1}]},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert auth_response.status_code in {201, 404}, auth_response.text
