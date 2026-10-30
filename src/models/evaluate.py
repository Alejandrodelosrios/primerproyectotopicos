from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from src.nlp.transformer import SpanishReviewTransformer


def create_pipeline(*, method="stemming", ngram_range=(1, 2),
                    max_features=20000, min_df=1, max_df=1.0,
                    C=1.0, random_state=42):
    """Devuelve un pipeline sin entrenar.

    min_df=1 y max_df=1.0 permiten ejecutar también datasets pequeños de prueba.
    Para el dataset real pueden compararse min_df=3 y max_df=0.95.
    """
    return Pipeline([
        ("nlp", SpanishReviewTransformer(method=method)),
        ("tfidf", TfidfVectorizer(
            ngram_range=ngram_range,
            max_features=max_features,
            min_df=min_df,
            max_df=max_df,
            lowercase=False,
            token_pattern=r"(?u)\b\w+\b",  # Mantiene la negación 'no'
            sublinear_tf=True,
        )),
        ("classifier", LogisticRegression(
            C=C, max_iter=1000, random_state=random_state,
        )),
    ])
