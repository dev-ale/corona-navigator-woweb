from pytest_helper import client
import json
from jsonschema import validate

schema_incidence = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "canton": {"type": "string"},
            "date": {"type": "string"},
            "incident": {"type": "number"},
            "name": {"type": "string"}
        }
    }
}


def test_if_api_is_reachable(client):
    response = client.get("/api/incidences")
    assert response.status_code == 200


def test_wrong_uri_should_return_404(client):
    response = client.get("/api/incidenct")
    assert response.status_code == 404


def test_get_incidences_from_db(client):
    response = client.get("/api/incidences")
    body = response.json
    assert len(body) == 2


def test_get_incidences_and_check_schema(client):
    response = client.get("/api/incidences")
    body = response.json
    validate(instance=body, schema=schema_incidence)
    assert response.headers['Content-Type'] == "application/json"
    assert len(body) == 2
