"""
Logging configuration for the trading bot.

This module sets up structured logging with both file and console handlers.
"""

import logging
import os
from pathlib import Path
from datetime import datetime


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Configure and return a logger with file and console handlers.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)  # Capture all levels, handlers will filter
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    console_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S"
    )
    
    # File handler - detailed logging
    log_file = log_dir / f"trading_bot_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler - less verbose
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Logging initialized. Log file: {log_file}")
    
    return logger


def log_api_request(logger: logging.Logger, method: str, endpoint: str, params: dict = None):
    """
    Log API request details.
    
    Args:
        logger: Logger instance
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint
        params: Request parameters
    """
    logger.debug(f"API Request: {method} {endpoint}")
    if params:
        # Don't log sensitive data
        safe_params = {k: v for k, v in params.items() if k not in ["signature", "apiKey"]}
        logger.debug(f"Request params: {safe_params}")


def log_api_response(logger: logging.Logger, status_code: int, response_data: dict):
    """
    Log API response details.
    
    Args:
        logger: Logger instance
        status_code: HTTP status code
        response_data: Response data
    """
    logger.debug(f"API Response: Status {status_code}")
    logger.debug(f"Response data: {response_data}")


def log_order_summary(logger: logging.Logger, order_params: dict, response: dict):
    """
    Log a formatted order summary.
    
    Args:
        logger: Logger instance
        order_params: Order parameters sent
        response: Order response from API
    """
    logger.info("=" * 60)
    logger.info("ORDER PLACEMENT SUMMARY")
    logger.info("=" * 60)
    
    # Request summary
    logger.info("Request Details:")
    logger.info(f"  Symbol: {order_params.get('symbol')}")
    logger.info(f"  Side: {order_params.get('side')}")
    logger.info(f"  Type: {order_params.get('type')}")
    logger.info(f"  Quantity: {order_params.get('quantity')}")
    if order_params.get('price'):
        logger.info(f"  Price: {order_params.get('price')}")
    
    # Response summary
    logger.info("\nResponse Details:")
    logger.info(f"  Order ID: {response.get('orderId')}")
    logger.info(f"  Status: {response.get('status')}")
    logger.info(f"  Executed Qty: {response.get('executedQty', 0)}")
    
    if response.get('avgPrice'):
        logger.info(f"  Average Price: {response.get('avgPrice')}")
    
    logger.info(f"  Client Order ID: {response.get('clientOrderId')}")
    logger.info(f"  Update Time: {response.get('updateTime')}")
    logger.info("=" * 60)