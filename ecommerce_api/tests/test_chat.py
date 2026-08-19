from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat_rejects_empty_message():
    response = client.post("/api/chat", json={"message": "   "})

    assert response.status_code == 400, response.text


def test_chat_reports_missing_gemini_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    response = client.post("/api/chat", json={"message": "Qual é o prazo de entrega?"})

    assert response.status_code == 503, response.text
    assert "GEMINI_API_KEY" in response.json()["detail"]


def test_chat_retries_and_uses_fallback_model(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    calls = []

    class FakeModels:
        def generate_content(self, *, model, contents, config):
            calls.append(model)
            if model == "gemini-3.6-flash":
                raise RuntimeError("503 UNAVAILABLE: high demand")
            return type("Result", (), {"text": "Resposta do modelo reserva"})()

    class FakeClient:
        models = FakeModels()

    monkeypatch.setattr("app.main.genai.Client", lambda api_key: FakeClient())
    response = client.post("/api/chat", json={"message": "Qual o prazo?"})

    assert response.status_code == 200, response.text
    assert response.json()["response"] == "Resposta do modelo reserva"
    assert calls == ["gemini-3.6-flash", "gemini-3.6-flash", "gemini-3.5-flash"]


def test_chat_returns_friendly_503_when_all_models_are_unavailable(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    class FakeModels:
        def generate_content(self, **kwargs):
            raise RuntimeError("503 UNAVAILABLE: high demand")

    class FakeClient:
        models = FakeModels()

    monkeypatch.setattr("app.main.genai.Client", lambda api_key: FakeClient())
    response = client.post("/api/chat", json={"message": "Olá"})

    assert response.status_code == 503, response.text
    assert "temporariamente sobrecarregado" in response.json()["detail"]
