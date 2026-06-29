from fastapi import APIRouter
from .cases import router as cases_router

router = APIRouter(prefix="/v1")
router.include_router(cases_router)