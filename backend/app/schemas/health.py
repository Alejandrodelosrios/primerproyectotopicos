from typing import Literal
from pydantic import BaseModel

class HealthResponse(BaseModel):
    """
     Estado del servicio y del modelo.
    """
    status: Literal["ok","degraded"]
    model_loaded: bool 