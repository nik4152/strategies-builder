from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import product
from typing import Any, Callable, Dict, Iterable, List, Tuple

# In-memory stores for demo purposes
RUNS: Dict[str, Dict[str, Any]] = {}
RESULTS: Dict[str, List[Dict[str, Any]]] = {}


@dataclass
class Fold:
    train_start: datetime
    train_end: datetime
    test_start: datetime
    test_end: datetime


def walk_forward(start: datetime, end: datetime, k: int) -> List[Fold]:
    """Split [start,end] into k train-test folds without pandas."""
    total = end - start
    step = total / (2 * k)
    folds: List[Fold] = []
    cur = start
    for _ in range(k):
        train_start = cur
        train_end = cur + step
        test_start = train_end
        test_end = test_start + step
        folds.append(Fold(train_start, train_end, test_start, test_end))
        cur = test_end
    return folds


def aggregate(metrics_list: List[Dict[str, float]]) -> Dict[str, float]:
    if not metrics_list:
        return {}
    keys = metrics_list[0].keys()
    return {k: sum(m[k] for m in metrics_list) / len(metrics_list) for k in keys}


def grid_search(space: Dict[str, Iterable[Any]], evaluate: Callable[[Dict[str, Any], Fold], Dict[str, float]],
                folds: List[Fold]) -> List[Dict[str, Any]]:
    keys = list(space.keys())
    combos = product(*space.values())
    results: List[Dict[str, Any]] = []
    for combo in combos:
        params = dict(zip(keys, combo))
        metrics_list = [evaluate(params, f) for f in folds]
        metrics = aggregate(metrics_list)
        results.append({"params": params, "metrics": metrics})
    results.sort(key=lambda x: x["metrics"].get("PF", 0), reverse=True)
    return results


def bayesian_search(space: Dict[str, Tuple[float, float]], evaluate: Callable[[Dict[str, Any], Fold], Dict[str, float]],
                    folds: List[Fold], n_trials: int = 20) -> List[Dict[str, Any]]:
    import importlib

    optuna = importlib.import_module("optuna")

    def objective(trial: Any) -> float:
        params: Dict[str, Any] = {}
        for name, bounds in space.items():
            low, high = bounds
            params[name] = trial.suggest_float(name, low, high)
        metrics_list = [evaluate(params, f) for f in folds]
        metrics = aggregate(metrics_list)
        trial.set_user_attr("metrics", metrics)
        return metrics.get("PF", 0)

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)
    results = [
        {"params": t.params, "metrics": t.user_attrs.get("metrics", {})}
        for t in study.trials
    ]
    results.sort(key=lambda x: x["metrics"].get("PF", 0), reverse=True)
    return results


def run_optimization(run_id: str, algorithm: str, space: Dict[str, Any], evaluate: Callable[[Dict[str, Any], Fold], Dict[str, float]],
                     start: datetime, end: datetime, k_folds: int) -> Dict[str, Any]:
    folds = walk_forward(start, end, k_folds)
    if algorithm == "bayesian":
        results = bayesian_search(space, evaluate, folds)
    else:
        results = grid_search(space, evaluate, folds)
    best = results[0] if results else {}
    RUNS[run_id] = {"best_params": best.get("params"), "status": "done"}
    RESULTS[run_id] = results
    return RUNS[run_id]
