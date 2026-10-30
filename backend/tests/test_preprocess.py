import pytest

from src.nlp.preprocessing import normalize_text, tokenize_text

PREPROCESS_URL = "/api/v1/preprocess"


# ---------- Caso bueno: reseña normal ----------

def test_preprocess_valid_review_returns_normalized_text_and_tokens(client):
    response = client.post(PREPROCESS_URL, json={"text": "NO me GUSTÓ la batería"})

    assert response.status_code == 200
    body = response.json()
    assert body["original_text"] == "NO me GUSTÓ la batería"
    assert body["normalized_text"] == "no me gustó la batería"
    assert body["tokens"] == ["no", "me", "gustó", "la", "batería"]


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

    assert set(response.json().keys()) == {
        "original_text", "normalized_text", "tokens",
        "filtered_tokens", "morphological_method",
        "morphological_tokens", "processed_text",
    }


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

# ---------- Etapas nuevas: stop words, raices y texto procesado ----------

def test_preprocess_removes_stopwords_but_keeps_negations(client):
    body = client.post(
        PREPROCESS_URL,
        json={"text": "NO me gustó la batería, pero la pantalla es excelente!"},
    ).json()

    assert body["filtered_tokens"] == [
        "no", "gustó", "batería", ",", "pantalla", "excelente", "!"
    ]


def test_preprocess_applies_stemming_to_filtered_tokens(client):
    body = client.post(
        PREPROCESS_URL,
        json={"text": "NO me gustó la batería, pero la pantalla es excelente!"},
    ).json()

    assert body["morphological_method"] == "stemming"
    assert body["morphological_tokens"] == [
        "no", "gust", "bat", ",", "pantall", "excelent", "!"
    ]


def test_preprocess_processed_text_is_what_the_model_receives(client):
    """processed_text debe ser identico a lo que produce el transformer
    que va dentro del modelo (misma logica, sin duplicarla)."""
    from src.nlp.transformer import SpanishReviewTransformer

    text = "NO me gustó la batería, pero la pantalla es excelente!"
    body = client.post(PREPROCESS_URL, json={"text": text}).json()

    expected = SpanishReviewTransformer(method="stemming").transform([text])[0]
    assert body["processed_text"] == expected


def test_preprocess_uses_the_method_of_the_loaded_model(client, monkeypatch):
    monkeypatch.setattr(
        "app.routers.preprocess.get_nlp_method", lambda: "none"
    )
    body = client.post(PREPROCESS_URL, json={"text": "no me gustó"}).json()

    assert body["morphological_method"] == "none"
    assert body["morphological_tokens"] == body["filtered_tokens"]


def test_preprocess_without_model_falls_back_to_stemming(client, monkeypatch):
    monkeypatch.setattr("app.services.model_service._model", None)
    response = client.post(PREPROCESS_URL, json={"text": "buen producto"})

    assert response.status_code == 200
    assert response.json()["morphological_method"] == "stemming"


def test_preprocess_lemmatization_without_spacy_model_returns_503(client, monkeypatch):
    def missing_spacy_model(tokens):
        raise RuntimeError("No está instalado el modelo spaCy es_core_news_sm")

    monkeypatch.setattr("app.routers.preprocess.get_nlp_method", lambda: "lemmatization")
    monkeypatch.setattr("app.services.nlp_service.lemmatize_tokens", missing_spacy_model)

    response = client.post(PREPROCESS_URL, json={"text": "buen producto"})

    assert response.status_code == 503
    assert "es_core_news_sm" in response.json()["detail"]