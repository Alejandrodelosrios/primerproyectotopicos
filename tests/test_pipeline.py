import json
import joblib
import pandas as pd
import pytest

from src.nlp.transformer import SpanishReviewTransformer
from src.models.pipeline import create_pipeline
from src.models.train import train


SAMPLES = {
    1: ["horrible producto roto", "pésimo servicio defectuoso", "muy malo nunca funcionó", "terrible compra inútil", "desastroso producto pésimo"],
    2: ["producto malo lento", "calidad baja falla", "no funciona bien", "decepcionante calidad pobre", "bastante malo decepción"],
    3: ["producto aceptable normal", "funciona regular suficiente", "calidad promedio normal", "ni bueno ni malo", "producto común aceptable"],
    4: ["buen producto recomendable", "funciona bien satisfecho", "calidad buena útil", "bastante bueno práctico", "compra buena conveniente"],
    5: ["excelente producto perfecto", "maravillosa calidad increíble", "fantástico funciona excelente", "magnífica compra perfecta", "extraordinaria calidad excelente"],
}


def test_transformer_uses_previous_nlp():
    result = SpanishReviewTransformer(method="none").fit_transform(["NO funciona la batería!!!"])[0]
    assert "no" in result.split()
    assert "la" not in result.split()


def test_invalid_method():
    with pytest.raises(ValueError):
        SpanishReviewTransformer(method="other").fit([])


def test_model_predicts_valid_stars():
    X = [s for group in SAMPLES.values() for s in group]
    y = [rating for rating, group in SAMPLES.items() for _ in group]
    pipeline = create_pipeline().fit(X, y)
    assert int(pipeline.predict(["excelente producto"])[0]) in {1, 2, 3, 4, 5}
    assert pipeline.predict_proba(["excelente producto"]).shape == (1, 5)


def test_end_to_end_training_and_loading(tmp_path):
    csv = tmp_path / "reviews.csv"
    pd.DataFrame([
        {"review_text": review, "rating": rating}
        for rating, group in SAMPLES.items() for review in group
    ]).to_csv(csv, index=False)
    out = tmp_path / "models"
    metrics = train(csv, out)
    assert (out / "pipeline.joblib").exists()
    assert metrics["train_size"] == 20
    assert metrics["test_size"] == 5
    saved = json.loads((out / "metrics.json").read_text(encoding="utf-8"))
    assert len(saved["confusion_matrix"]) == 5
    loaded = joblib.load(out / "pipeline.joblib")
    assert int(loaded.predict(["producto horrible"])[0]) in {1, 2, 3, 4, 5}


def test_invalid_dataset_rejected(tmp_path):
    csv = tmp_path / "invalid.csv"
    pd.DataFrame([{"review_text": "hola", "rating": 6}]).to_csv(csv, index=False)
    with pytest.raises(ValueError):
        train(csv, tmp_path / "models")
