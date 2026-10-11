from fastapi import FastAPI

from app.api import api_router
from app.core.config import settings

app = FastAPI(
    title="Ensemble Finder",
    version="0.1.0",
    debug=settings.debug,
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
