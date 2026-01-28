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
║     Binance Futures Testnet Trading Bot v1.0.0           ║
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

The code is split up so each file has one job. Makes it easier to understand and modify.

## Logs - Your New Best Friend

Every time you run a command, the bot creates detailed logs. You can find them in the `logs/` folder.

**To see what happened:**

Windows:
```bash
type logs\trading_bot_*.log
```

Mac/Linux:
```bash
cat logs/trading_bot_*.log
```

The logs show you everything - when the bot connected, what order it tried to place, what response it got back, any errors that happened, etc.

## When Things Go Wrong

Don't worry, I've been there! Here are the most common issues and how to fix them:

### "Missing API credentials"

**What happened**: The bot can't find your API keys.

**How to fix it**: 
- Make sure you created the `.env` file
- Check that you actually pasted your keys in there
- Make sure there are no extra spaces

### "Invalid API key"

**What happened**: Your API keys aren't working.

**How to fix it**:
- Go back to the testnet and generate new keys
- Update your `.env` file with the new ones
- Make sure you copied them correctly (no missing characters)

### "Symbol not valid"

**What happened**: You typed the symbol wrong.

**How to fix it**:
- Use the full symbol like `BTCUSDT` (not just `BTC`)
- Make sure it's all uppercase
- Check that it's a valid symbol on Binance Futures

### "Insufficient balance"

**What happened**: You don't have enough testnet USDT.

**How to fix it**:
- Request more funds from the testnet (they're free!)
- Try a smaller quantity

### "Request timed out"

**What happened**: Your internet hiccuped or Binance's servers are slow.

**How to fix it**:
- Check your internet connection
- Wait a few seconds and try again
- Make sure https://testnet.binancefuture.com is accessible

### Module errors or "No module named..."

**What happened**: The packages aren't installed right.

**How to fix it**:
- Make sure your virtual environment is activated (you should see `(venv)` in your prompt)
- Run `pip install -r requirements.txt` again

## Popular Trading Symbols

Here are some symbols you can try on the testnet:

- **BTCUSDT** - Bitcoin
- **ETHUSDT** - Ethereum  
- **BNBUSDT** - Binance Coin
- **ADAUSDT** - Cardano
- **DOGEUSDT** - Dogecoin
- **SOLUSDT** - Solana

## Safety Stuff

A few things to keep in mind:

✅ **This is testnet only** - You're using fake money, so it's completely safe to experiment  
✅ **Your API keys are safe** - They're stored in `.env` which git ignores  
✅ **No real money** - Can't stress this enough. Testnet = practice mode  
⚠️ **Don't share your keys** - Even testnet keys should stay private  

## How It Works Under the Hood

When you run a command:

1. The CLI checks your inputs to make sure they're valid
2. It loads your API keys from the `.env` file
3. Connects to Binance's testnet
4. Places your order
5. Shows you the results
6. Saves everything to a log file

Each layer (CLI, validation, order logic, API client) is separated so the code is clean and easy to follow.

## What I Built This With

- **Python 3.8+** - The programming language
- **python-binance** - Makes it easy to talk to Binance's API
- **python-dotenv** - Loads environment variables from `.env`
- **requests** - Handles HTTP requests
- **argparse** - Processes command-line arguments

## A Few Notes

- The bot uses Binance Futures Testnet at `https://testnet.binancefuture.com`
- All orders are signed using HMAC SHA256 for security
- Logs are created daily with timestamps
- The code includes type hints to make it easier to understand
- Error messages try to be helpful and tell you what went wrong

## Testing Your Setup

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

Let me explain what each file does:

**bot/client.py**: This is where all the Binance API magic happens. It signs requests, sends them to Binance, and handles responses.

**bot/orders.py**: This manages the business logic for orders. It uses the client to actually place orders but adds validation and error handling.

**bot/validators.py**: Before sending anything to Binance, this checks if your inputs make sense. Saves you from embarrassing typos!

**bot/logging_config.py**: Sets up logging so you can see what's happening and debug issues later.

**cli.py**: This is what you interact with. It takes your command-line arguments and orchestrates everything else.

## What's Logged

The bot logs:
- When it starts up
- Connection attempts to Binance
- Every order you place
- Responses from Binance  
- Any errors that occur
- Validation results

All with timestamps so you can see exactly what happened when.

## Final Thoughts

This bot is meant to be a learning tool and portfolio piece. It demonstrates:
- Clean code organization
- Proper error handling
- User-friendly CLI design
- Comprehensive logging
- Security best practices

Feel free to modify it, break it, improve it - that's how we learn!

## Questions?

If something's not working or you're confused about anything:

1. Check the logs in the `logs/` folder
2. Make sure your `.env` file is set up correctly
3. Verify you're using the testnet (not real Binance)
4. Try the troubleshooting section above

## Disclaimer

**Important**: This is for educational purposes only. It's built for the Binance Futures **Testnet** where you trade with fake money. 

- ✅ Perfect for learning
- ✅ Great for testing strategies
- ✅ Zero financial risk
- ❌ Not financial advice
- ❌ Don't use with real money without proper modifications

Trade responsibly!

---

**Assignment Submission Info**

This project was created for the Python Developer Intern position at Anything.ai

**Contact**:
- saami@anything.ai
- chetan@anything.ai
- CC: sonika@anything.ai

---

**Built with ❤️ and Python**

Version 1.0.0 | January 2025

---

## Quick Checklist Before Submitting

- [ ] Tested with at least one market order ✓
- [ ] Tested with at least one limit order ✓
- [ ] Log files generated ✓
- [ ] No API keys in the code ✓
- [ ] README is clear and helpful ✓
- [ ] Code is on GitHub ✓

If all boxes are checked, you're ready to go! Good luck! 🍀