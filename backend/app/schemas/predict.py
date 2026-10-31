from pydantic import BaseModel, Field


class Prediction(BaseModel):
    stars: int = Field(ge=1, le=5, description="Puntuacion predicha")
    confidence: float = Field(ge=0, le=1,
                              description="Probabilidad de la clase predicha")
    # Clave = estrellas ("1" a "5"), valor = probabilidad
    probabilities: dict[str, float]


class ModelSummary(BaseModel):
    name: str
    method: str


class PredictResponse(BaseModel):
    """Puntuacion estimada de una reseña, con probabilidades y modelo usado"""
    prediction: Prediction
    model: ModelSummary