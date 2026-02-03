import pytest
import httpx

from app.main import app
from app.settings import settings


@pytest.mark.asyncio
async def test_customize_configuration_pass_through(monkeypatch, respx_mock):
    # Arrange: patch nas configs corretas do Settings (pydantic)
    monkeypatch.setattr(settings, "univers_base_url", "https://upstream.test/univers/v1")
    monkeypatch.setattr(settings, "univers_token_url", "https://auth.test/oauth/token")
    monkeypatch.setattr(settings, "univers_client_id", "client-id")
    monkeypatch.setattr(settings, "univers_client_secret", "client-secret")

    fake_token = {"access_token": "tok-abc", "expires_in": 3600}
    token_route = respx_mock.post("https://auth.test/oauth/token").respond(200, json=fake_token)

    upstream_payload = {"foo": "bar", "store": "DROGASIL"}
    upstream_url = "https://upstream.test/univers/v1/store/DROGASIL/customize/configuration"
    upstream_route = respx_mock.get(upstream_url).respond(200, json=upstream_payload)

    # Act: chama o nosso endpoint local (ASGI), que por dentro chama OAuth + Upstream
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get(
            "/store/DROGASIL/customize/configuration",
            headers={"X-Correlation-Id": "test-123"},
        )

    # Assert: resposta repassada
    assert resp.status_code == 200
    assert resp.json() == upstream_payload

    # Assert: token foi buscado
    assert token_route.called is True
    token_req = token_route.calls[0].request
    assert token_req.headers.get("X-Correlation-Id") == "test-123"

    # Assert: upstream foi chamado com Bearer + correlation id
    assert upstream_route.called is True
    up_req = upstream_route.calls[0].request
    assert up_req.headers.get("X-Correlation-Id") == "test-123"
    assert up_req.headers.get("Authorization") == "Bearer tok-abc"
