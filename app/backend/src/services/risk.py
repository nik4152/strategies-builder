from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class RiskConfig:
    max_concurrent_positions: int = 1
    daily_loss_limit_pct: float = 0.0
    stop_after_n_losses: int = 3
    per_trade_risk_pct: float = 1.0


@dataclass
class RiskState:
    equity: float = 10_000.0
    open_positions: int = 0
    consecutive_losses: int = 0
    daily_loss: float = 0.0
    last_reset: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    trading_enabled: bool = True


class RiskManager:
    def __init__(self, config: RiskConfig) -> None:
        self.config = config
        self.state = RiskState()

    def _reset_daily_if_needed(self) -> None:
        now = datetime.now(timezone.utc)
        if now.date() != self.state.last_reset.date():
            self.state.daily_loss = 0.0
            self.state.consecutive_losses = 0
            self.state.last_reset = now
            self.state.trading_enabled = True

    def compute_position_size(self, price: float, stop: float) -> float:
        """Compute quantity based on equity and risk pct."""
        risk_amount = self.state.equity * (self.config.per_trade_risk_pct / 100)
        risk_per_unit = abs(price - stop)
        if risk_per_unit == 0:
            return 0.0
        qty = risk_amount / risk_per_unit
        return max(qty, 0.0)

    def register_trade_result(self, pnl: float) -> None:
        self._reset_daily_if_needed()
        self.state.equity += pnl
        self.state.daily_loss += -min(pnl, 0)
        if pnl < 0:
            self.state.consecutive_losses += 1
        else:
            self.state.consecutive_losses = 0
        if self.state.consecutive_losses >= self.config.stop_after_n_losses:
            self.state.trading_enabled = False
        if self.config.daily_loss_limit_pct > 0 and self.state.daily_loss >= self.state.equity * (self.config.daily_loss_limit_pct / 100):
            self.state.trading_enabled = False

    def can_trade(self) -> bool:
        self._reset_daily_if_needed()
        return self.state.trading_enabled and self.state.open_positions < self.config.max_concurrent_positions
