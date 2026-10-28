import pytest

from src.nlp.preprocessing import normalize_text, tokenize_text

PREPROCESS_URL = "/api/v1/preprocess"


# ---------- Caso bueno: reseña normal ----------

def test_preprocess_valid_review_returns_normalized_text_and_tokens(client):
    response = client.post(PREPROCESS_URL, json={"text": "NO me GUSTÓ la batería"})

    assert response.status_code == 200
    assert response.json() == {
        "original_text": "NO me GUSTÓ la batería",
        "normalized_text": "no me gustó la batería",
        "tokens": ["no", "me", "gustó", "la", "batería"],
    }


# ---------- Casos malos: entradas inválidas ----------

INVALID_PAYLOADS = [
    pytest.param({"text": ""}, id="texto_vacio"),
    pytest.param({"text": "   "}, id="solo_espacios"),
    pytest.param({"text": "ab"}, id="2_caracteres"),
    pytest.param({"text": "  ab  "}, id="2_caracteres_con_espacios"),
    pytest.param({"text": "a" * 5001}, id="5001_caracteres"),
    pytest.param({}, id="campo_ausente"),
    pytest.param({"text": None}, id="texto_null"),
    pytest.param({"text": 123}, id="numero_en_vez_de_texto"),
    pytest.param({"text": ["hola"]}, id="lista_en_vez_de_texto"),
    pytest.param({"texto": "hola mundo"}, id="campo_con_otro_nombre"),
]


@pytest.mark.parametrize("payload", INVALID_PAYLOADS)
def test_preprocess_rejects_invalid_payload(client, payload):
    response = client.post(PREPROCESS_URL, json=payload)

    assert response.status_code == 422


def test_preprocess_rejects_malformed_json(client):
    response = client.post(
        PREPROCESS_URL,
        content='{"text": sin comillas',
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422


def test_preprocess_rejects_request_without_body(client):
    response = client.post(PREPROCESS_URL)

    assert response.status_code == 422


def test_preprocess_validation_error_points_to_text_field(client):
    response = client.post(PREPROCESS_URL, json={"text": ""})

    errors = response.json()["detail"]
    assert any("text" in error["loc"] for error in errors)


# ---------- Casos intermedios: bordes y contrato ----------

@pytest.mark.parametrize(
    "text",
    [
        pytest.param("abc", id="3_caracteres_minimo"),
        pytest.param("a" * 5000, id="5000_caracteres_maximo"),
    ],
)
def test_preprocess_accepts_text_at_the_length_limits(client, text):
    response = client.post(PREPROCESS_URL, json={"text": text})

    assert response.status_code == 200


def test_preprocess_trims_surrounding_whitespace(client):
    response = client.post(PREPROCESS_URL, json={"text": "  hola mundo  "})

    assert response.status_code == 200
    assert response.json()["original_text"] == "hola mundo"


def test_preprocess_replaces_urls(client):
    response = client.post(PREPROCESS_URL, json={"text": "Ver HTTPS://ejemplo.com/a?q=1 ahora"})

    body = response.json()
    assert body["normalized_text"] == "ver url ahora"
    assert body["tokens"] == ["ver", "url", "ahora"]


def test_preprocess_splits_punctuation_and_emoji(client):
    response = client.post(PREPROCESS_URL, json={"text": "NO funciona bien!!! 😡"})

    assert response.json()["tokens"] == ["no", "funciona", "bien", "!", "!", "!", "😡"]


def test_preprocess_response_has_exactly_the_contract_fields(client):
    response = client.post(PREPROCESS_URL, json={"text": "buen producto"})

    assert set(response.json().keys()) == {"original_text", "normalized_text", "tokens"}


def test_preprocess_rejects_get_method(client):
    response = client.get(PREPROCESS_URL)

    assert response.status_code == 405


def test_preprocess_works_when_model_is_not_loaded(client, model_unavailable):
    response = client.post(PREPROCESS_URL, json={"text": "buen producto"})

    assert response.status_code == 200


def test_preprocess_matches_nlp_functions(client):
    text = "Llegó TARDE y NO me gustó 😡 https://ejemplo.com"

    body = client.post(PREPROCESS_URL, json={"text": text}).json()

    assert body["normalized_text"] == normalize_text(text)
    assert body["tokens"] == tokenize_text(text)


def test_preprocess_is_documented_in_openapi(client):
    response = client.get("/openapi.json")

    assert PREPROCESS_URL in response.json()["paths"]