
import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, mean_absolute_error
from sklearn.model_selection import GridSearchCV, StratifiedKFold

from .pipeline import create_pipeline
from .train import LABELS, load_reviews, validate_splits


def score(y_true, y_pred):
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0)),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=LABELS).tolist(),
    }


def run_experiments(train_path, test_path, output_dir="models/final", seed=42, folds=3,
                    methods=("stemming", "lemmatization"), c_values=(0.1, 1.0, 10.0)):
    if folds < 2:
        raise ValueError("folds debe ser al menos 2")
    if not c_values or any(c <= 0 for c in c_values):
        raise ValueError("Los valores de C deben ser positivos")
    if not methods or any(m not in ("stemming", "lemmatization", "none") for m in methods):
        raise ValueError("Método NLP no válido")
    train = load_reviews(train_path)
    test = load_reviews(test_path)
    validate_splits(train, test)
    if train.rating.value_counts().min() < folds:
        raise ValueError("Cada clase de entrenamiento debe tener al menos folds registros")
    X_train, y_train = train.review_text.tolist(), train.rating.to_numpy()
    X_test, y_test = test.review_text.tolist(), test.rating.to_numpy()
    cv = StratifiedKFold(n_splits=folds, shuffle=True, random_state=seed)
    pipeline = create_pipeline(random_state=seed)
    grid = GridSearchCV(
        estimator=pipeline,
        param_grid={
            "nlp__method": list(methods),
            "tfidf__ngram_range": [(1, 1), (1, 2)],
            "classifier__C": list(c_values),
        },
        scoring={"macro_f1": "f1_macro", "accuracy": "accuracy", "neg_mae": "neg_mean_absolute_error"},
        refit="macro_f1", cv=cv, n_jobs=1, error_score="raise", return_train_score=False,
    )
    grid.fit(X_train, y_train)
    result_rows = []
    for i, params in enumerate(grid.cv_results_["params"]):
        result_rows.append({
            "method": params["nlp__method"],
            "ngrams": "1" if params["tfidf__ngram_range"] == (1, 1) else "1-2",
            "C": float(params["classifier__C"]),
            "cv_macro_f1_mean": float(grid.cv_results_["mean_test_macro_f1"][i]),
            "cv_macro_f1_std": float(grid.cv_results_["std_test_macro_f1"][i]),
            "cv_accuracy_mean": float(grid.cv_results_["mean_test_accuracy"][i]),
            "cv_mae_mean": float(-grid.cv_results_["mean_test_neg_mae"][i]),
        })
    # Baseline sencillo: predice siempre la clase más frecuente de entrenamiento.
    baseline = DummyClassifier(strategy="most_frequent")
    baseline.fit(np.zeros((len(y_train), 1)), y_train)
    baseline_metrics = score(y_test, baseline.predict(np.zeros((len(y_test), 1))))
    predictions = grid.best_estimator_.predict(X_test)
    final_metrics = score(y_test, predictions)
    # Ejemplos fallidos con etiquetas/predicciones, sin datos personales adicionales.
    errors = []
    for index, (text, true, pred) in enumerate(zip(X_test, y_test, predictions)):
        if true != pred:
            errors.append({"row_index_in_test": index, "review_text": text,
                           "actual": int(true), "predicted": int(pred),
                           "absolute_error": int(abs(true - pred))})
    errors.sort(key=lambda r: (-r["absolute_error"], r["row_index_in_test"]))
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    joblib.dump(grid.best_estimator_, out / "pipeline.joblib")
    with (out / "experiments.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(result_rows[0]))
        writer.writeheader()
        writer.writerows(result_rows)
    with (out / "errors.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["row_index_in_test", "review_text", "actual", "predicted", "absolute_error"])
        writer.writeheader()
        writer.writerows(errors[:100])
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "selection_rule": "max CV macro_f1 on train only",
        "best_params": {"method": grid.best_params_["nlp__method"],
                        "ngram_range": list(grid.best_params_["tfidf__ngram_range"]),
                        "C": float(grid.best_params_["classifier__C"])},
        "best_cv_macro_f1": float(grid.best_score_),
        "cv_folds": folds,
        "train_size": len(train), "test_size": len(test), "labels": LABELS,
        "baseline": baseline_metrics, "final_test": final_metrics,
        "num_errors": len(errors), "error_examples_exported": min(100, len(errors)),
    }
    (out / "metrics.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main():
    p = argparse.ArgumentParser(description="Comparación reproducible de NLP, n-gramas y C con validación cruzada")
    p.add_argument("--train", required=True)
    p.add_argument("--test", required=True)
    p.add_argument("--output-dir", default="models/final")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--folds", type=int, default=3)
    p.add_argument("--methods", nargs="+", choices=["stemming", "lemmatization", "none"], default=["stemming", "lemmatization"])
    p.add_argument("--c-values", nargs="+", type=float, default=[0.1, 1.0, 10.0])
    args = p.parse_args()
    print(json.dumps(run_experiments(args.train, args.test, args.output_dir, args.seed,
                                     args.folds, tuple(args.methods), tuple(args.c_values)),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
