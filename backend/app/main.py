from fastapi import FastAPI

app = FastAPI(title="reseña de productos")


@app.get("/")
def root():
    return {"message": "proyecto de topicos"}