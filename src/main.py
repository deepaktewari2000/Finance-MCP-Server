from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import importlib, pkgutil, os, traceback

API_KEY = os.environ.get("MCP_API_KEY", "secret123")
app = FastAPI(title="Finance & Markets MCP Server")

class InvokeRequest(BaseModel):
    tool: str
    args: dict = {}

TOOLS = {}
def load_tools():
    import src.tools as tools_pkg
    package_path = tools_pkg.__path__
    for finder, name, ispkg in pkgutil.iter_modules(package_path):
        module = importlib.import_module(f"src.tools.{name}")
        if hasattr(module, "name") and hasattr(module, "run"):
            TOOLS[module.name] = {
                "module": module,
                "description": getattr(module, "description", ""),
                "schema": getattr(module, "schema", None)
            }
load_tools()

def check_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/tools")
def list_tools(x_api_key: str = Header(None)):
    check_api_key(x_api_key)
    return [{"name":name, "description": TOOLS[name]['description'], "schema": TOOLS[name]['schema']} for name in TOOLS]

@app.post("/invoke")
def invoke(request: InvokeRequest, x_api_key: str = Header(None)):
    check_api_key(x_api_key)
    if request.tool not in TOOLS:
        raise HTTPException(status_code=404, detail="Tool not found")
    module = TOOLS[request.tool]['module']
    try:
        result = module.run(request.args)
        return {"ok": True, "result": result}
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail={"error": str(e), "trace": tb})
