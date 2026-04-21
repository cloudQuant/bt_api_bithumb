from __future__ import annotations

from unittest.mock import MagicMock

from bt_api_bithumb.feeds.live_bithumb.request_base import BithumbRequestData


def test_bithumb_disconnect_closes_http_client() -> None:
    request_data = BithumbRequestData()
    request_data._http_client.close = MagicMock()

    request_data.disconnect()

    request_data._http_client.close.assert_called_once_with()


def test_bithumb_accepts_public_private_key_aliases() -> None:
    request_data = BithumbRequestData(public_key="public-key", private_key="secret-key")
    auth_params = request_data._get_auth_params()

    assert request_data._params.api_key == "public-key"
    assert request_data._params.api_secret == "secret-key"
    assert auth_params["apiKey"] == "public-key"
    assert "signature" in auth_params
