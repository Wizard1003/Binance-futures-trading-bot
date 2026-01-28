# Binance Futures Trading Bot 🚀

Hey there! Welcome to my trading bot project. This is a Python bot I built for the Binance Futures Testnet that can place market and limit orders. It's got solid error handling, logs everything important, and is pretty straightforward to use.

## What Does It Do?

This bot connects to Binance Futures Testnet (the practice environment where you use fake money) and lets you:

- Place **market orders** (buy/sell instantly at current price)
- Place **limit orders** (buy/sell at a specific price you choose)
- See exactly what's happening with detailed logs
- Handle errors gracefully without crashing

## What You'll Need

- **Python 3.8 or newer** - Check by running `python --version` in your terminal
- **Internet connection** - The bot needs to talk to Binance's servers
- **A Binance Futures Testnet account** - Don't worry, it's free and uses fake money!

### Getting Your Testnet Account

1. Go to https://testnet.binancefuture.com
2. Click "Login with GitHub" or "Login with Google" 
3. Once you're in, find the API Management section
4. Generate a new API Key and Secret
5. **Important**: Copy both right away! You won't be able to see the secret again

The testnet gives you fake USDT to practice with, so there's zero risk.

## Getting Started

Let me walk you through setting this up. It'll take about 5 minutes.

### Step 1: Get the Code

If you're cloning from GitHub:
```bash
git clone <your-repo-url>
cd trading_bot
```

Or if you downloaded a zip file, just extract it and open the folder in your terminal.

### Step 2: Set Up Python Environment

We'll create a virtual environment to keep things clean:

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You'll see `(venv)` appear at the start of your command line when it's activated.

### Step 3: Install What We Need

Just run this to install all required libraries or packages:
```bash
pip install -r requirements.txt
```

### Step 4: Add Your API Keys

1. First, copy the example file:
```bash
copy .env.example .env    # Windows
cp .env.example .env      # Mac/Linux
```

2. Open the new `.env` file in any text editor and add your keys:
```
BINANCE_API_KEY=paste_your_key_here
BINANCE_API_SECRET=paste_your_secret_here
```

**Pro tip**: Don't share this file with anyone! It's already set up to be ignored by git.

### Step 5: Try It Out!

Let's place your first order. Start with something small:
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

If everything's set up correctly, you'll see something like:
```
╔═══════════════════════════════════════════════════════════╗
║     Binance Futures Testnet Trading Bot v1.0.0            ║
║     Professional Trading Bot for Educational Use          ║
╚═══════════════════════════════════════════════════════════╝

ℹ Validating environment...
✓ Environment validated

ℹ Initializing Binance Futures client...
✓ Connected to Binance Futures Testnet

ℹ Placing order...
✓ Order placed successfully!

============================================================
ORDER RESPONSE
============================================================
Order ID:         12345678
Status:           FILLED
Symbol:           BTCUSDT
Side:             BUY
Quantity:         0.001
...
```

Congrats! You just placed your first order on the testnet! 🎉

## How to Use It

### Basic Command

The general format is:
```bash
python cli.py --symbol <SYMBOL> --side <BUY|SELL> --type <MARKET|LIMIT> --quantity <AMOUNT> [--price <PRICE>]
```

Let me break down what each part means:

- `--symbol`: What you want to trade (like BTCUSDT for Bitcoin, ETHUSDT for Ethereum)
- `--side`: Whether you're buying (BUY) or selling (SELL)
- `--type`: MARKET (execute right now) or LIMIT (at a specific price)
- `--quantity`: How much you want to trade
- `--price`: Only needed for limit orders - the price you want

### Real Examples

**Buy some Bitcoin right now:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Sell Ethereum when it hits $3000:**
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3000
```

**Buy Bitcoin at a specific price:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 40000
```

**Want to see more detailed logs?**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --verbose
```

**Need help?**
```bash
python cli.py --help
```

## What's Inside

Here's how I organized the code:
```
trading_bot/
├── bot/                      # The main bot code
│   ├── client.py            # Talks to Binance's API
│   ├── orders.py            # Handles placing orders
│   ├── validators.py        # Checks if your inputs make sense
│   └── logging_config.py    # Sets up logging
├── cli.py                   # The command-line interface you interact with
├── requirements.txt         # List of packages needed
├── .env                     # Your API keys (keep this secret!)
├── .env.example            # Template for the .env file
└── logs/                    # Where all the logs go
```
Here are some symbols you can try on the testnet:

- **BTCUSDT** - Bitcoin
- **ETHUSDT** - Ethereum  
- **BNBUSDT** - Binance Coin
- **ADAUSDT** - Cardano
- **DOGEUSDT** - Dogecoin
- **SOLUSDT** - Solana

Want to make sure everything works? Try these in order:
```bash
# 1. Check if you can connect
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# 2. Try a limit order
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 50000

# 3. Test error handling (this should fail gracefully)
python cli.py --symbol FAKESYMBOL --side BUY --type MARKET --quantity 0.001
```

If all three work (the last one should give you a clear error message), you're all set!

## Project Structure Explained

**bot/client.py**: This is where all the Binance API magic happens. It signs requests, sends them to Binance, and handles responses.

**bot/orders.py**: This manages the business logic for orders. It uses the client to actually place orders but adds validation and error handling.

**bot/validators.py**: Before sending anything to Binance, this checks if your inputs make sense. Saves you from embarrassing typos!

**bot/logging_config.py**: Sets up logging so you can see what's happening and debug issues later.

**cli.py**: This is what you interact with. It takes your command-line arguments and orchestrates everything else.
