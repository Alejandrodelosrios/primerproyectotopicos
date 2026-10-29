import re
import unicodedata
from functools import lru_cache
from typing import Iterable

# Dependencias externas: no se cargan modelos lingüísticos al importar el módulo.
from nltk.stem.snowball import SnowballStemmer
from spacy.lang.es.stop_words import STOP_WORDS as SPACY_STOP_WORDS

_URL_RE = re.compile(r"(?i)\b(?:https?://|www\.)[^\s<>]+")
_TOKEN_RE = re.compile(r"[^\W_]+(?:[’'][^\W_]+)*|[^\w\s]", re.UNICODE)
_WHITESPACE_RE = re.compile(r"\s+")
_WORD_RE = re.compile(r"[^\W_]+(?:[’'][^\W_]+)*\Z", re.UNICODE)

# Las negaciones cambian el sentimiento. No eliminarlas como stop words.
NEGATIONS = frozenset({"no", "nunca", "jamás", "jamas", "sin", "ni", "tampoco"})
SPANISH_STOPWORDS = frozenset(SPACY_STOP_WORDS) - NEGATIONS
_STEMMER = SnowballStemmer("spanish")


def normalize_text(text: str) -> str:
    """Normaliza con Unicode NFC, minúsculas, URLs y espacios.

    Mantiene tildes, números, emojis, puntuación y palabras de negación.
    """
    if not isinstance(text, str):
        raise TypeError("El texto debe ser una cadena (str).")
    normalized = unicodedata.normalize("NFC", text)
    normalized = _URL_RE.sub(" url ", normalized)
    normalized = normalized.lower()
    return _WHITESPACE_RE.sub(" ", normalized).strip()


def tokenize_text(text: str) -> list[str]:
    """Separa tokens y conserva puntuación, emojis y números."""
    return _TOKEN_RE.findall(normalize_text(text))


def _validate_tokens(tokens: Iterable[str]) -> list[str]:
    if isinstance(tokens, (str, bytes)):
        raise TypeError("Se espera una secuencia de tokens, no un texto.")
    try:
        result = list(tokens)
    except TypeError as exc:
        raise TypeError("Se espera una secuencia de tokens.") from exc
    if not all(isinstance(token, str) for token in result):
        raise TypeError("Todos los tokens deben ser cadenas (str).")
    return result


def remove_stopwords(tokens: Iterable[str]) -> list[str]:
    words = _validate_tokens(tokens)
    return [token for token in words if token.casefold() not in SPANISH_STOPWORDS]


def stem_tokens(tokens: Iterable[str]) -> list[str]:
    """Aplica SnowballStemmer a tokens léxicos; conserva signos y emojis."""
    words = _validate_tokens(tokens)
    return [_STEMMER.stem(token) if _WORD_RE.fullmatch(token) else token
            for token in words]


@lru_cache(maxsize=1)
def _spanish_model():
    import spacy

    try:
        return spacy.load("es_core_news_sm", disable=["ner", "parser"])
    except OSError as exc:
        raise RuntimeError(
            "No está instalado el modelo spaCy es_core_news_sm. "
            "Ejecuta: python -m spacy download es_core_news_sm"
        ) from exc


def lemmatize_tokens(tokens: Iterable[str]) -> list[str]:
    words = _validate_tokens(tokens)
    if not words:
        return []
    doc = _spanish_model()(" ".join(words))
    return [token.lemma_.lower() if token.lemma_ else token.text.lower()
            for token in doc if not token.is_space]

