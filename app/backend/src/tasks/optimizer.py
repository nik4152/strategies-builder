from __future__ import annotations

from celery import shared_task
from datetime import datetime

from ..optimizer import run_optimization


@shared_task
def optimize_workflow(run_id: str, algorithm: str, space: dict, start: str, end: str, k_folds: int) -> dict:
    def dummy_eval(params: dict, fold) -> dict:
        # Placeholder: performance proportional to sum of params
        score = sum(params.values())
        return {"PF": float(score), "Sharpe": float(score / 2), "MaxDD": -float(score)}

    return run_optimization(run_id, algorithm, space, dummy_eval,
                            datetime.fromisoformat(start), datetime.fromisoformat(end), k_folds)
