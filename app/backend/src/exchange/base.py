from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class OrderRequest:
    symbol: str
    side: str  # "buy" or "sell"
    quantity: float
    type: str = "MARKET"
    price: float | None = None
    sl: float | None = None
    tp: float | None = None
    tag: str | None = None


class ExchangeClient(ABC):
    """Abstract exchange client used by order router."""

    @abstractmethod
    async def place_order(self, order: OrderRequest) -> Dict[str, Any]:
        """Place an order and return exchange response."""

    @abstractmethod
    async def get_balances(self) -> Dict[str, float]:
        """Return available balances."""

    @abstractmethod
    async def get_positions(self) -> Dict[str, Any]:
        """Return current open positions."""
