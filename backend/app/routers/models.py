from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.models import (
    ExperimentsResponse,
    MetricsResponse,
    ModelInfoResponse,
)
from app.services.model_service import get_model_info, is_model_loaded
from app.services.report_service import read_experiments, read_metrics

router = APIRouter(prefix="/models", tags=["Model"])

NO_RESULTS = ("No hay resultados de entrenamiento. Ejecuta: "
              "python -m src.models.experiments")


@router.get("/info", response_model=ModelInfoResponse,
            summary="Modelo activo y su configuracion",
            responses={503: {"description": "El modelo no esta disponible"}})
def model_info(model_loaded: bool = Depends(is_model_loaded)):
    if not model_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El modelo no esta disponible",
        )
    return get_model_info()


@router.get("/metrics", response_model=MetricsResponse,
            summary="Resultados del entrenamiento",
            responses={404: {"description": "Aun no hay metricas"}})
def model_metrics():
    try:
        return read_metrics()
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=NO_RESULTS)


@router.get("/experiments", response_model=ExperimentsResponse,
            summary="Comparacion de configuraciones (stemming, lematizacion...)",
            responses={404: {"description": "Aun no hay experimentos"}})
def model_experiments():
    try:
        return ExperimentsResponse(experiments=read_experiments())
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=NO_RESULTS)