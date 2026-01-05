import os
import json
from dotenv import load_dotenv
from typing import Dict, Any, Optional, Tuple
from google import genai
from google.genai import types  # FIXED: Correct import

from mcp_tools import call_tool

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing in .env")

# Create Google Gen AI client (Gemini Developer API)
client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"

SYSTEM_PROMPT = (
    "You are a local automation agent. You have access to tools via JSON actions."
    "Follow this loop: Think -> Decide a single tool action -> Return JSON -> Wait for observation -> Continue."
    "When the goal is completed, return a final message with \"finish\": true."  # FIXED: Escaped inner quotes
    "CRITICAL RULES:"
    "- Prefer Python tools over shell. Use list_files/read_file/write_file before run_command."
    "- When listing the current directory, call list_files with {\"path\": \".\"}."
    "- When writing files, use relative paths (e.g., \"summary.txt\")."
    "- Keep outputs short and strictly JSON."
    "Tools available:"
    "- list_files(path: string) -> lists directory entries"
    "- read_file(path: string) -> reads a text file"
    "- write_file(path: string, content: string) -> writes text content"
    "- run_command(cmd: string) -> runs a restricted shell command (safe-listed)"
    "Output format strictly JSON, one of:"
    "1) {\"thought\": \"...\", \"tool\": \"tool_name\", \"args\": {...}"
    "2) {\"thought\": \"...\", \"finish\": true, \"result\": \"...\"}"
)

def model_decide(goal: str, observation: Optional[str]) -> Dict[str, Any]:
    contents = [
        types.Part(text=f"CWD: {os.getcwd()}"),  # FIXED: Use keyword argument
        types.Part(text=f"GOAL: {goal}"),
    ]
    if observation:
        contents.append(types.Part(text=f"OBSERVATION: {observation}"))

    resp = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0,
            response_mime_type="application/json",
        ),
    )
    text = (resp.text or "").strip()

    try:
        return json.loads(text)
    except Exception:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            candidate = text[start:end+1]
            try:
                return json.loads(candidate)
            except Exception:
                pass
        return {"thought": "Model returned non-JSON. Requesting strict JSON.", "tool": None, "args": {}}
    
def agent_loop(goal: str, max_steps: int = 8) -> Tuple[bool, str]:
    observation = "Use list_files with path '.' for directory listing."
    for step in range(1, max_steps + 1):
        plan = model_decide(goal, observation)
        thought = plan.get("thought", "")
        finish = plan.get("finish", False)
        result = plan.get("result")

        if finish:
            return True, result or "Finished."

        tool_name = plan.get("tool")
        args = plan.get("args", {})

        if not tool_name:
            observation = f"Step {step}: No tool chosen. Thought: {thought}"
            continue

        if tool_name == "list_files" and not args.get("path"):
            args["path"] = "."
        if tool_name == "write_file" and not args.get("path"):
            args["path"] = "summary.txt"

        tool_resp = call_tool(tool_name, args)
        if tool_resp.get("ok"):
            data = tool_resp.get("data")
            obs_str = json.dumps(data, ensure_ascii=False)
            if len(obs_str) > 4000:
                obs_str = obs_str[:4000] + "...(truncated)"
            observation = f"Tool {tool_name} success. Data: {obs_str}"
        else:
            observation = f"Tool {tool_name} error: {tool_resp.get('error')}"

    return False, f"Max steps reached. Last observation: {observation}"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gemini MCP-style local agent (Gemini 2.5)")
    parser.add_argument("--goal", type=str, required=True,
                        help="Describe what you want the agent to do.")
    args = parser.parse_args()

    ok, msg = agent_loop(args.goal, max_steps=8)
    print("=== AGENT RESULT ===")
    print(msg)