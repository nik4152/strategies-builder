from __future__ import annotations

from celery import shared_task

from ..services import trade


@shared_task
def route_order(data: dict) -> dict:
    return trade.place_order(data)


@shared_task
def sync_positions() -> dict:
    return trade.status()["positions"]


@shared_task
def sync_balances() -> dict:
    return trade.status()["balances"]
