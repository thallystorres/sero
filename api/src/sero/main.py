from fastapi import FastAPI

from sero.devotions.router import router as devotions_router
from sero.streak.router import router as streak_router

app = FastAPI()
app.include_router(devotions_router)
app.include_router(streak_router)


@app.get("/health")
async def health() -> dict[str, bool]:
    return {"healthy": True}
