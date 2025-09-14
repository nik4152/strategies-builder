from __future__ import annotations

from typing import Any, Dict

from .base import ExchangeClient, OrderRequest


class PaperBroker(ExchangeClient):
    """Simple paper trading engine with commission and slippage."""

    def __init__(self, commission: float = 0.0004, slippage: float = 0.0005) -> None:
        self.commission = commission
        self.slippage = slippage
        self.positions: Dict[str, Dict[str, Any]] = {}
        self.balance: float = 10_000.0

    async def place_order(self, order: OrderRequest) -> Dict[str, Any]:
        price = order.price or 0.0
        price *= 1 + self.slippage if order.side == "buy" else 1 - self.slippage
        cost = price * order.quantity
        fee = cost * self.commission
        self.balance -= cost + fee if order.side == "buy" else -(cost - fee)
        self.positions[order.symbol] = {
            "side": order.side,
            "qty": order.quantity,
            "price": price,
        }
        return {"status": "filled", "price": price, "fee": fee}

    async def get_balances(self) -> Dict[str, float]:
        return {"USDT": self.balance}

    async def get_positions(self) -> Dict[str, Any]:
        return self.positions
