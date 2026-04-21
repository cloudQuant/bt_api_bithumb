from __future__ import annotations

from bt_api_base.containers.exchanges.exchange_data import ExchangeData


class BithumbExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "bithumb"
        self.rest_url = "https://global-openapi.bithumb.pro/openapi/v1"
        self.wss_url = "wss://global-api.bithumb.pro/message/realtime"
        self.kline_periods = {
            "1m": "m1",
            "3m": "m3",
            "5m": "m5",
            "15m": "m15",
            "30m": "m30",
            "1h": "h1",
            "2h": "h2",
            "4h": "h4",
            "6h": "h6",
            "8h": "h8",
            "12h": "h12",
            "1d": "d1",
            "3d": "d3",
            "1w": "w1",
            "1M": "M1",
        }
        self.legal_currency = ["USDT", "USD", "BTC", "ETH", "KRW"]
        self.rest_paths = {}
        self.wss_paths = {}

    def get_period(self, period: str) -> str:
        if period not in self.kline_periods:
            return period
        return self.kline_periods[period]


class BithumbExchangeDataSpot(BithumbExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "SPOT"
        self.api_key: str | None = None
        self.api_secret: str | None = None
