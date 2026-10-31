import json
import pandas as pd
import pytest
from src.models.train import load_reviews, train_from_splits


BASE = {
    1: ["terrible articulo roto", "horrible compra defectuosa", "producto malo inútil", "muy mala experiencia"],
    2: ["baja calidad material", "producto lento y flojo", "decepción con acabado", "servicio malo tardío"],
    3: ["calidad promedio aceptable", "producto normal sencillo", "uso regular cotidiano", "resultado intermedio esperado"],
    4: ["buen producto conveniente", "bastante útil recomendado", "calidad buena práctica", "compra satisfactoria segura"],
    5: ["excelente producto perfecto", "increíble calidad superior", "maravillosa compra ideal", "fantástico rendimiento excelente"],
}


def write_splits(tmp_path):
    train = tmp_path / "train.csv"
    test = tmp_path / "test.csv"
    pd.DataFrame([{"review_text": t, "rating": r} for r, texts in BASE.items() for t in texts[:3]]).to_csv(train, index=False)
    pd.DataFrame([{"review_text": texts[3], "rating": r} for r, texts in BASE.items()]).to_csv(test, index=False)
    return train, test


def test_training_uses_external_splits(tmp_path):
    train, test = write_splits(tmp_path)
    metrics = train_from_splits(train, test, tmp_path / "out")
    assert metrics["train_size"] == 15
    assert metrics["test_size"] == 5
    assert metrics["source"] == "external_splits"
    assert (tmp_path / "out" / "pipeline.joblib").exists()
    assert json.loads((tmp_path / "out" / "metrics.json").read_text())["source"] == "external_splits"


def test_rejects_leakage(tmp_path):
    train, test = write_splits(tmp_path)
    df = pd.read_csv(test)
    df.loc[0, "review_text"] = "TERRIBLE ARTICULO ROTO"
    df.to_csv(test, index=False)
    with pytest.raises(ValueError, match="Fuga de datos"):
        train_from_splits(train, test, tmp_path / "out")


def test_rejects_fractional_rating(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame({"review_text": ["es bueno"], "rating": [3.5]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="entero"):
        load_reviews(path)


def test_rejects_missing_column(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame({"text": ["bueno"], "rating": [5]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="faltan columnas"):
        load_reviews(path)
