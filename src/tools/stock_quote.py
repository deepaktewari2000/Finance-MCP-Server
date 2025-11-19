import yfinance as yf
name = "stock.quote"
description = "Get latest stock quote for a ticker. args: {'ticker': 'AAPL'}"
schema = {"ticker":{"type":"string"}}

def run(args: dict):
    ticker = args.get("ticker")
    if not ticker:
        raise ValueError("missing 'ticker'")
    t = yf.Ticker(ticker)
    info = t.info
    # Try to extract sensible fields (some may be missing)
    return {
        "symbol": ticker.upper(),
        "shortName": info.get("shortName") or info.get("longName"),
        "currentPrice": info.get("regularMarketPrice"),
        "previousClose": info.get("previousClose"),
        "open": info.get("open"),
        "dayHigh": info.get("dayHigh"),
        "dayLow": info.get("dayLow"),
        "marketCap": info.get("marketCap"),
        "currency": info.get("currency"),
    }
