from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI()

@app.get("/health")
async def get_health():
    return {"status": "ok"}

app.include_router(api_router)