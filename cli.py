#!/usr/bin/env python3
"""
Trading Bot CLI - Command Line Interface

Main entry point for the Binance Futures Testnet Trading Bot.
"""

import os
import sys
from typing import Optional
import argparse
from pathlib import Path

from dotenv import load_dotenv

from bot.client import BinanceFuturesClient, BinanceClientError
from bot.orders import OrderManager
from bot.validators import ValidationError
from bot.logging_config import setup_logging


# Load environment variables
load_dotenv()


def print_banner():
    """Print application banner."""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║     Binance Futures Testnet Trading Bot v1.0.0           ║
║     Professional Trading Bot for Educational Use          ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_success(message: str):
    """Print success message."""
    print(f"\n✓ {message}\n")


def print_error(message: str):
    """Print error message."""
    print(f"\n✗ ERROR: {message}\n", file=sys.stderr)


def print_info(message: str):
    """Print info message."""
    print(f"ℹ {message}")


def validate_environment() -> tuple:
    """
    Validate required environment variables.
    
    Returns:
        Tuple of (api_key, api_secret)
        
    Raises:
        SystemExit: If environment variables are missing
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        print_error(
            "Missing API credentials!\n"
            "Please create a .env file with:\n"
            "  BINANCE_API_KEY=your_key\n"
            "  BINANCE_API_SECRET=your_secret\n\n"
            "Get your credentials from: https://testnet.binancefuture.com"
        )
        sys.exit(1)
    
    return api_key, api_secret


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure argument parser.
    
    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Place a market buy order
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  # Place a limit sell order
  python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 45000

  # Place an order with verbose logging
  python cli.py --symbol ETHUSDT --side BUY --type MARKET --quantity 0.01 --verbose

For more information, see README.md
        """
    )
    
    # Required arguments
    parser.add_argument(
        "--symbol",
        type=str,
        required=True,
        help="Trading pair symbol (e.g., BTCUSDT, ETHUSDT)"
    )
    
    parser.add_argument(
        "--side",
        type=str,
        required=True,
        choices=["BUY", "SELL", "buy", "sell"],
        help="Order side: BUY or SELL"
    )
    
    parser.add_argument(
        "--type",
        type=str,
        required=True,
        choices=["MARKET", "LIMIT", "market", "limit"],
        help="Order type: MARKET or LIMIT"
    )
    
    parser.add_argument(
        "--quantity",
        type=float,
        required=True,
        help="Order quantity (amount to buy/sell)"
    )
    
    # Optional arguments
    parser.add_argument(
        "--price",
        type=float,
        required=False,
        help="Limit price (required for LIMIT orders)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging (DEBUG level)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Trading Bot v1.0.0"
    )
    
    return parser


def main():
    """Main entry point for CLI."""
    # Print banner
    print_banner()
    
    # Parse arguments
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    logger = setup_logging(log_level)
    
    try:
        # Validate environment
        print_info("Validating environment...")
        api_key, api_secret = validate_environment()
        print_success("Environment validated")
        
        # Initialize client
        print_info("Initializing Binance Futures client...")
        client = BinanceFuturesClient(
            api_key=api_key,
            api_secret=api_secret,
            testnet=True
        )
        
        # Test connectivity
        print_info("Testing API connectivity...")
        client.test_connectivity()
        print_success("Connected to Binance Futures Testnet")
        
        # Initialize order manager
        order_manager = OrderManager(client)
        
        # Display order details
        print("\n" + "=" * 60)
        print("ORDER DETAILS")
        print("=" * 60)
        print(f"Symbol:       {args.symbol.upper()}")
        print(f"Side:         {args.side.upper()}")
        print(f"Type:         {args.type.upper()}")
        print(f"Quantity:     {args.quantity}")
        if args.price:
            print(f"Price:        {args.price}")
        print("=" * 60 + "\n")
        
        # Verify symbol
        print_info(f"Verifying symbol {args.symbol.upper()}...")
        if not order_manager.verify_symbol(args.symbol.upper()):
            print_error(f"Symbol {args.symbol.upper()} is not valid or not tradeable")
            sys.exit(1)
        print_success(f"Symbol {args.symbol.upper()} verified")
        
        # Place order
        print_info("Placing order...")
        response = order_manager.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )
        
        # Display success message
        print_success("Order placed successfully!")
        
        # Display order response
        print("\n" + "=" * 60)
        print("ORDER RESPONSE")
        print("=" * 60)
        print(f"Order ID:         {response.get('orderId')}")
        print(f"Client Order ID:  {response.get('clientOrderId')}")
        print(f"Status:           {response.get('status')}")
        print(f"Symbol:           {response.get('symbol')}")
        print(f"Side:             {response.get('side')}")
        print(f"Type:             {response.get('type')}")
        print(f"Quantity:         {response.get('origQty')}")
        print(f"Executed Qty:     {response.get('executedQty', 0)}")
        
        if response.get('avgPrice'):
            print(f"Average Price:    {response.get('avgPrice')}")
        
        if response.get('price') and response.get('price') != '0':
            print(f"Limit Price:      {response.get('price')}")
        
        print(f"Time in Force:    {response.get('timeInForce', 'N/A')}")
        print(f"Update Time:      {response.get('updateTime')}")
        print("=" * 60 + "\n")
        
        print_info("Check logs folder for detailed logs")
        
        return 0
        
    except ValidationError as e:
        print_error(f"Validation Error: {e}")
        logger.error(f"Validation failed: {e}")
        return 1
        
    except BinanceClientError as e:
        print_error(f"API Error: {e}")
        logger.error(f"API request failed: {e}")
        return 1
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        logger.info("Operation cancelled by user")
        return 130
        
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        logger.exception("Unexpected error occurred")
        return 1


if __name__ == "__main__":
    sys.exit(main())