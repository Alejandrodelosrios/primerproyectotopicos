from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.preprocess import router as preprocess_router
from app.services.model_service import load_model
API_V1_PREFIX = "/api/v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
     Lo que esta antes del yield corre al iniciar la app;
     lo que va despues, al apagarla
    """
    load_model()
    yield


app = FastAPI(title="reseña de productos",
              description= """API que consume el modelo de NLP 
                        para estimar la puntuación de una reseña.""",
              lifespan=lifespan,
             )

app.include_router(health_router, prefix=API_V1_PREFIX)
app.include_router(preprocess_router, prefix=API_V1_PREFIX)