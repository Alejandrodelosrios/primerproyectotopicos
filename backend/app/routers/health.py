from fastapi import APIRouter,Depends,Response, status
from app.schemas.health import HealthResponse
from app.services.model_service import is_model_loaded

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse,
            summary="Verificar el estado del servicio",
            responses = {503: {"description": HealthResponse,
                               "description": """el modelo no
                                              esta disponible"""
                               }
                        }
            )
def get_health(response: Response,
               model_loaded: bool = Depends(is_model_loaded)
              )-> HealthResponse:
        """
         Devuelve 200 si la api y el modelo funcionan,
         Devuelve 503 si el modelo no esta disponible
        """
        if not model_loaded:
                response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                return HealthResponse(status = "degraded", model_loaded=False)
        
        return HealthResponse(status = "ok", model_loaded=True)
