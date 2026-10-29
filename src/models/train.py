import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, mean_absolute_error
from sklearn.model_selection import train_test_split

from .pipeline import create_pipeline

LABELS = [1, 2, 3, 4, 5]


def load_reviews(path):
    """Carga CSV con columnas review_text (texto) y rating (entero 1..5)."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"No existe el archivo: {path}")
    df = pd.read_csv(path, dtype={"review_text": "string"})
    required = {"review_text", "rating"}
    if not required.issubset(df.columns):
        raise ValueError(f"{path}: faltan columnas {sorted(required - set(df.columns))}")
    df = df.copy()
    if df["review_text"].isna().any() or df["rating"].isna().any():
        raise ValueError(f"{path}: existen textos o puntuaciones nulos")
    df["review_text"] = df["review_text"].str.strip()
    if df["review_text"].eq("").any():
        raise ValueError(f"{path}: existen reseñas vacías")
    # Evita convertir silenciosamente 4.5 en 4 o aceptar etiquetas 0..4.
    rating = pd.to_numeric(df["rating"], errors="coerce")
    if rating.isna().any() or not rating.isin(LABELS).all():
        raise ValueError(f"{path}: rating debe ser un entero de 1 a 5 (sin decimales)")
    df["rating"] = rating.astype("int64")
    return df


def _text_keys(df):
    # Se aplica la normalización establecida por el primer commit para
    # detectar textos idénticos tras normalización y reducir fuga de datos.
    from src.nlp.preprocessing import normalize_text
    return df["review_text"].map(normalize_text)


def validate_splits(train_df, test_df):
    """Evita fugas entre train y test y verifica clases suficientes."""
    train_keys = _text_keys(train_df)
    test_keys = _text_keys(test_df)
    if train_keys.duplicated().any() or test_keys.duplicated().any():
        raise ValueError("Hay textos duplicados dentro de train o test; depura en la rama data")
    overlap = set(train_keys) & set(test_keys)
    if overlap:
        raise ValueError(f"Fuga de datos: {len(overlap)} reseñas presentes tanto en train como en test")
    if set(train_df["rating"]) != set(LABELS):
        raise ValueError("train debe contener las cinco clases de rating: 1,2,3,4,5")
    if set(test_df["rating"]) != set(LABELS):
        raise ValueError("test debe contener las cinco clases de rating: 1,2,3,4,5")


def _save_and_evaluate(train_df, test_df, output_dir, method, seed, source):
    validate_splits(train_df, test_df)
    model = create_pipeline(method=method, random_state=seed)
    model.fit(train_df["review_text"].tolist(), train_df["rating"].tolist())
    pred = model.predict(test_df["review_text"].tolist())
    metrics = {
        "accuracy": float(accuracy_score(test_df["rating"], pred)),
        "macro_f1": float(f1_score(test_df["rating"], pred, labels=LABELS, average="macro", zero_division=0)),
        "mae": float(mean_absolute_error(test_df["rating"], pred)),
        "labels": LABELS,
        "confusion_matrix": confusion_matrix(test_df["rating"], pred, labels=LABELS).tolist(),
        "train_size": int(len(train_df)),
        "test_size": int(len(test_df)),
        "method": method,
        "random_state": seed,
        "source": source,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out / "pipeline.joblib")
    (out / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    return metrics


def train(csv_path, output_dir="models", method="stemming", test_size=0.2, seed=42):
    """Modo compatible con el tercer commit: divide un CSV sin splits previos."""
    df = load_reviews(csv_path)
    keys = _text_keys(df)
    if keys.duplicated().any():
        raise ValueError("CSV con textos duplicados: elimina duplicados antes del split")
    if set(df["rating"]) != set(LABELS) or df["rating"].value_counts().min() < 2:
        raise ValueError("El CSV necesita al menos 2 reseñas únicas de cada clase")
    if int(round(len(df) * test_size)) < 5 or len(df) - int(round(len(df) * test_size)) < 5:
        raise ValueError("Dataset demasiado pequeño para una división estratificada de 5 clases")
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=seed, stratify=df["rating"])
    return _save_and_evaluate(train_df, test_df, output_dir, method, seed, "internal_split")


def train_from_splits(train_path, test_path, output_dir="models", method="stemming", seed=42):
    """Modo recomendado: usa los CSV creados en la rama data, sin dividir de nuevo."""
    train_df = load_reviews(train_path)
    test_df = load_reviews(test_path)
    return _save_and_evaluate(train_df, test_df, output_dir, method, seed, "external_splits")


def main():
    parser = argparse.ArgumentParser(description="Entrena TF-IDF + LogisticRegression")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--train", help="CSV de entrenamiento (requiere --test)")
    group.add_argument("--csv", help="CSV original para división interna (modo anterior)")
    parser.add_argument("--test", help="CSV de prueba generado por la rama data")
    parser.add_argument("--output-dir", default="models")
    parser.add_argument("--method", choices=["stemming", "lemmatization", "none"], default="stemming")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.train and not args.test:
        parser.error("--train requiere --test")
    if args.csv and args.test:
        parser.error("--test se utiliza únicamente junto con --train")
    result = (train_from_splits(args.train, args.test, args.output_dir, args.method, args.seed)
              if args.train else train(args.csv, args.output_dir, args.method, seed=args.seed))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
