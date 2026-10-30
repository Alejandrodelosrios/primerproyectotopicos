#Pruebas del primer commit: normalización y tokenización.

import pytest

from src.nlp.preprocessing import normalize_text, tokenize_text


def test_normalization_preserves_accents_and_negations():
    assert normalize_text("  NO me GUSTÓ la BATERÍA  ") == "no me gustó la batería"


def test_normalization_handles_whitespace_and_unicode():
    assert normalize_text("Cafe\u0301\n\t  EXCELENTE") == "café excelente"


def test_normalization_replaces_urls():
    assert normalize_text("Ver HTTPS://ejemplo.com/a?q=1 ahora") == "ver url ahora"


def test_normalization_preserves_numbers_emoji_punctuation():
    assert normalize_text("¡Dura 2 horas! 😡") == "¡dura 2 horas! 😡"


def test_empty_input():
    assert normalize_text("   ") == ""
    assert tokenize_text("   ") == []


def test_non_string_input():
    with pytest.raises(TypeError, match="cadena"):
        normalize_text(None)
    with pytest.raises(TypeError, match="cadena"):
        tokenize_text(42)


def test_tokenization_with_negation_and_punctuation():
    assert tokenize_text("NO funciona bien!!!") == ["no", "funciona", "bien", "!", "!", "!"]


def test_tokenization_with_accent_numbers_emoji():
    assert tokenize_text("Batería 2h 😡") == ["batería", "2h", "😡"]


def test_tokenization_preserves_apostrophes():
    assert tokenize_text("L'ORÉAL llegó") == ["l'oréal", "llegó"]
