from pydantic import BaseModel


class ModelInfoResponse(BaseModel):
    """Modelo activo y su configuracion"""
    model_name: str
    model_version: str
    nlp_method: str
    vectorizer: str
    ngram_range: list[int]
    classes: list[int]
    artifact_path: str


class BestParams(BaseModel):
    method: str
    ngram_range: list[int]
    C: float


class EvaluationMetrics(BaseModel):
    accuracy: float
    macro_f1: float
    mae: float
    # Filas = estrella real, columnas = estrella predicha (orden de `labels`)
    confusion_matrix: list[list[int]]


class MetricsResponse(BaseModel):
    """Resultados del entrenamiento (leidos de models/final/metrics.json)"""
    created_at: str | None = None
    selection_rule: str
    best_params: BestParams
    best_cv_macro_f1: float
    cv_folds: int
    train_size: int
    test_size: int
    labels: list[int]
    baseline: EvaluationMetrics
    final_test: EvaluationMetrics


class ExperimentRow(BaseModel):
    method: str
    ngrams: str
    C: float
    cv_macro_f1_mean: float
    cv_macro_f1_std: float
    cv_accuracy_mean: float
    cv_mae_mean: float


class ExperimentsResponse(BaseModel):
    """Comparacion de configuraciones (leida de models/final/experiments.csv)"""
    experiments: list[ExperimentRow]