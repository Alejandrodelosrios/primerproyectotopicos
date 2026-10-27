HEALTH_URL = "/api/v1/health"


# ---------- Caso bueno: todo funciona ----------

def test_health_when_model_is_loaded_returns_ok(client, model_available):
    response = client.get(HEALTH_URL)

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "model_loaded": True}


# ---------- Caso malo: el modelo no está disponible ----------

def test_health_when_model_is_not_loaded_returns_503_degraded(client, model_unavailable):
    response = client.get(HEALTH_URL)

    assert response.status_code == 503
    assert response.json() == {"status": "degraded", "model_loaded": False}


def test_health_when_model_is_not_loaded_never_reports_ok(client, model_unavailable):
    response = client.get(HEALTH_URL)

    assert response.json()["status"] != "ok"


# ---------- Casos intermedios: bordes y contrato ----------

def test_health_response_has_exactly_the_contract_fields(client, model_available):
    response = client.get(HEALTH_URL)

    assert set(response.json().keys()) == {"status", "model_loaded"}


def test_health_response_is_json(client, model_available):
    response = client.get(HEALTH_URL)

    assert response.headers["content-type"] == "application/json"


def test_health_rejects_post_method(client, model_available):
    response = client.post(HEALTH_URL)

    assert response.status_code == 405


def test_old_health_route_does_not_exist(client):
    response = client.get("/api/health")

    assert response.status_code == 404


def test_health_endpoint_is_documented_in_openapi(client):
    response = client.get("/openapi.json")

    assert HEALTH_URL in response.json()["paths"]