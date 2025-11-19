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
   ```
3. Examples:
   ```bash
   python example_client.py --api-key secret123 --tool list_tools
   python example_client.py --api-key secret123 --tool stock.quote --args '{"ticker":"AAPL"}'
   python example_client.py --api-key secret123 --tool crypto.price --args '{"id":"bitcoin"}'
   ```

4. Via Docker:
   docker build -t finance-mcp-server .
   docker run -p 8000:8000 -e MCP_API_KEY=secret123 finance-mcp-server

## Notes & Security
- `yfinance` fetches data from Yahoo Finance (no API key), CoinGecko is public, and exchangerate.host is a free public rates API.
- For production, add rate limiting, caching, and restrict which external APIs are allowed.
- Tools should validate inputs carefully before using in queries.
