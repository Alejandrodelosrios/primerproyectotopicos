import pytest

PREDICT_URL = "/api/v1/predict"
POSITIVE = "Excelente producto, llegó rápido y funciona perfectamente."
NEGATIVE = "Pésima compra, llegó roto y no funciona."


# ---------- Caso bueno ----------

def test_predict_valid_review_returns_stars_and_probabilities(client, model_available):
    response = client.post(PREDICT_URL, json={"text": POSITIVE})

    assert response.status_code == 200
    prediction = response.json()["prediction"]
    assert prediction["stars"] in (1, 2, 3, 4, 5)
    assert set(prediction["probabilities"]) == {"1", "2", "3", "4", "5"}


def test_predict_probabilities_sum_to_one(client, model_available):
    probs = client.post(PREDICT_URL, json={"text": POSITIVE}).json()["prediction"]["probabilities"]

    assert sum(probs.values()) == pytest.approx(1.0, abs=0.01)


def test_predict_confidence_is_the_probability_of_the_predicted_stars(client, model_available):
    prediction = client.post(PREDICT_URL, json={"text": POSITIVE}).json()["prediction"]

    assert prediction["confidence"] == prediction["probabilities"][str(prediction["stars"])]
    assert prediction["confidence"] == max(prediction["probabilities"].values())


def test_predict_positive_review_scores_higher_than_negative(client, model_available):
    positive = client.post(PREDICT_URL, json={"text": POSITIVE}).json()["prediction"]["stars"]
    negative = client.post(PREDICT_URL, json={"text": NEGATIVE}).json()["prediction"]["stars"]

    assert positive > negative


def test_predict_reports_the_model_used(client, model_available):
    from app.services.model_service import get_nlp_method

    model = client.post(PREDICT_URL, json={"text": POSITIVE}).json()["model"]

    assert model["name"] == "logistic_regression"
    assert model["method"] == get_nlp_method()


# ---------- Caso malo: modelo no disponible ----------

def test_predict_when_model_is_not_loaded_returns_503(client, model_unavailable):
    response = client.post(PREDICT_URL, json={"text": POSITIVE})

    assert response.status_code == 503
    assert "modelo" in response.json()["detail"]


# ---------- Casos intermedios: validacion de entrada ----------

@pytest.mark.parametrize("payload", [
    {},                      # sin campo text
    {"text": ""},            # vacio
    {"text": "   "},         # solo espacios
    {"text": "ab"},          # menos de 3 caracteres
    {"text": "a" * 5001},    # mas de 5000 caracteres
    {"text": 123},           # tipo incorrecto
])
def test_predict_rejects_invalid_input(client, model_available, payload):
    response = client.post(PREDICT_URL, json=payload)

    assert response.status_code == 422


def test_predict_accepts_text_at_the_length_limits(client, model_available):
    assert client.post(PREDICT_URL, json={"text": "abc"}).status_code == 200
    assert client.post(PREDICT_URL, json={"text": "a" * 5000}).status_code == 200


def test_predict_rejects_get_method(client, model_available):
    assert client.get(PREDICT_URL).status_code == 405


def test_predict_endpoint_is_documented_in_openapi(client):
    assert PREDICT_URL in client.get("/openapi.json").json()["paths"]