from fastapi import APIRouter

from . import workflows

router = APIRouter()
router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
