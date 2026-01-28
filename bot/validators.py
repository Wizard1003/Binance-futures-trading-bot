"""
Input validation module for trading bot.

Validates user inputs before sending to the API.
"""

from typing import Optional
import logging


logger = logging.getLogger("trading_bot.validators")


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_symbol(symbol: str) -> str:
    """
    Validate trading symbol format.
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        
    Returns:
        Uppercase symbol
        
    Raises:
        ValidationError: If symbol format is invalid
    """
    if not symbol:
        raise ValidationError("Symbol cannot be empty")
    
    symbol = symbol.upper().strip()
    
    # Basic format validation
    if len(symbol) < 6:
        raise ValidationError(f"Symbol '{symbol}' is too short (minimum 6 characters)")
    
    if not symbol.isalnum():
        raise ValidationError(f"Symbol '{symbol}' must contain only alphanumeric characters")
    
    logger.debug(f"Symbol validated: {symbol}")
    return symbol


def validate_side(side: str) -> str:
    """
    Validate order side.
    
    Args:
        side: Order side (BUY or SELL)
        
    Returns:
        Uppercase side
        
    Raises:
        ValidationError: If side is invalid
    """
    if not side:
        raise ValidationError("Side cannot be empty")
    
    side = side.upper().strip()
    
    valid_sides = ["BUY", "SELL"]
    if side not in valid_sides:
        raise ValidationError(f"Side must be one of {valid_sides}, got '{side}'")
    
    logger.debug(f"Side validated: {side}")
    return side


def validate_order_type(order_type: str) -> str:
    """
    Validate order type.
    
    Args:
        order_type: Order type (MARKET or LIMIT)
        
    Returns:
        Uppercase order type
        
    Raises:
        ValidationError: If order type is invalid
    """
    if not order_type:
        raise ValidationError("Order type cannot be empty")
    
    order_type = order_type.upper().strip()
    
    valid_types = ["MARKET", "LIMIT"]
    if order_type not in valid_types:
        raise ValidationError(f"Order type must be one of {valid_types}, got '{order_type}'")
    
    logger.debug(f"Order type validated: {order_type}")
    return order_type


def validate_quantity(quantity: float) -> float:
    """
    Validate order quantity.
    
    Args:
        quantity: Order quantity
        
    Returns:
        Validated quantity
        
    Raises:
        ValidationError: If quantity is invalid
    """
    if quantity is None:
        raise ValidationError("Quantity cannot be empty")
    
    try:
        quantity = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError(f"Quantity must be a number, got '{quantity}'")
    
    if quantity <= 0:
        raise ValidationError(f"Quantity must be greater than 0, got {quantity}")
    
    logger.debug(f"Quantity validated: {quantity}")
    return quantity


def validate_price(price: Optional[float], order_type: str) -> Optional[float]:
    """
    Validate order price.
    
    Args:
        price: Order price (required for LIMIT orders)
        order_type: Order type
        
    Returns:
        Validated price or None
        
    Raises:
        ValidationError: If price validation fails
    """
    # Price is required for LIMIT orders
    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders")
        
        try:
            price = float(price)
        except (ValueError, TypeError):
            raise ValidationError(f"Price must be a number, got '{price}'")
        
        if price <= 0:
            raise ValidationError(f"Price must be greater than 0, got {price}")
        
        logger.debug(f"Price validated: {price}")
        return price
    
    # Price should not be provided for MARKET orders
    if order_type == "MARKET" and price is not None:
        logger.warning("Price provided for MARKET order will be ignored")
        return None
    
    return price


def validate_order_params(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None
) -> dict:
    """
    Validate all order parameters at once.
    
    Args:
        symbol: Trading pair symbol
        side: Order side (BUY/SELL)
        order_type: Order type (MARKET/LIMIT)
        quantity: Order quantity
        price: Order price (optional)
        
    Returns:
        Dictionary of validated parameters
        
    Raises:
        ValidationError: If any validation fails
    """
    logger.info("Validating order parameters...")
    
    validated = {
        "symbol": validate_symbol(symbol),
        "side": validate_side(side),
        "type": validate_order_type(order_type),
        "quantity": validate_quantity(quantity),
        "price": validate_price(price, validate_order_type(order_type))
    }
    
    # Remove None values
    validated = {k: v for k, v in validated.items() if v is not None}
    
    logger.info("All parameters validated successfully")
    return validated