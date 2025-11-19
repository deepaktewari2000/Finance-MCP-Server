import requests, json, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--api-key", required=True)
parser.add_argument("--tool", required=True, help="tool name or 'list_tools'")
parser.add_argument("--args", default="{}", help="JSON string of arguments")
parser.add_argument("--server", default="http://localhost:8000")
args = parser.parse_args()

headers = {"x-api-key": args.api_key, "Content-Type":"application/json"}
if args.tool == "list_tools":
    r = requests.get(f"{args.server}/tools", headers=headers)
    print(r.status_code, r.text)
else:
    payload = {"tool": args.tool, "args": json.loads(args.args)}
    r = requests.post(f"{args.server}/invoke", headers=headers, json=payload)
    print(r.status_code)
    try:
        print(json.dumps(r.json(), indent=2))
    except Exception:
        print(r.text)
