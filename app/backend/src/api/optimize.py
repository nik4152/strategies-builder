from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..optimizer import RUNS, RESULTS
from ..tasks.optimizer import optimize_workflow


class OptimizeRequest(BaseModel):
    algorithm: str = "grid"
    space: dict[str, list | tuple]
    start: datetime
    end: datetime
    k_folds: int = 3


router = APIRouter()


@router.post("/run")
async def run_optimize(req: OptimizeRequest) -> dict:
    run_id = str(uuid4())
    RUNS[run_id] = {"status": "pending"}
    optimize_workflow.delay(run_id, req.algorithm, req.space, req.start.isoformat(), req.end.isoformat(), req.k_folds)
    return {"id": run_id}


@router.get("/{run_id}")
async def get_optimize(run_id: UUID) -> dict:
    run = RUNS.get(str(run_id))
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"run": run, "results": RESULTS.get(str(run_id), [])}
