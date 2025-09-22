from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from ..services import trade

router = APIRouter()


class TradeEnable(BaseModel):
    enabled: bool


@router.post("/enable")
async def enable(body: TradeEnable) -> dict[str, bool]:
    trade.enable_trading(body.enabled)
    return {"enabled": trade.trading_enabled()}


class OrderBody(BaseModel):
    symbol: str
    side: str
    qty_pct: float | None = None
    qty_abs: float | None = None
    type: str = "MARKET"
    price: float | None = None
    sl: float | None = None
    tp: float | None = None
    tag: str | None = None


@router.post("/order")
async def order(body: OrderBody) -> dict[str, Any]:
    return trade.place_order(body.model_dump())


@router.get("/status")
async def status() -> dict[str, Any]:
    return trade.status()
