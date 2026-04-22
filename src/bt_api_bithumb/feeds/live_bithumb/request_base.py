from __future__ import annotations

import hashlib
import hmac
import time
import uuid

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed
from bt_api_base.feeds.http_client import HttpClient
from bt_api_base.logging_factory import get_logger

from bt_api_bithumb.exchange_data import BithumbExchangeDataSpot


class BithumbRequestData(Feed):
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
        self.data_queue = data_queue
        self.exchange_name = kwargs.get("exchange_name", "BITHUMB___SPOT")
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self._params = BithumbExchangeDataSpot()
        self._params.api_key = kwargs.get("public_key") or kwargs.get("api_key")
        self._params.api_secret = (
            kwargs.get("private_key") or kwargs.get("secret_key") or kwargs.get("api_secret")
        )
        self.request_logger = get_logger("bithumb_feed")
        self.async_logger = get_logger("bithumb_feed")
        self._http_client = HttpClient(venue=self.exchange_name, timeout=10)

    def _generate_signature(self, params):
        secret = self._params.api_secret
        if secret:
            sorted_params = sorted(params.items())
            query_string = "&".join(f"{k}={v}" for k, v in sorted_params)
            signature = hmac.new(
                secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
            ).hexdigest()
            return signature
        return ""

    def _get_auth_params(self):
        params = {
            "apiKey": self._params.api_key,
            "timestamp": str(int(time.time() * 1000)),
            "msgNo": str(uuid.uuid4()).replace("-", "")[:32],
        }
        signature = self._generate_signature(params)
        if signature:
            params["signature"] = signature
        return params

    def request(self, path, params=None, body=None, extra_data=None, timeout=10):
        method = path.split()[0] if " " in path else "GET"
        request_path = "/" + path.split()[1] if " " in path else path

        headers = {"Content-Type": "application/json"}

        is_private = any(
            x in path
            for x in [
                "placeOrder",
                "cancelOrder",
                "orderDetail",
                "singleOrder",
                "orderList",
                "assetList",
            ]
        )

        request_params = params.copy() if params else {}
        request_body = body.copy() if body else {}

        if is_private:
            auth_params = self._get_auth_params()
            if method == "POST":
                request_body.update(auth_params)
            else:
                request_params.update(auth_params)

        try:
            response = self._http_client.request(
                method=method,
                url=self._params.rest_url + request_path,
                headers=headers,
                json_data=request_body if method == "POST" and request_body else None,
                params=request_params if method == "GET" else None,
            )
            return self._process_response(response, extra_data)
        except Exception as e:
            self.request_logger.error(f"Request failed: {e}")
            raise

    async def async_request(self, path, params=None, body=None, extra_data=None, timeout=5):
        method = path.split()[0] if " " in path else "GET"
        request_path = "/" + path.split()[1] if " " in path else path

        headers = {"Content-Type": "application/json"}
        is_private = any(
            x in path
            for x in [
                "placeOrder",
                "cancelOrder",
                "orderDetail",
                "singleOrder",
                "orderList",
                "assetList",
                "account",
                "balance",
            ]
        )
        request_params = params.copy() if params else {}
        request_body = body.copy() if body else {}

        if is_private:
            auth_params = self._get_auth_params()
            if method == "POST":
                request_body.update(auth_params)
            else:
                request_params.update(auth_params)

        try:
            response = await self._http_client.async_request(
                method=method,
                url=self._params.rest_url + request_path,
                headers=headers,
                json_data=request_body if method == "POST" and request_body else None,
                params=request_params if method == "GET" else None,
            )
            return self._process_response(response, extra_data)
        except Exception as e:
            self.async_logger.error(f"Async request failed: {e}")
            raise

    def async_callback(self, future):
        try:
            result = future.result()
            if result is not None:
                self.push_data_to_queue(result)
        except Exception as e:
            self.async_logger.error(f"Async callback error: {e}")

    def _process_response(self, response, extra_data=None):
        if extra_data is None:
            extra_data = {}
        return RequestData(response, extra_data)

    def push_data_to_queue(self, data):
        if self.data_queue is not None:
            self.data_queue.put(data)

    def connect(self):
        pass

    def disconnect(self):
        super().disconnect()

    def is_connected(self):
        return True
