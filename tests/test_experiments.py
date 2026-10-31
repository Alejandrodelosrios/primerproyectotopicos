import csv
import json

import pandas as pd
import pytest

from src.models.experiments import run_experiments, score


def build_csv(path, suffix):
    rows = []
    for stars, phrase in [(1,"pésimo roto"),(2,"malo defectuoso"),(3,"normal aceptable"),
                          (4,"bueno recomendable"),(5,"excelente magnífico")]:
        for i in range(6):
            rows.append({"review_text": f"{phrase} {suffix} referencia{i} codigo{stars}", "rating": stars})
    pd.DataFrame(rows).to_csv(path, index=False)


def test_scoring():
    r = score([1, 2, 3, 4, 5], [1, 2, 2, 4, 5])
    assert r["accuracy"] == pytest.approx(0.8)
    assert r["mae"] == pytest.approx(0.2)
    assert len(r["confusion_matrix"]) == 5


def test_experiment_end_to_end(tmp_path):
    train, test, output = tmp_path / "train.csv", tmp_path / "test.csv", tmp_path / "results"
    build_csv(train, "entrenamiento")
    build_csv(test, "prueba")
    report = run_experiments(train, test, output, folds=2,
                             methods=("stemming",), c_values=(1.0,))
    assert (output / "pipeline.joblib").is_file()
    assert (output / "metrics.json").is_file()
    assert (output / "experiments.csv").is_file()
    assert (output / "errors.csv").is_file()
    assert len(list(csv.DictReader((output / "experiments.csv").open(encoding="utf-8")))) == 2
    assert report["best_params"]["method"] == "stemming"
    assert report["train_size"] == 30
    assert 0 <= report["final_test"]["accuracy"] <= 1


def test_rejects_insufficient_records_per_fold(tmp_path):
    train, test = tmp_path / "train.csv", tmp_path / "test.csv"
    build_csv(train, "entrenamiento")
    build_csv(test, "prueba")
    with pytest.raises(ValueError, match="folds"):
        run_experiments(train, test, tmp_path / "out", folds=7,
                        methods=("stemming",), c_values=(1.0,))


def test_rejects_bad_hyperparameters(tmp_path):
    with pytest.raises(ValueError, match="C"):
        run_experiments("missing.csv", "missing.csv", c_values=(-1,))
