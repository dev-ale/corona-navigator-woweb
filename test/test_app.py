from pytest_helper import client

def test_api_incidences(client):
    response = client.get("/api/incidences")
    assert response.json == []
