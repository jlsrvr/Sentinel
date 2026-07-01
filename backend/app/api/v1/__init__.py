from fastapi import APIRouter
from .cases import router as cases_router
from .decisions import router as decisions_router

router = APIRouter(prefix="/v1")
router.include_router(cases_router)
router.include_router(decisions_router)