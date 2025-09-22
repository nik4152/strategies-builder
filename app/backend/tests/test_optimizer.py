from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from optimizer.service import grid_search, walk_forward


def test_walk_forward_splits():
    start = datetime(2024, 1, 1)
    end = datetime(2024, 1, 11)
    folds = walk_forward(start, end, 2)
    assert len(folds) == 2
    assert folds[0].train_start == start
    assert folds[1].test_end == end


def test_grid_search_selects_best():
    def eval_fn(params, fold):
        score = params["x"]
        return {"PF": score}

    folds = walk_forward(datetime(2024, 1, 1), datetime(2024, 1, 11), 2)
    res = grid_search({"x": [1, 2, 3]}, eval_fn, folds)
    assert res[0]["params"]["x"] == 3
