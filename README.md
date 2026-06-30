# Personal Task & Email Assistant Agent

An AI agent built with **Groq** (free, blazing-fast Llama 3.3 70B) that manages your tasks and
summarizes your inbox using **tool-calling** — the core building block of agentic AI systems.

## Live Demo :- https://ai-task-agent-bkwe9qnzslatzjccowrepa.streamlit.app/

## Premium Replit Live :- groq-python-convert--srilehkakada.replit.app ( Expires in 30 days )

## What makes this an "agent" and not just a chatbot?

Instead of only replying with text, the AI decides **which action to take**:
- `add_task` — creates a task in the database
- `summarize_emails` — reads sample emails and summarizes/prioritizes them
- `list_tasks` — fetches your current tasks

This decision-making + tool execution loop (see `agent.py` → `run_agent()`) is exactly
how production AI agents work (e.g. customer support bots, coding agents).

## Why Groq?

- ⚡ **Extremely fast** inference (often 10x faster than other providers)
- 🆓 **Free tier** is generous — no credit card required to start
- 🔧 **OpenAI-compatible** tool-calling API
- 🦙 Runs **Llama 3.3 70B**, an excellent open model for agents

## Files

| File | Purpose |
|---|---|
| `app.py` | Streamlit UI — chat interface + live task dashboard |
| `agent.py` | Core agent logic: tool definitions + the tool-calling loop (Groq) |
| `database.py` | SQLite functions for storing/retrieving tasks |
| `sample_data.py` | Dummy emails (simulates an inbox — no Gmail login needed) |
| `requirements.txt` | Python dependencies |

## How to run on Replit

1. Create a new **Python Repl** on replit.com
2. Upload these 5 files (`app.py`, `agent.py`, `database.py`, `sample_data.py`, `requirements.txt`)
3. Go to the **Secrets** tab (lock icon on the left sidebar) and add:
   - Key: `GROQ_API_KEY`
   - Value: your Groq API key (get one free at https://console.groq.com/keys)
4. Open the **Shell** tab and run:
