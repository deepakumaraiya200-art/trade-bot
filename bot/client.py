import hashlib
import hmac
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests
import logging

logger = logging.getLogger("trading_bot")

BASE_URL = "https://testnet.binancefuture.com"


class BinanceClientError(Exception):
    pass


class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})
        logger.info("BinanceFuturesClient initialised (testnet).")

    def _sign(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _request(self, method, path, params=None, signed=False):
        url = f"{self.base_url}{path}"
        params = params or {}
        if signed:
            params = self._sign(params)
        logger.debug(f"API REQUEST  → {method} {url} | params={params}")
        try:
            response = self.session.request(method, url, params=params)
            data = response.json()
        except requests.exceptions.RequestException as exc:
            logger.error(f"Network error: {exc}")
            raise BinanceClientError(f"Network error: {exc}") from exc
        logger.debug(f"API RESPONSE ← status={response.status_code} | body={data}")
        if response.status_code >= 400:
            msg = data.get("msg", "Unknown API error")
            code = data.get("code", response.status_code)
            logger.error(f"API error [{code}]: {msg}")
            raise BinanceClientError(f"API error [{code}]: {msg}")
        return data

    def ping(self):
        return self._request("GET", "/fapi/v1/ping")

    def get_server_time(self):
        return self._request("GET", "/fapi/v1/time")

    def get_ticker_price(self, symbol):
        return self._request("GET", "/fapi/v1/ticker/price", {"symbol": symbol})

    def get_account(self):
        return self._request("GET", "/fapi/v2/account", signed=True)

    def place_order(self, symbol, side, order_type, quantity, price=None, time_in_force="GTC"):
        params = {"symbol": symbol, "side": side, "type": order_type, "quantity": quantity}
        if order_type == "LIMIT":
            if price is None:
                raise BinanceClientError("Price is required for LIMIT orders.")
            params["price"] = price
            params["timeInForce"] = time_in_force
        return self._request("POST", "/fapi/v1/order", params=params, signed=True)
