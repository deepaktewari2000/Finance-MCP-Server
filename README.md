# Finance & Markets MCP Server (Python)

A scaffold for a **Finance & Markets** MCP server implemented in **Python** with FastAPI.
This project exposes modular "tools" that an LLM can call to fetch market data, crypto prices,
exchange rates, historical prices, and compute portfolio values.

## Features included
- FastAPI-based MCP server with API-key auth
- Dynamic tool loading from `src/tools/`
- Tools included:
  - `stock.quote` — latest stock quote (uses `yfinance`)
  - `stock.history` — historical OHLCV data for a ticker
  - `crypto.price` — current crypto price (CoinGecko public API)
  - `forex.rate` — exchange rate via exchangerate.host public API
  - `portfolio.value` — compute portfolio market value given holdings
- Example client to call the MCP server
- `run.sh` to start the server locally

## Quickstart
1. Create virtualenv and install:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # or .\.venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Start server:
   ```bash
   export MCP_API_KEY=secret123
   ./run.sh
   ./run.bat
   ```
3. Examples:
   ```bash
   python example_client.py --api-key secret123 --tool list_tools
   python example_client.py --api-key secret123 --tool stock.quote --args '{"ticker":"AAPL"}'
   python example_client.py --api-key secret123 --tool crypto.price --args '{"id":"bitcoin"}'
   ```

## Testing

### Running Tests
After starting the server, you can test all tools using the example client:

```bash
# 1. Health check (Windows - use .venv\Scripts\python.exe, Linux/Mac - use .venv/bin/python)
.venv\Scripts\python.exe -c "import requests; r = requests.get('http://localhost:8000/health'); print(r.status_code, r.json())"

# 2. List all available tools
python example_client.py --api-key secret123 --tool list_tools

# 3. Test stock quote
python example_client.py --api-key secret123 --tool stock.quote --args '{"ticker":"AAPL"}'

# 4. Test historical stock data
python example_client.py --api-key secret123 --tool stock.history --args '{"ticker":"MSFT","period":"5d"}'

# 5. Test crypto price
python example_client.py --api-key secret123 --tool crypto.price --args '{"id":"bitcoin"}'

# 6. Test forex rates
python example_client.py --api-key secret123 --tool forex.rate --args '{"base":"USD","symbols":"EUR"}'

# 7. Test portfolio value
python example_client.py --api-key secret123 --tool portfolio.value --args '{"holdings":[{"type":"stock","symbol":"AAPL","qty":10},{"type":"crypto","symbol":"bitcoin","qty":0.5}]}'
```

### Expected Results
All commands should return status `200` with JSON responses containing:
- **stock.quote**: Current price, market cap, daily high/low
- **stock.history**: Array of OHLCV data for specified period
- **crypto.price**: Current price, market cap, 24h change
- **forex.rate**: Exchange rates between currencies
- **portfolio.value**: Total portfolio value with breakdown per holding

## Notes & Security
- `yfinance` fetches data from Yahoo Finance (no API key), CoinGecko is public, and exchangerate.host is a free public rates API.
- For production, add rate limiting, caching, and restrict which external APIs are allowed.
- Tools should validate inputs carefully before using in queries.
