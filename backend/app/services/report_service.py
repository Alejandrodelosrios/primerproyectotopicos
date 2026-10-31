import csv
import json
from app.core import config


def read_metrics() -> dict:
    """
    Lee las metricas del entrenamiento (models/final/metrics.json).
    Lanza FileNotFoundError si todavia no se ha corrido el experimento.
    Se lee config.METRICS_PATH al llamar (no al importar) para poder
    cambiar la ruta en las pruebas.
    """
    with open(config.METRICS_PATH, encoding="utf-8") as file:
        return json.load(file)


def read_experiments() -> list[dict]:
    """
    Lee la comparacion de configuraciones (models/final/experiments.csv).
    Devuelve una fila por experimento; pydantic convierte los numeros.
    Lanza FileNotFoundError si el archivo no existe.
    """
    with open(config.EXPERIMENTS_PATH, encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))