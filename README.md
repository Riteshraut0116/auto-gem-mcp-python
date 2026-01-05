
**## 🤖 AutoGem MCP**

A lightweight, local **agentic automation framework** powered by **Gemini API (free key)**, **Python**, and an **MCP-style tool interface**. It uses a **ReAct loop** (Think → Act → Observe → Repeat) to plan actions, execute local tools, and complete tasks autonomously.
<BLOCKQUOTE><P>Perfect for quick local workflows, coding helpers, and file automation. Runs entirely on your machine with no external dependencies beyond Gemini.</P></BLOCKQUOTE>

---

## ✨ Features

- **Agentic Automation:** Implements ReAct-style reasoning for iterative task execution.
- **Gemini Integration:** Uses Google’s Gemini model (`gemini-2.5-flash` by default) for intelligent decision-making.
- **MCP-Style Tools:** Includes local tools for:

    - Listing files 📂

    - Reading files 📖

    - Writing files ✍️

    - Running safe shell commands ⚙️
- **Environment Config:** `.env` for API keys and safe command restrictions.
- **Extensible Design:** Add custom tools easily using decorators.
- **Cross-Platform:** Works on Windows, macOS, and Linux.

---

## 🎯 Final Output

When you run the agent with a goal, you’ll see:

✅ A structured JSON-based reasoning loop.

📂 Automatic file operations (list, read, write).

⚡ Safe command execution with restrictions.

📜 A summary or result printed after task completion.

---

## 🛠️ Tech Stack

- **Python 3.10+**

- **Google Gen AI SDK (`google-genai`)**

- **dotenv:** For environment variable management.

- **Pydantic:** For optional schema validation.

---

## 🚀 Getting Started

# 1. Clone the Repository

# 2.  Create Virtual Environment & Install Dependencies

1. python -m venv .venv
2. source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
3. pip install -r requirements.txt


2) Create README
# 3.  Configure Environment
1. Create a .env file:

---

## 📂 File Structure

auto-gem-mcp-python/
│
├── .env                  # Gemini API key and safe commands
├── .gitignore            # Ignore venv, cache, etc.
├── agent.py              # Core agent logic (ReAct loop)
├── mcp_tools.py          # MCP-style local tools
├── requirements.txt      # Dependencies
└── README.md             # Project documentation

---

## 🏃 Usage Examples

# 1) List Files and Summarize
1. python agent.py --goal "List files in the current directory and write a summary into summary.txt."

# 2) Create README
1. python agent.py --goal "Create a file named README.md with a short project description."

# 3) Safe Shell Command
1. Python agent.py --goal "Run 'echo Hello Pune' and save the output to hello.txt."

---

## 🛡️ Safety & Best Practices

# Restrict shell commands via SAFE_COMMANDS in .env.
# Use relative paths for file operations.
# Limit steps in agent.py to prevent infinite loops.
# Validate tool calls for security.

---


## 🔧 Extending Tools

# Add new tools in mcp_tools.py:

@tool("append_file")
def append_file(args: Dict[str, Any]) -> Dict[str, Any]:
    path = args.get("path")
    content = args.get("content", "")
    if not path:
        return {"ok": False, "error": "Missing 'path'."}
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        return {"ok": True, "data": f"Appended {len(content)} chars to {path}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

---

## 🗺️ Roadmap

- Add Git integration tools.
- Implement Markdown parsing for docs automation.
- Add schema validation with Pydantic.
- CI/CD pipeline for automated testing.

---

## 👤 Author

**Ritesh Raut**  
*Programmer Analyst, Cognizant*

🚀 "Automate smarter, faster, safer with Gemini-powered local tools!" ⚡🤖📂

---

### 🌐 Connect with me:
<p align="left">
<a href="https://github.com/Riteshraut0116" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/github.svg" alt="Riteshraut0116" height="30" width="40" /></a>
<a href="https://linkedin.com/in/ritesh-raut-9aa4b71ba" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="ritesh-raut-9aa4b71ba" height="30" width="40" /></a>
<a href="https://www.instagram.com/riteshraut1601/" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="riteshraut1601" height="30" width="40" /></a>
<a href="https://www.facebook.com/ritesh.raut.649321/" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/facebook.svg" alt="ritesh.raut.649321" height="30" width="40" /></a>
</p>

---





