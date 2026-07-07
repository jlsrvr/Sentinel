from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router as api_router
from app.core.config import settings
from app.models import user, queue, case, decision, escalation, audit_log, content_exposure  # noqa: F401


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def get_health():
    return {"status": "ok"}

app.include_router(api_router)