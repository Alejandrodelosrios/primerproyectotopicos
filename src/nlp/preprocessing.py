#Normalización y tokenización inicial para reseñas de productos en español.

import re
import unicodedata

# URLs HTTP(S) y dominios que comienzan por www.
_URL_RE = re.compile(r"(?i)\b(?:https?://|www\.)[^\s<>]+")
_TOKEN_RE = re.compile(r"[^\W_]+(?:[’'][^\W_]+)*|[^\w\s]", re.UNICODE)
_WHITESPACE_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    #Normaliza una reseña sin eliminar información de sentimiento.
    if not isinstance(text, str):
        raise TypeError("El texto debe ser una cadena (str).")
    normalized = unicodedata.normalize("NFC", text)
    normalized = _URL_RE.sub(" url ", normalized)
    normalized = normalized.lower()
    return _WHITESPACE_RE.sub(" ", normalized).strip()


def tokenize_text(text: str) -> list[str]:
    #Devuelve tokens de una reseña normalizada.
    normalized = normalize_text(text)
    return _TOKEN_RE.findall(normalized)
