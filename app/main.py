from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title="Ensemble Finder",
    version="0.1.0",
    debug=settings.debug,
)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok"}