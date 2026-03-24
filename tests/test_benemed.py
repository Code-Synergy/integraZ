import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_checkout_plano_essencial():
    """Testa redirect para plano essencial"""
    response = client.get(
        "/benemed/checkout",
        params={"plan_id": "26d876219db04110881153441ad585d8"},
        follow_redirects=False
    )
    assert response.status_code == 302
    assert "hml.benemedsaude.com.br/checkout" in response.headers["location"]
    assert "id_plan=26d876219db04110881153441ad585d8" in response.headers["location"]
    assert "type=Individual" in response.headers["location"]
    assert "id_parceiro=157" in response.headers["location"]


def test_checkout_plano_essencial_saude_mental():
    """Testa redirect para plano essencial com saúde mental"""
    response = client.get(
        "/benemed/checkout",
        params={"plan_id": "720d68006f5f489eb8458d788710b451"},
        follow_redirects=False
    )
    assert response.status_code == 302
    assert "hml.benemedsaude.com.br/checkout" in response.headers["location"]
    assert "id_plan=720d68006f5f489eb8458d788710b451" in response.headers["location"]
    assert "type=Individual" in response.headers["location"]
    assert "id_parceiro=157" in response.headers["location"]


def test_checkout_plano_invalido():
    """Testa erro com plano inválido"""
    response = client.get(
        "/benemed/checkout",
        params={"plan_id": "plano_invalido_123"}
    )
    assert response.status_code == 400
    assert "Plano inválido" in response.json()["detail"]
