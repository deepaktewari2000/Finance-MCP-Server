import requests
name = "forex.rate"
description = "Get exchange rate between two currencies. args: {'base':'USD','symbols':'INR'}"
schema = {"base":{"type":"string"}, "symbols":{"type":"string"}}

def run(args: dict):
    base = args.get("base","USD")
    symbols = args.get("symbols","USD")
    url = f"https://api.exchangerate.host/latest?base={base}&symbols={symbols}"
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        raise ValueError(f"Exchange API error: {r.status_code}")
    data = r.json()
    rates = data.get('rates',{})
    return {"base": base, "rates": rates}
