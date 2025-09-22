import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from services.risk import RiskConfig, RiskManager


def test_position_size_computation():
    rm = RiskManager(RiskConfig(per_trade_risk_pct=1.0))
    size = rm.compute_position_size(price=100.0, stop=90.0)
    assert round(size, 2) == 10.0  # risk 100 on 10 diff


def test_stop_after_n_losses_blocks_trading():
    cfg = RiskConfig(stop_after_n_losses=2)
    rm = RiskManager(cfg)
    assert rm.can_trade()
    rm.register_trade_result(-10)
    assert rm.can_trade()
    rm.register_trade_result(-5)
    assert not rm.can_trade()
