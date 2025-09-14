from fastapi import FastAPI

from .api import router as api_router


app = FastAPI(title="Strategy Builder API")
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok"}
