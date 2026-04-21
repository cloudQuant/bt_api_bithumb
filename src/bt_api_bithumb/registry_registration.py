from __future__ import annotations

from bt_api_base.registry import ExchangeRegistry

from bt_api_bithumb.exchange_data import BithumbExchangeDataSpot
from bt_api_bithumb.feeds.live_bithumb.spot import BithumbRequestDataSpot


def register_bithumb(registry: ExchangeRegistry | type[ExchangeRegistry]) -> None:
    registry.register_feed("BITHUMB___SPOT", BithumbRequestDataSpot)
    registry.register_exchange_data("BITHUMB___SPOT", BithumbExchangeDataSpot)


def register(registry: ExchangeRegistry | None = None) -> None:
    if registry is None:
        register_bithumb(ExchangeRegistry)
        return
    register_bithumb(registry)
