import joblib
import pytest

from app.services import model_service


@pytest.fixture(autouse=True)
def reset_model(monkeypatch):
    """Cada test empieza sin modelo cargado."""
    monkeypatch.setattr(model_service, "_model", None)


def test_load_model_with_valid_file_marks_model_as_loaded(tmp_path):
    model_file = tmp_path / "pipeline.joblib"
    joblib.dump({"fake": "model"}, model_file)

    model_service.load_model(model_file)

    assert model_service.is_model_loaded() is True


def test_load_model_with_missing_file_stays_unloaded(tmp_path):
    model_service.load_model(tmp_path / "no_existe.joblib")

    assert model_service.is_model_loaded() is False


def test_load_model_with_empty_file_stays_unloaded(tmp_path):
    empty_file = tmp_path / "pipeline.joblib"
    empty_file.touch()

    model_service.load_model(empty_file)

    assert model_service.is_model_loaded() is False


def test_load_model_with_corrupt_file_stays_unloaded(tmp_path):
    corrupt_file = tmp_path / "pipeline.joblib"
    corrupt_file.write_text("esto no es un modelo")

    model_service.load_model(corrupt_file)

    assert model_service.is_model_loaded() is False