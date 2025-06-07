from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_add_trade():
    response = client.post("/trades", json={"ticker": "AAPL", "price": 150.0, "quantity": 10, "side": "buy"})
    assert response.status_code == 200
    assert response.json()["ticker"] == "AAPL"

def test_get_trades():
    response = client.get("/trades?ticker=AAPL")
    assert response.status_code == 200
    assert isinstance(response.json(), list)