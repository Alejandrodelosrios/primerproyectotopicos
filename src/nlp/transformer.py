from sklearn.base import BaseEstimator, TransformerMixin
from src.nlp.preprocessing import (
    normalize_text, tokenize_text, remove_stopwords, stem_tokens,
    lemmatize_tokens,
)


class SpanishReviewTransformer(TransformerMixin, BaseEstimator):
    """Normaliza y transforma reseñas; stemming y lematización son excluyentes.

    method: 'stemming', 'lemmatization' o 'none'.
    La configuración se almacena dentro del Pipeline serializado.
    """

    def __init__(self, method: str = "stemming", remove_stop_words: bool = True):
        self.method = method
        self.remove_stop_words = remove_stop_words

    def fit(self, X, y=None):
        if self.method not in ("stemming", "lemmatization", "none"):
            raise ValueError("method debe ser stemming, lemmatization o none")
        return self

    def transform(self, X):
        if isinstance(X, (str, bytes)):
            raise TypeError("X debe ser una secuencia de reseñas, no un string")
        result = []
        for text in X:
            if not isinstance(text, str):
                raise TypeError("Cada reseña debe ser un texto (str)")
            normalized = normalize_text(text)
            tokens = tokenize_text(normalized)
            if self.remove_stop_words:
                tokens = remove_stopwords(tokens)
            if self.method == "stemming":
                tokens = stem_tokens(tokens)
            elif self.method == "lemmatization":
                tokens = lemmatize_tokens(tokens)
            result.append(" ".join(tokens))
        return result
