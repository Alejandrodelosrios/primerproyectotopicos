from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.predict import ModelSummary, Prediction, PredictResponse
from app.schemas.review import ReviewRequest
from app.services.model_service import is_model_loaded, predict

router = APIRouter(tags=["Prediction"])


@router.post("/predict", response_model=PredictResponse,
             summary="Predecir la puntuacion (1 a 5) de una reseña",
             responses={503: {"description": "El modelo no esta disponible"}}
             )
def predict_review(request: ReviewRequest,
                   model_loaded: bool = Depends(is_model_loaded)):
    """
     Recibe el texto de una reseña y devuelve las estrellas predichas,
     la confianza y la probabilidad de cada puntuacion.
     Devuelve 503 si el modelo no esta cargado
    """
    if not model_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El modelo no esta disponible",
        )

    result = predict(request.text)
    return PredictResponse(
        prediction=Prediction(
            stars=result["stars"],
            confidence=result["confidence"],
            probabilities=result["probabilities"],
        ),
        model=ModelSummary(name=result["model_name"], method=result["method"]),
    )