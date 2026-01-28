"""
Binance Futures API Client.

Handles all communication with Binance Futures Testnet API.
"""

import time
import hmac
import hashlib
from typing import Optional, Dict, Any
from urllib.parse import urlencode
import logging

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

from bot.logging_config import log_api_request, log_api_response


logger = logging.getLogger("trading_bot.client")


class BinanceClientError(Exception):
    """Custom exception for Binance API errors."""
    pass


class BinanceFuturesClient:
    """
    Client for interacting with Binance Futures Testnet API.
    
    Attributes:
        base_url: Base URL for Binance Futures Testnet
        api_key: API key for authentication
        api_secret: API secret for signing requests
    """
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize Binance Futures client.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Use testnet environment (default: True)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://testnet.binancefuture.com" if testnet else "https://fapi.binance.com"
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        })
        
        logger.info(f"Initialized Binance Futures Client (testnet={testnet})")
        logger.debug(f"Base URL: {self.base_url}")
    
    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """
        Generate HMAC SHA256 signature for API request.
        
        Args:
            params: Request parameters
            
        Returns:
            Hex signature string
        """
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        signed: bool = False
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Binance API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Request parameters
            signed: Whether request requires signature
            
        Returns:
            Response data as dictionary
            
        Raises:
            BinanceClientError: If request fails
        """
        if params is None:
            params = {}
        
        # Add timestamp and signature for signed requests
        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["signature"] = self._generate_signature(params)
        
        url = f"{self.base_url}{endpoint}"
        
        # Log request
        log_api_request(logger, method, endpoint, params)
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=10)
            elif method.upper() == "POST":
                response = self.session.post(url, params=params, timeout=10)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, params=params, timeout=10)
            else:
                raise BinanceClientError(f"Unsupported HTTP method: {method}")
            
            # Log response
            log_api_response(logger, response.status_code, response.text)
            
            # Parse response
            try:
                data = response.json()
            except ValueError:
                raise BinanceClientError(f"Invalid JSON response: {response.text}")
            
            # Handle API errors
            if response.status_code != 200:
                error_msg = data.get("msg", "Unknown error")
                error_code = data.get("code", "N/A")
                raise BinanceClientError(
                    f"API Error [{error_code}]: {error_msg} (Status: {response.status_code})"
                )
            
            return data
            
        except Timeout:
            logger.error("Request timeout")
            raise BinanceClientError("Request timed out. Please check your internet connection.")
        
        except ConnectionError:
            logger.error("Connection error")
            raise BinanceClientError("Failed to connect to Binance API. Please check your internet connection.")
        
        except RequestException as e:
            logger.error(f"Request exception: {e}")
            raise BinanceClientError(f"Network error: {str(e)}")
    
    def test_connectivity(self) -> bool:
        """
        Test API connectivity.
        
        Returns:
            True if connection successful
            
        Raises:
            BinanceClientError: If connection fails
        """
        logger.info("Testing API connectivity...")
        
        try:
            self._make_request("GET", "/fapi/v1/ping")
            logger.info("✓ API connectivity test passed")
            return True
        except BinanceClientError as e:
            logger.error(f"✗ API connectivity test failed: {e}")
            raise
    
    def get_exchange_info(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get exchange trading rules and symbol information.
        
        Args:
            symbol: Optional symbol to filter
            
        Returns:
            Exchange information
        """
        params = {}
        if symbol:
            params["symbol"] = symbol
        
        return self._make_request("GET", "/fapi/v1/exchangeInfo", params)
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information including balances.
        
        Returns:
            Account information
        """
        logger.info("Fetching account information...")
        return self._make_request("GET", "/fapi/v2/account", signed=True)
    
    def get_symbol_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get current price for a symbol.
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Price information
        """
        return self._make_request("GET", "/fapi/v1/ticker/price", {"symbol": symbol})
    
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        time_in_force: str = "GTC"
    ) -> Dict[str, Any]:
        """
        Place an order on Binance Futures.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            side: Order side (BUY or SELL)
            order_type: Order type (MARKET or LIMIT)
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
            time_in_force: Time in force (default: GTC)
            
        Returns:
            Order response data
            
        Raises:
            BinanceClientError: If order placement fails
        """
        logger.info(f"Placing {order_type} {side} order for {quantity} {symbol}")
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }
        
        # Add price for LIMIT orders
        if order_type == "LIMIT":
            if price is None:
                raise BinanceClientError("Price is required for LIMIT orders")
            params["price"] = price
            params["timeInForce"] = time_in_force
        
        return self._make_request("POST", "/fapi/v1/order", params, signed=True)
    
    def get_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Get order information.
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID
            
        Returns:
            Order information
        """
        params = {
            "symbol": symbol,
            "orderId": order_id
        }
        
        return self._make_request("GET", "/fapi/v1/order", params, signed=True)
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Cancel an open order.
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID to cancel
            
        Returns:
            Cancellation response
        """
        logger.info(f"Cancelling order {order_id} for {symbol}")
        
        params = {
            "symbol": symbol,
            "orderId": order_id
        }
        
        return self._make_request("DELETE", "/fapi/v1/order", params, signed=True)
    
    def get_open_orders(self, symbol: Optional[str] = None) -> list:
        """
        Get all open orders.
        
        Args:
            symbol: Optional symbol filter
            
        Returns:
            List of open orders
        """
        params = {}
        if symbol:
            params["symbol"] = symbol
        
        return self._make_request("GET", "/fapi/v1/openOrders", params, signed=True)