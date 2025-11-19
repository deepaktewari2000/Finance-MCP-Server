import yfinance as yf
import pandas as pd
name = "stock.history"
description = "Get historical OHLCV data. args: {'ticker':'AAPL', 'period':'1mo', 'interval':'1d'}"
schema = {"ticker":{"type":"string"}, "period":{"type":"string", "optional":True}, "interval":{"type":"string", "optional":True}}

def run(args: dict):
    ticker = args.get("ticker")
    if not ticker:
        raise ValueError("missing 'ticker'")
    period = args.get("period", "1mo")
    interval = args.get("interval", "1d")
    t = yf.Ticker(ticker)
    hist = t.history(period=period, interval=interval)
    if hist.empty:
        return {"rows": []}
    # Convert to serializable format
    rows = []
    for idx, row in hist.iterrows():
        rows.append({
            "date": idx.strftime("%Y-%m-%d %H:%M:%S"),
            "open": None if pd.isna(row['Open']) else float(row['Open']),
            "high": None if pd.isna(row['High']) else float(row['High']),
            "low": None if pd.isna(row['Low']) else float(row['Low']),
            "close": None if pd.isna(row['Close']) else float(row['Close']),
            "volume": None if pd.isna(row['Volume']) else int(row['Volume']),
        })
    return {"rows": rows}
