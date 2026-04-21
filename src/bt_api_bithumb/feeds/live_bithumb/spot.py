from __future__ import annotations

import time
from typing import Any

from bt_api_base.feeds.capability import Capability
from bt_api_bithumb.feeds.live_bithumb.request_base import BithumbRequestData


class BithumbRequestDataSpot(BithumbRequestData):
    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
        }

    def __init__(self, data_queue=None, **kwargs) -> None:
        super().__init__(data_queue, **kwargs)
        self.exchange_name = kwargs.get("exchange_name", "BITHUMB___SPOT")

    def _convert_symbol(self, symbol):
        if "/" in symbol:
            return symbol.replace("/", "-")
        elif "_" in symbol:
            return symbol.replace("_", "-")
        if "-" in symbol:
            return symbol
        for quote in ["USDT", "USD", "BTC", "ETH", "KRW"]:
            if symbol.endswith(quote) and len(symbol) > len(quote):
                base = symbol[: -len(quote)]
                return f"{base}-{quote}"
        return symbol

    def _get_tick(self, symbol, extra_data=None, **kwargs):
        path = "GET /spot/ticker"
        bithumb_symbol = self._convert_symbol(symbol)
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_tick",
                "symbol_name": bithumb_symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_tick_normalize_function,
            }
        )
        params = {"symbol": bithumb_symbol}
        return path, params, extra_data

    @staticmethod
    def _get_tick_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        data_list = input_data.get("data", [])
        if data_list and isinstance(data_list, list) and len(data_list) > 0:
            ticker = data_list[0]
            return [ticker], ticker is not None
        return [], False

    def get_tick(self, symbol, extra_data=None, **kwargs):
        path, params, extra = self._get_tick(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra)

    def async_get_tick(self, symbol, extra_data=None, **kwargs):
        path, params, extra = self._get_tick(symbol, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra), callback=self.async_callback
        )

    def _get_depth(self, symbol, count=20, extra_data=None, **kwargs):
        path = "GET /spot/orderBook"
        bithumb_symbol = self._convert_symbol(symbol)
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_depth",
                "symbol_name": bithumb_symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_depth_normalize_function,
            }
        )
        params = {"symbol": bithumb_symbol, "limit": count}
        return path, params, extra_data

    @staticmethod
    def _get_depth_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        depth = input_data.get("data", {})
        return [depth], depth is not None

    def get_depth(self, symbol, count=20, extra_data=None, **kwargs):
        path, params, extra = self._get_depth(symbol, count, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra)

    def async_get_depth(self, symbol, count=20, extra_data=None, **kwargs):
        path, params, extra = self._get_depth(symbol, count, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra), callback=self.async_callback
        )

    def _get_kline(self, symbol, period, count=20, extra_data=None, **kwargs):
        path = "GET /spot/kline"
        bithumb_symbol = self._convert_symbol(symbol)
        bithumb_period = self._params.get_period(period)
        end_time = int(time.time())
        start_time = end_time - 3600 * 24
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_kline",
                "symbol_name": bithumb_symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_kline_normalize_function,
            }
        )
        params = {
            "symbol": bithumb_symbol,
            "type": bithumb_period,
            "start": start_time,
            "end": end_time,
        }
        return path, params, extra_data

    @staticmethod
    def _get_kline_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        klines = input_data.get("data", [])
        return [klines], klines is not None

    def get_kline(self, symbol, period, count=20, extra_data=None, **kwargs):
        path, params, extra = self._get_kline(symbol, period, count, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra)

    def async_get_kline(self, symbol, period="1m", count=20, extra_data=None, **kwargs):
        path, params, extra = self._get_kline(symbol, period, count, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra), callback=self.async_callback
        )

    def _get_exchange_info(self, extra_data=None, **kwargs):
        path = "GET /spot/config"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_exchange_info",
                "symbol_name": "",
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_exchange_info_normalize_function,
            }
        )
        return path, {}, extra_data

    @staticmethod
    def _get_exchange_info_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        config = input_data.get("data", {})
        return [config], config is not None

    def get_exchange_info(self, extra_data=None, **kwargs):
        path, params, extra = self._get_exchange_info(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra)

    def _get_account(self, extra_data=None, **kwargs):
        path = "GET /spot/account"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_account",
                "symbol_name": "",
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_account_normalize_function,
            }
        )
        return path, {}, extra_data

    @staticmethod
    def _get_account_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        account = input_data.get("data", {})
        return [account], account is not None

    def get_account(self, symbol="ALL", extra_data=None, **kwargs):
        path, params, extra = self._get_account(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra)

    def async_get_account(self, symbol="ALL", extra_data=None, **kwargs):
        path, params, extra = self._get_account(extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra), callback=self.async_callback
        )

    def _get_balance(self, symbol=None, extra_data=None, **kwargs):
        path = "GET /spot/balance"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_balance",
                "symbol_name": symbol or "",
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_balance_normalize_function,
            }
        )
        params = {}
        if symbol:
            params["currency"] = symbol
        return path, params, extra_data

    @staticmethod
    def _get_balance_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        balance = input_data.get("data", {})
        return [balance], balance is not None

    def get_balance(self, symbol=None, extra_data=None, **kwargs):
        path, params, extra = self._get_balance(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra)

    def _make_order(
        self,
        symbol,
        volume,
        price,
        order_type,
        offset="open",
        post_only=False,
        client_order_id=None,
        extra_data=None,
        **kwargs,
    ):
        bithumb_symbol = self._convert_symbol(symbol)
        path = "POST /spot/placeOrder"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": bithumb_symbol,
                "asset_type": self.asset_type,
                "request_type": "make_order",
            }
        )
        params = {
            "symbol": bithumb_symbol,
            "side": offset.upper() if offset in ("BUY", "SELL", "buy", "sell") else "BUY",
            "type": order_type.upper(),
            "quantity": str(volume),
            "price": str(price),
        }
        return path, params, extra_data

    def make_order(
        self,
        symbol,
        volume,
        price,
        order_type,
        offset="open",
        post_only=False,
        client_order_id=None,
        extra_data=None,
        **kwargs,
    ):
        path, params, extra = self._make_order(
            symbol,
            volume,
            price,
            order_type,
            offset,
            post_only,
            client_order_id,
            extra_data,
            **kwargs,
        )
        return self.request(path, body=params, extra_data=extra)

    def _cancel_order(self, symbol, order_id, extra_data=None, **kwargs):
        bithumb_symbol = self._convert_symbol(symbol)
        path = "POST /spot/cancelOrder"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": bithumb_symbol,
                "asset_type": self.asset_type,
                "request_type": "cancel_order",
                "order_id": order_id,
            }
        )
        params = {"symbol": bithumb_symbol, "orderId": order_id}
        return path, params, extra_data

    def cancel_order(self, symbol, order_id, extra_data=None, **kwargs):
        path, params, extra = self._cancel_order(symbol, order_id, extra_data, **kwargs)
        return self.request(path, body=params, extra_data=extra)

    def _query_order(self, symbol, order_id, extra_data=None, **kwargs):
        bithumb_symbol = self._convert_symbol(symbol)
        path = "GET /spot/singleOrder"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": bithumb_symbol,
                "asset_type": self.asset_type,
                "request_type": "query_order",
                "order_id": order_id,
            }
        )
        params = {"symbol": bithumb_symbol, "orderId": order_id}
        return path, params, extra_data

    def query_order(self, symbol, order_id, extra_data=None, **kwargs):
        path, params, extra = self._query_order(symbol, order_id, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra)

    def _get_open_orders(self, symbol=None, extra_data=None, **kwargs):
        path = "GET /spot/orderList"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol or "",
                "asset_type": self.asset_type,
                "request_type": "get_open_orders",
            }
        )
        params = {}
        if symbol:
            params["symbol"] = self._convert_symbol(symbol)
        return path, params, extra_data

    def get_open_orders(self, symbol=None, extra_data=None, **kwargs):
        path, params, extra = self._get_open_orders(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra)
