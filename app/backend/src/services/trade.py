from __future__ import annotations

from typing import Any, Dict

from ..core.config import settings
from ..exchange import BinanceFuturesClient, OrderRequest, PaperBroker, ExchangeClient
from .risk import RiskConfig, RiskManager


risk_manager = RiskManager(RiskConfig())
_trading_enabled = True
_exchange: ExchangeClient | None = None


def get_exchange() -> ExchangeClient:
    global _exchange
    if _exchange is None:
        if settings.is_paper or not settings.binance_api_key:
            _exchange = PaperBroker()
        else:
            _exchange = BinanceFuturesClient(settings.binance_api_key, settings.binance_api_secret)
    return _exchange


def enable_trading(enabled: bool) -> None:
    global _trading_enabled
    _trading_enabled = enabled


def trading_enabled() -> bool:
    return _trading_enabled and risk_manager.can_trade()


def place_order(data: Dict[str, Any]) -> Dict[str, Any]:
    if not trading_enabled():
        return {"status": "disabled"}
    price = data.get("price", 0.0)
    sl = data.get("sl", price)
    qty = data.get("qty_abs")
    if qty is None:
        qty_pct = data.get("qty_pct", 0.0)
        risk_manager.config.per_trade_risk_pct = qty_pct
        qty = risk_manager.compute_position_size(price, sl)
    order = OrderRequest(
        symbol=data["symbol"],
        side=data["side"],
        quantity=qty,
        type=data.get("type", "MARKET"),
        price=price,
        sl=sl,
        tp=data.get("tp"),
        tag=data.get("tag"),
    )
    return run_async(get_exchange().place_order(order))


def status() -> Dict[str, Any]:
    client = get_exchange()
    balances = run_async(client.get_balances())
    positions = run_async(client.get_positions())
    return {"balances": balances, "positions": positions}


def run_async(awaitable):
    """Run async function in sync context (for demo/testing)."""
    import asyncio

    return asyncio.get_event_loop().run_until_complete(awaitable)
