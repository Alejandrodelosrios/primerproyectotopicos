from pathlib import Path

INFO_URL = "/api/v1/models/info"
METRICS_URL = "/api/v1/models/metrics"
EXPERIMENTS_URL = "/api/v1/models/experiments"


# ---------- /models/info ----------

def test_info_returns_the_loaded_model_configuration(client, model_available):
    response = client.get(INFO_URL)

    assert response.status_code == 200
    body = response.json()
    assert body["model_name"] == "LogisticRegression"
    assert body["vectorizer"] == "TfidfVectorizer"
    assert body["classes"] == [1, 2, 3, 4, 5]
    assert body["nlp_method"] in ("stemming", "lemmatization", "none")
    assert len(body["ngram_range"]) == 2


def test_info_artifact_path_is_relative_and_does_not_leak_local_folders(client, model_available):
    path = client.get(INFO_URL).json()["artifact_path"]

    assert not Path(path).is_absolute()
    assert path.endswith("pipeline.joblib")


def test_info_when_model_is_not_loaded_returns_503(client, model_unavailable):
    assert client.get(INFO_URL).status_code == 503


# ---------- /models/metrics ----------

def test_metrics_returns_training_results(client):
    response = client.get(METRICS_URL)

    assert response.status_code == 200
    body = response.json()
    assert body["labels"] == [1, 2, 3, 4, 5]
    assert body["best_params"]["method"] in ("stemming", "lemmatization")
    assert 0 <= body["final_test"]["accuracy"] <= 1
    assert body["train_size"] > 0 and body["test_size"] > 0


def test_metrics_include_complete_5x5_confusion_matrices(client):
    body = client.get(METRICS_URL).json()

    for block in ("baseline", "final_test"):
        matrix = body[block]["confusion_matrix"]
        assert len(matrix) == 5
        assert all(len(row) == 5 for row in matrix)


def test_metrics_final_test_beats_the_baseline(client):
    body = client.get(METRICS_URL).json()

    assert body["final_test"]["macro_f1"] > body["baseline"]["macro_f1"]


def test_metrics_without_results_file_returns_404(client, monkeypatch, tmp_path):
    monkeypatch.setattr("app.core.config.METRICS_PATH", tmp_path / "no_existe.json")

    response = client.get(METRICS_URL)

    assert response.status_code == 404
    assert "experiments" in response.json()["detail"]


# ---------- /models/experiments ----------

def test_experiments_returns_one_row_per_configuration(client):
    response = client.get(EXPERIMENTS_URL)

    assert response.status_code == 200
    rows = response.json()["experiments"]
    assert len(rows) > 0
    assert {"method", "ngrams", "C", "cv_macro_f1_mean", "cv_macro_f1_std",
            "cv_accuracy_mean", "cv_mae_mean"} == set(rows[0])


def test_experiments_compare_stemming_and_lemmatization(client):
    rows = client.get(EXPERIMENTS_URL).json()["experiments"]

    assert {"stemming", "lemmatization"} <= {row["method"] for row in rows}


def test_experiments_values_are_numbers(client):
    row = client.get(EXPERIMENTS_URL).json()["experiments"][0]

    assert isinstance(row["C"], float)
    assert isinstance(row["cv_macro_f1_mean"], float)


def test_experiments_without_results_file_returns_404(client, monkeypatch, tmp_path):
    monkeypatch.setattr("app.core.config.EXPERIMENTS_PATH", tmp_path / "no_existe.csv")

    assert client.get(EXPERIMENTS_URL).status_code == 404