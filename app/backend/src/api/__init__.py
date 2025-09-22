from fastapi import APIRouter

from . import trade, workflows, optimize

router = APIRouter()
router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
router.include_router(trade.router, prefix="/trade", tags=["trade"])
router.include_router(optimize.router, prefix="/optimize", tags=["optimize"])
