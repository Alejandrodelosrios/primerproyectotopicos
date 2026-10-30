from typing import Literal
from pydantic import BaseModel

class HealthResponse(BaseModel):
    """
     Estado del servicio y del modelo.
    """
    status: Literal["healthy","degraded"]
    model_loaded: bool
    # Version del modelo cargado ("final", "legacy").
    # Es None cuando no hay modelo cargado.
    model_version: str | None = None