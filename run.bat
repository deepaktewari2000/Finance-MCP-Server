@echo off
REM Windows batch script to run the Finance MCP server
if "%MCP_API_KEY%"=="" (
    set MCP_API_KEY=secret123
)
echo Starting Finance MCP Server with API Key: %MCP_API_KEY%
.venv\Scripts\python.exe -m uvicorn src.main:app --reload --port 8000
