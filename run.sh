#!/usr/bin/env bash
export MCP_API_KEY=${MCP_API_KEY:-secret123}
uvicorn src.main:app --reload --port 8000
