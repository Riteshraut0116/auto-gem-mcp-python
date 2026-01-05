import os
import json
import subprocess
from typing import Dict, Any, List, Optional

# Simple tool registry
TOOLS: Dict[str, Any] = {}

def tool(name: str):
    def decorator(fn):
        TOOLS[name] = fn
        return fn
    return decorator

@tool("list_files")
def list_files(args: Dict[str, Any]) -> Dict[str, Any]:
    """List files in a directory."""
    directory = args.get("path", ".")
    try:
        entries = os.listdir(directory)
        return {"ok": True, "data": entries}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@tool("read_file")
def read_file(args: Dict[str, Any]) -> Dict[str, Any]:
    """Read a text file (UTF-8)."""
    path = args.get("path")
    if not path:
        return {"ok": False, "error": "Missing 'path'."}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return {"ok": True, "data": f.read()}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@tool("write_file")
def write_file(args: Dict[str, Any]) -> Dict[str, Any]:
    """Write text to a file."""
    path = args.get("path")
    content = args.get("content", "")
    if not path:
        return {"ok": False, "error": "Missing 'path'."}
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"ok": True, "data": f"Wrote {len(content)} chars to {path}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@tool("run_command")
def run_command(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run a restricted shell command for safety.
    You can configure SAFE_COMMANDS via environment.
    """
    cmd = args.get("cmd")
    if not cmd:
        return {"ok": False, "error": "Missing 'cmd'."}

    safe = os.getenv("SAFE_COMMANDS", "")
    safe_list = [c.strip() for c in safe.split(",") if c.strip()]
    program = cmd.split()[0]

    if safe_list and program not in safe_list:
        return {"ok": False, "error": f"Command '{program}' not in SAFE_COMMANDS: {safe_list}"}

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
        return {
            "ok": True,
            "data": {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

def call_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    fn = TOOLS.get(tool_name)
    if not fn:
        return {"ok": False, "error": f"Unknown tool '{tool_name}'."}
    return fn(args)