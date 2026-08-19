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


def test_current_user_profile_and_update_are_protected():
    anonymous_response = client.get("/users/me")
    assert anonymous_response.status_code == 401, anonymous_response.text

    unique_email = f"profile+{uuid.uuid4().hex[:8]}@example.com"
    credentials = {"name": "Perfil", "email": unique_email, "password": "senha123"}
    register_response = client.post("/register", json=credentials)
    assert register_response.status_code == 201, register_response.text

    token = register_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    profile_response = client.get("/users/me", headers=headers)
    assert profile_response.status_code == 200, profile_response.text
    assert profile_response.json()["name"] == "Perfil"
    assert profile_response.json()["email"] == unique_email
    assert profile_response.json()["orders"] == []
    assert "hashed_password" not in profile_response.json()

    update_response = client.put(
        "/users/me",
        json={"name": "Perfil Atualizado", "password": "novasenha"},
        headers=headers,
    )
    assert update_response.status_code == 200, update_response.text
    assert update_response.json()["name"] == "Perfil Atualizado"

    login_response = client.post(
        "/login",
        json={"email": unique_email, "password": "novasenha"},
    )
    assert login_response.status_code == 200, login_response.text
