from __future__ import annotations

from typing import Any, Dict

import ccxt.async_support as ccxt

from .base import ExchangeClient, OrderRequest


class BinanceFuturesClient(ExchangeClient):
    """Minimal Binance Futures client using ccxt."""

    def __init__(self, api_key: str | None = None, api_secret: str | None = None) -> None:
        self._client = ccxt.binanceusdm({
            "apiKey": api_key or "",
            "secret": api_secret or "",
            "enableRateLimit": True,
        })

    async def place_order(self, order: OrderRequest) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if order.type == "LIMIT" and order.price is not None:
            params["price"] = order.price
        return await self._client.create_order(
            symbol=order.symbol,
            type=order.type,
            side=order.side,
            amount=order.quantity,
            price=order.price,
            params=params,
        )

    async def get_balances(self) -> Dict[str, float]:
        bal = await self._client.fetch_balance()
        return {k: float(v["free"]) for k, v in bal["total"].items()}

    async def get_positions(self) -> Dict[str, Any]:
        return await self._client.fapiPrivateGetPositionRisk()
