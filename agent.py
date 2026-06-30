"""
agent.py
Core AI Agent logic — now powered by Groq (free, fast Llama 3.3 70B).

This is the heart of the "agentic" behavior: instead of just replying with text,
the agent decides WHICH tool to call (add_task, summarize_emails, list_tasks)
based on what the user asks. This tool-calling loop is what separates an "agent"
from a simple chatbot.
"""

import os
import json
from groq import Groq
from database import add_task, get_all_tasks
from sample_data import SAMPLE_EMAILS

# The API key is read from an environment variable (set this in Replit's "Secrets" tab
# as GROQ_API_KEY -- never hardcode API keys directly in your code).
# Get a free key at https://console.groq.com/keys
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"

# ---------------------------------------------------------------------------
# TOOL DEFINITIONS (OpenAI-compatible format, which Groq uses)
# These tell the model what actions ("tools") it is allowed to take.
# This is the core of agentic / tool-calling AI.
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task to the user's task list with a priority level and optional deadline.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Short description of the task"},
                    "priority": {"type": "string", "enum": ["High", "Medium", "Low"], "description": "Priority level of the task"},
                    "deadline": {"type": "string", "description": "Deadline for the task, e.g. 'Monday 10 AM' or 'Not specified'"}
                },
                "required": ["title", "priority"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_emails",
            "description": "Summarize the user's unread emails, extract action items, and flag which ones are urgent.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Get the user's current task list from the database.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
]


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Runs the actual Python function that corresponds to the tool the model chose."""
    if tool_name == "add_task":
        return add_task(
            title=tool_input.get("title"),
            priority=tool_input.get("priority", "Medium"),
            deadline=tool_input.get("deadline", "Not specified")
        )

    elif tool_name == "summarize_emails":
        emails_text = "\n\n".join(
            [f"From: {e['from']}\nSubject: {e['subject']}\nBody: {e['body']}" for e in SAMPLE_EMAILS]
        )
        return emails_text  # raw emails returned to the model for it to summarize in its final answer

    elif tool_name == "list_tasks":
        tasks = get_all_tasks()
        if not tasks:
            return "No tasks found."
        return "\n".join([f"#{t[0]} | {t[1]} | Priority: {t[2]} | Deadline: {t[3]} | Status: {t[4]}" for t in tasks])

    return "Unknown tool."


SYSTEM_PROMPT = """You are Pooja's personal productivity AI agent.

You help manage her tasks and emails. You have access to tools:
- add_task: use this when the user wants to create/add a task, OR when summarizing
  emails reveals an action item that should become a task (ask user first, don't auto-add silently
  unless they say "add these as tasks").
- summarize_emails: use this when the user asks about their emails/inbox.
- list_tasks: use this when the user asks to see their current tasks.

Be concise, friendly, and proactive. When you summarize emails, clearly flag which ones
are urgent/time-sensitive vs informational. When listing tasks, organize by priority.
"""


def run_agent(user_message: str, conversation_history: list) -> tuple:
    """
    Main agent loop. Sends the user's message to Groq along with the
    available tools. If the model decides to call a tool, we execute it and
    send the result back so it can give a final natural-language answer.

    Returns: (final_text_response, updated_conversation_history)
    """
    # Groq/OpenAI format keeps the system prompt inside the messages list
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + \
               conversation_history + \
               [{"role": "user", "content": user_message}]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        max_tokens=1024,
        temperature=0.4,
    )

    msg = response.choices[0].message

    # Keep looping while the model wants to use tools (it may chain multiple tool calls)
    safety = 0
    while msg.tool_calls and safety < 5:
        safety += 1

        # Append the assistant message containing the tool_calls
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in msg.tool_calls
            ],
        })

        # Execute each tool call and append its result
        for tc in msg.tool_calls:
            try:
                tool_input = json.loads(tc.function.arguments) if tc.function.arguments else {}
            except json.JSONDecodeError:
                tool_input = {}

            result = execute_tool(tc.function.name, tool_input)

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "name": tc.function.name,
                "content": result,
            })

        # Ask the model again now that it has the tool results
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            max_tokens=1024,
            temperature=0.4,
        )
        msg = response.choices[0].message

    # Extract final text reply
    final_text = msg.content or ""

    # Append final assistant message to history
    messages.append({"role": "assistant", "content": final_text})

    # Strip the system message before returning — we re-add it on each call
    updated_history = [m for m in messages if m.get("role") != "system"]

    return final_text, updated_history