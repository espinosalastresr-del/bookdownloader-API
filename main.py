from fastapi import FastAPI

from app.config import get_settings
from app.routes import router

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API para búsqueda y descarga de libros."
)

app.include_router(router)


@app.get("/", tags=["Root"])
async def root():

    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health():

    return {
        "status": "ok",
        "version": settings.VERSION
    }