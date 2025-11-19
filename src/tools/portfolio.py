import requests
name = "portfolio.value"
description = "Compute portfolio value. args: {'holdings':[{'type':'stock'|'crypto','symbol':str,'qty':float}], 'vs_currency':'usd'}"
schema = {"holdings":{"type":"array"}, "vs_currency":{"type":"string", "optional":True}}

def _get_stock_price(ticker):
    # Use Yahoo Finance via requests to fetch quote page fallback to yfinance is recommended in production
    try:
        import yfinance as yf
        t = yf.Ticker(ticker)
        info = t.info
        return info.get('regularMarketPrice') or info.get('previousClose')
    except Exception:
        return None

def _get_crypto_price(cid, vs='usd'):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={cid}&vs_currencies={vs}"
        r = requests.get(url, timeout=10)
        if r.status_code != 200: return None
        data = r.json().get(cid,{})
        return data.get(vs)
    except Exception:
        return None

def run(args: dict):
    holdings = args.get('holdings', [])
    if not isinstance(holdings, list):
        raise ValueError('holdings must be a list')
    vs = args.get('vs_currency','usd')
    total = 0.0
    details = []
    for h in holdings:
        typ = h.get('type')
        sym = h.get('symbol')
        qty = float(h.get('qty', 0))
        price = None
        if typ == 'stock':
            price = _get_stock_price(sym)
        elif typ == 'crypto':
            price = _get_crypto_price(sym, vs)
        else:
            raise ValueError('unknown holding type, use stock or crypto')
        if price is None:
            details.append({'symbol': sym, 'qty': qty, 'price': None, 'value': None, 'status':'price_not_found'})
        else:
            value = price * qty
            total += value
            details.append({'symbol': sym, 'qty': qty, 'price': price, 'value': value, 'status':'ok'})
    return {'vs_currency': vs, 'total': total, 'details': details}
