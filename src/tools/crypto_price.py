import requests
name = "crypto.price"
description = "Get current crypto price from CoinGecko. args: {'id':'bitcoin', 'vs_currency':'usd'}"
schema = {"id":{"type":"string"}, "vs_currency":{"type":"string", "optional":True}}

def run(args: dict):
    cid = args.get("id")
    if not cid:
        raise ValueError("missing 'id' (CoinGecko coin id)")
    vs = args.get("vs_currency","usd")
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={cid}&vs_currencies={vs}&include_market_cap=true&include_24hr_change=true"
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        raise ValueError(f"CoinGecko API error: {r.status_code}")
    data = r.json().get(cid)
    if not data:
        raise ValueError("coin not found")
    return {
        "id": cid,
        "vs_currency": vs,
        "price": data.get(vs),
        "market_cap": data.get(f"{vs}_market_cap"),
        "24h_change": data.get(f"{vs}_24h_change")
    }
