# Trading Bot — Binance Futures Testnet (USDT-M)

A simplified Python trading bot that places **Market** and **Limit** orders on the [Binance Futures Testnet](https://testnet.binancefuture.com) via direct REST calls (HMAC-SHA256 signed), with a clean CLI interface, structured logging, and proper error handling.

---

## Project Structure

```
trade-bot/
  bot/
    __init__.py          # Package init
    client.py            # Binance Futures REST client (signing, requests)
    orders.py            # Order placement logic and result formatting
    validators.py        # Input validation
    logging_config.py    # Logging configuration (file + console)
  cli.py                 # CLI entry point (Typer)
  requirements.txt       # Python dependencies
  .env.example           # Example environment variables
  README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/deepakumaraiya200-art/trade-bot.git
cd trade-bot
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure credentials

Copy `.env.example` to `.env` and fill in your Binance Futures **Testnet** API key and secret:

```bash
cp .env.example .env
```

Edit `.env`:

```
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

> **Note:** Obtain testnet credentials at [https://testnet.binancefuture.com](https://testnet.binancefuture.com) (register/login and generate API keys).

---

## Usage

Run the CLI via:

```bash
python cli.py order [OPTIONS]
```

### Options

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--symbol` | `-s` | Yes | Trading pair (e.g. `BTCUSDT`) |
| `--side` | | Yes | `BUY` or `SELL` |
| `--type` | `-t` | Yes | `MARKET` or `LIMIT` |
| `--quantity` | `-q` | Yes | Order quantity |
| `--price` | `-p` | For LIMIT | Limit price |

### Examples

**Place a MARKET BUY order:**

```bash
python cli.py order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Place a LIMIT SELL order:**

```bash
python cli.py order -s BTCUSDT --side SELL -t LIMIT -q 0.001 -p 50000
```

**View help:**

```bash
python cli.py order --help
```

---

## Logging

Logs are written to the `logs/` directory (created automatically). Each run creates a timestamped file, e.g. `logs/trading_bot_20240101_120000.log`. The file contains `DEBUG`-level detail (including full API request/response bodies); the console shows `INFO` and above.

---

## Assumptions

- Only **Binance Futures Testnet (USDT-M)** is supported (`https://testnet.binancefuture.com`).
- Symbols must be alphabetic strings (e.g., `BTCUSDT`). Numeric or special characters are rejected.
- For `LIMIT` orders, `--price` is mandatory and must be positive.
- `timeInForce` defaults to `GTC` (Good Till Cancelled) for LIMIT orders.
- Credentials are loaded from a `.env` file in the working directory.
