import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.model_service import is_model_loaded


@pytest.fixture
def client():
    """Cliente HTTP de prueba: simula peticiones a la API sin levantar un servidor."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def model_available():
    """Simula que el modelo SÍ está cargado."""
    app.dependency_overrides[is_model_loaded] = lambda: True
    yield
    app.dependency_overrides.clear()  # limpia para no afectar otros tests


@pytest.fixture
def model_unavailable():
    """Simula que el modelo NO está cargado."""
    app.dependency_overrides[is_model_loaded] = lambda: False
    yield
    app.dependency_overrides.clear()