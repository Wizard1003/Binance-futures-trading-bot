"""
Order placement and management logic.

Handles order creation with validation and error handling.
"""

import logging
from typing import Optional, Dict, Any

from bot.client import BinanceFuturesClient, BinanceClientError
from bot.validators import validate_order_params, ValidationError
from bot.logging_config import log_order_summary


logger = logging.getLogger("trading_bot.orders")


class OrderManager:
    """
    Manages order placement and tracking.
    
    Attributes:
        client: BinanceFuturesClient instance
    """
    
    def __init__(self, client: BinanceFuturesClient):
        """
        Initialize OrderManager.
        
        Args:
            client: Configured BinanceFuturesClient
        """
        self.client = client
        logger.info("OrderManager initialized")
    
    def place_market_order(
        self,
        symbol: str,
        side: str,
        quantity: float
    ) -> Dict[str, Any]:
        """
        Place a market order.
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY/SELL)
            quantity: Order quantity
            
        Returns:
            Order response
            
        Raises:
            ValidationError: If validation fails
            BinanceClientError: If API request fails
        """
        logger.info(f"Placing MARKET order: {side} {quantity} {symbol}")
        
        # Validate parameters
        try:
            params = validate_order_params(
                symbol=symbol,
                side=side,
                order_type="MARKET",
                quantity=quantity
            )
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        
        # Place order
        try:
            response = self.client.place_order(
                symbol=params["symbol"],
                side=params["side"],
                order_type=params["type"],
                quantity=params["quantity"]
            )
            
            # Log success
            log_order_summary(logger, params, response)
            logger.info(f"✓ Market order placed successfully. Order ID: {response.get('orderId')}")
            
            return response
            
        except BinanceClientError as e:
            logger.error(f"Failed to place market order: {e}")
            raise
    
    def place_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        time_in_force: str = "GTC"
    ) -> Dict[str, Any]:
        """
        Place a limit order.
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY/SELL)
            quantity: Order quantity
            price: Limit price
            time_in_force: Time in force (default: GTC)
            
        Returns:
            Order response
            
        Raises:
            ValidationError: If validation fails
            BinanceClientError: If API request fails
        """
        logger.info(f"Placing LIMIT order: {side} {quantity} {symbol} @ {price}")
        
        # Validate parameters
        try:
            params = validate_order_params(
                symbol=symbol,
                side=side,
                order_type="LIMIT",
                quantity=quantity,
                price=price
            )
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        
        # Place order
        try:
            response = self.client.place_order(
                symbol=params["symbol"],
                side=params["side"],
                order_type=params["type"],
                quantity=params["quantity"],
                price=params["price"],
                time_in_force=time_in_force
            )
            
            # Log success
            log_order_summary(logger, params, response)
            logger.info(f"✓ Limit order placed successfully. Order ID: {response.get('orderId')}")
            
            return response
            
        except BinanceClientError as e:
            logger.error(f"Failed to place limit order: {e}")
            raise
    
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Place an order (automatically routes to market or limit).
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY/SELL)
            order_type: Order type (MARKET/LIMIT)
            quantity: Order quantity
            price: Limit price (required for LIMIT orders)
            
        Returns:
            Order response
            
        Raises:
            ValidationError: If validation fails
            BinanceClientError: If API request fails
        """
        order_type = order_type.upper()
        
        if order_type == "MARKET":
            return self.place_market_order(symbol, side, quantity)
        elif order_type == "LIMIT":
            if price is None:
                raise ValidationError("Price is required for LIMIT orders")
            return self.place_limit_order(symbol, side, quantity, price)
        else:
            raise ValidationError(f"Unsupported order type: {order_type}")
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Get the status of an order.
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID
            
        Returns:
            Order status information
        """
        logger.info(f"Fetching status for order {order_id}")
        
        try:
            order = self.client.get_order(symbol, order_id)
            logger.info(f"Order {order_id} status: {order.get('status')}")
            return order
        except BinanceClientError as e:
            logger.error(f"Failed to fetch order status: {e}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Cancel an order.
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID to cancel
            
        Returns:
            Cancellation response
        """
        logger.info(f"Cancelling order {order_id}")
        
        try:
            response = self.client.cancel_order(symbol, order_id)
            logger.info(f"✓ Order {order_id} cancelled successfully")
            return response
        except BinanceClientError as e:
            logger.error(f"Failed to cancel order: {e}")
            raise
    
    def get_open_orders(self, symbol: Optional[str] = None) -> list:
        """
        Get all open orders.
        
        Args:
            symbol: Optional symbol filter
            
        Returns:
            List of open orders
        """
        try:
            orders = self.client.get_open_orders(symbol)
            logger.info(f"Found {len(orders)} open orders")
            return orders
        except BinanceClientError as e:
            logger.error(f"Failed to fetch open orders: {e}")
            raise
    
    def get_account_balance(self) -> Dict[str, Any]:
        """
        Get account balance information.
        
        Returns:
            Account balance data
        """
        try:
            account_info = self.client.get_account_info()
            logger.info("Account balance fetched successfully")
            return account_info
        except BinanceClientError as e:
            logger.error(f"Failed to fetch account balance: {e}")
            raise
    
    def verify_symbol(self, symbol: str) -> bool:
        """
        Verify if a symbol is valid and tradeable.
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            True if symbol is valid
        """
        try:
            exchange_info = self.client.get_exchange_info(symbol)
            symbols = exchange_info.get("symbols", [])
            
            for sym in symbols:
                if sym.get("symbol") == symbol and sym.get("status") == "TRADING":
                    logger.info(f"Symbol {symbol} is valid and tradeable")
                    return True
            
            logger.warning(f"Symbol {symbol} is not valid or not tradeable")
            return False
            
        except BinanceClientError as e:
            logger.error(f"Failed to verify symbol: {e}")
            return False