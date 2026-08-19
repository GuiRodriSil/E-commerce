from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_support_ticket_returns_protocol():
    response = client.post(
        "/support/tickets",
        json={
            "name": "Cliente Teste",
            "email": "cliente@example.com",
            "subject": "Dúvida sobre entrega",
            "message": "Gostaria de acompanhar meu pedido.",
        },
    )

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["message"] == "Solicitação recebida com sucesso"
    assert data["protocol"].startswith("SUP-")
    assert len(data["protocol"]) == 14
    assert data["created_at"]


def test_create_support_ticket_validates_required_content():
    response = client.post(
        "/support/tickets",
        json={
            "name": "   ",
            "email": "cliente@example.com",
            "subject": "Entrega",
            "message": "Mensagem válida",
        },
    )

    assert response.status_code == 400, response.text


def test_payment_requires_authentication():
    response = client.post(
        "/payments/mercadopago",
        json={
            "payer_email": "cliente@example.com",
            "payment_method": "card",
            "items": [{"id": 1, "title": "Produto", "quantity": 1, "unit_price": 10}],
        },
    )

    assert response.status_code == 401, response.text