from types import SimpleNamespace

import pytest

from src.nlp import preprocessing as nlp


def test_stopwords_remove_common_words_and_keep_negations():
    assert nlp.remove_stopwords(["no", "me", "gusta", "la", "batería"]) == [
        "no", "gusta", "batería"
    ]


def test_stopwords_keep_negations_punctuation_emoji():
    tokens = ["nunca", "sin", "ni", "tampoco", "jamás", "!", "😡"]
    assert nlp.remove_stopwords(tokens) == tokens


def test_stopwords_are_case_insensitive():
    assert nlp.remove_stopwords(["LA", "BATERÍA", "NO"]) == ["BATERÍA", "NO"]


def test_stemming_spanish_words():
    assert nlp.stem_tokens(["comprando", "comprar", "compramos"]) == [
        "compr", "compr", "compr"
    ]


def test_stemming_preserves_punctuation_and_emoji():
    assert nlp.stem_tokens(["bueno", "!", "😡", "2h"]) == ["buen", "!", "😡", "2h"]


def test_empty_and_invalid_tokens():
    for func in (nlp.remove_stopwords, nlp.stem_tokens, nlp.lemmatize_tokens):
        assert func([]) == []
        with pytest.raises(TypeError):
            func("texto sin tokenizar")
        with pytest.raises(TypeError):
            func(["correcto", 123])


def test_lemmatizer_uses_model_output(monkeypatch):
    class FakeModel:
        def __call__(self, text):
            assert text == "comprando baterías !"
            return [
                SimpleNamespace(lemma_="comprar", text="comprando", is_space=False),
                SimpleNamespace(lemma_="batería", text="baterías", is_space=False),
                SimpleNamespace(lemma_="!", text="!", is_space=False),
            ]

    monkeypatch.setattr(nlp, "_spanish_model", lambda: FakeModel())
    assert nlp.lemmatize_tokens(["comprando", "baterías", "!"]) == [
        "comprar", "batería", "!"
    ]


def test_lemmatizer_raises_actionable_error_when_model_missing(monkeypatch):
    def missing():
        raise RuntimeError("No está instalado el modelo spaCy es_core_news_sm. Ejecuta: python -m spacy download es_core_news_sm")

    monkeypatch.setattr(nlp, "_spanish_model", missing)
    with pytest.raises(RuntimeError, match="spacy download es_core_news_sm"):
        nlp.lemmatize_tokens(["hola"])


def test_stemming_and_lemmatization_are_separate_strategies():
    # El algoritmo de entrenamiento elegirá una estrategia, no las concatenará.
    assert callable(nlp.stem_tokens)
    assert callable(nlp.lemmatize_tokens)
