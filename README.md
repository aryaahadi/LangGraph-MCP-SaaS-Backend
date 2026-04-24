### LangGraph + MCP + SaaS Backend (Python Example Project)

---

## 🚀 Overview

This project demonstrates a **complete, practical integration** of:

- **LangGraph** (agent orchestration & reasoning loops)  
- **MCP (Model Context Protocol)** (tool server abstraction)  
- A **Python backend** (SaaS business logic)  
- A **Claude or GPT function‑calling model**  

Together, the system forms a realistic **AI-powered internal assistant** for a SaaS subscription platform. The assistant can:

- Look up customer accounts  
- Upgrade or downgrade their subscription plan  
- Check seat usage  
- Detect over-quota customers  
- Create support tickets  
- Automate customer ops workflows  

This is a *real-world production architecture* scaled down for clarity.

---

## 🏗 System Architecture

```
                      ┌──────────────────────┐
                      │       Frontend       │
                      └──────────┬───────────┘
                                 │ Text Query
                                 ▼
                        ┌─────────────────┐
                        │   LangGraph     │
                        │    Agent        │
                        └────────┬────────┘
                                 │ Tool Calls
                                 ▼
                 ┌──────────────────────────────────┐
                 │    MCP Client (inside agent)     │
                 └───────────────┬──────────────────┘
                                 │
        ┌──────────────────────────────────────────────────────────┐
        ▼                                                          ▼
┌──────────────┐                                           ┌─────────────────┐
│ MCP Server   │                                           │ MCP Server      │  (future)
│ (SaaS Tools) │                                           │ (Vector Search) │
└──────┬───────┘                                           └────────┬────────┘
       │ Backend Calls                                              │
       ▼                                                            ▼
┌──────────────┐  ┌───────────────┐  ┌──────────────────┐
│ billing.py   │  │ users.py      │  │ tickets.py       │
└──────────────┘  └───────────────┘  └──────────────────┘
```

---

## ✨ Features

### 🧠 AI Agent (LangGraph)
- Handles multi-step workflows  
- Decides when to call MCP tools  
- Can plan, correct, retry, summarize  

### 🔌 MCP Server
- Exposes backend services as clean tool APIs  
- Supports multiple services  
- Fully model-agnostic  

### 🏢 SaaS Backend
Includes:
- User accounts  
- Plans and billing  
- Seat usage  
- Support ticketing  

---

## 📂 Folder Structure

```
project/
│
├─ backend/
│  ├─ users.py               # User accounts
│  ├─ billing.py             # Subscription plans
│  ├─ tickets.py             # Support tickets
│  └─ usage.py               # Seat usage & over-quota logic
│
├─ mcp_server.py             # MCP tool server
│
├─ agent/
│  ├─ graph.py               # LangGraph workflow
│  └─ run_agent.py           # Entry point for agent
│
└─ README.md
```

---

## 🛠 Requirements

Add to `requirements.txt`:

```
langgraph
langchain
langchain-anthropic
anthropic
mcp
pydantic
fastapi
uvicorn
```

Install:

```
pip install -r requirements.txt
```

You will also need:

- Python 3.10+
- An API key for **Anthropic** (Claude) or **OpenAI GPT with tools**
  
Set your key:

```
export ANTHROPIC_API_KEY="sk-..."
```

or create a `.env` file from `example.env` file

---

## ▶️ How to Run the Project

### **Step 1 — Start the MCP Server**

In a terminal:

```
python mcp_server.py
```

You should see:

```
[MCP server] Starting 'saas-backend' server...
Tools loaded: fetch_customer, upgrade_plan...
```

Leave this running.

---

### **Step 2 — Run the LangGraph Agent**

Open a second terminal:

```
python agent/run_agent.py
```

Expected output (simplified):

```
--- MESSAGE ---
User: A customer (ID 200)...

--- MESSAGE ---
{"plan": "free", "seats_total": 3, "seats_used": 3, "over_limit": true}

--- MESSAGE ---
{"status": "ok", "old": "free", "new": "starter"}

--- MESSAGE ---
{"id": 1, "title": "...", "status": "open"}

--- MESSAGE ---
All tasks completed successfully.
```

The agent:

1. Checks usage  
2. Detects seat quota issues  
3. Upgrades customer to “starter”  
4. Opens a support ticket  
5. Summarizes the workflow  

---

## 💡 Example Queries You Can Try

```
Upgrade user 100 to enterprise if they are over the seat limit.
```

```
List available plans and recommend one for user 200.
```

```
Create a support ticket for user 100 complaining about billing issues.
```

```
Give me a complete account summary for customer 100.
```

---

## 🧩 How the Components Fit Together

### LangGraph agent:
- Receives the user message  
- Runs the LLM with tool-binding  
- When a tool call is requested → routes to MCP  

### MCP client:
- Translates LLM tool calls into MCP RPC calls  
- Communicates with the MCP server  

### MCP server:
- Executes backend functions  
- Returns JSON results back to the agent  

### Backend:
- Contains real business logic  
- Same code you would use in a real SaaS platform  

---

## 🧱 Extending the Project (Real Production Ideas)

You can extend this repo into a real system by adding:

### Backend:
- PostgreSQL database  
- Redis caches  
- Billing via Stripe  
- User events + logs  

### MCP servers:
- Vector search (for embeddings)  
- GitHub / Slack integration  
- Document retrieval  
- File system  

### LangGraph:
- Multi-agent systems  
- Memory layers  
- Updatable knowledge  
- Workflow branching  

### Deployment:
- Docker + Docker Compose  
- Fly.io, Railway, AWS, or GCP  
- WebSocket-based MCP  

---

## 🐞 Troubleshooting

### MCP server not found
Check that `mcp_server.py` is running.

### No tools are loaded
Ensure your MCPClient matches:

```
MCPClient(
    mode="stdio",
    command="python",
    args=["mcp_server.py"]
)
```

### LLM doesn’t call tools
Make sure you used:

```
llm.bind_tools(tools)
```

### Import errors
Run from project root:

```
python agent/run_agent.py
```

### Claude refuses improper tool calls
Make sure tool schemas have valid parameters.

---
