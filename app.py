"""
app.py
Streamlit dashboard for the Personal Task & Email Assistant Agent.

Run with: streamlit run app.py
"""

import streamlit as st
from database import init_db, get_all_tasks, update_task_status, delete_task, clear_all_tasks
from agent import run_agent

st.set_page_config(page_title="AI Productivity Agent", page_icon="🤖", layout="wide")

# Initialize database on first run
init_db()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []          # for display
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []  # for Groq API context

st.title("🤖 Personal Task & Email Assistant Agent")
st.caption("An AI agent that manages your tasks and summarizes your emails using tool-calling. Powered by Groq ⚡")

col1, col2 = st.columns([1.3, 1])

# ---------------------------------------------------------------------------
# LEFT COLUMN: Chat interface with the agent
# ---------------------------------------------------------------------------
with col1:
    st.subheader("💬 Talk to your agent")
    st.caption("Try: \"Summarize my emails\" or \"Add a task to finish my project report by Friday, high priority\"")

    chat_container = st.container(height=420)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    user_input = st.chat_input("Ask your agent something...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Agent is thinking..."):
            try:
                reply, updated_history = run_agent(user_input, st.session_state.conversation_history)
                st.session_state.conversation_history = updated_history
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Error: {e}\n\nMake sure GROQ_API_KEY is set in Replit Secrets. Get a free key at console.groq.com/keys"
                })

        st.rerun()

    # Quick action buttons
    st.write("Quick actions:")
    qcol1, qcol2 = st.columns(2)
    with qcol1:
        if st.button("📧 Summarize my emails", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Summarize my emails and flag what's urgent."})
            with st.spinner("Reading your inbox..."):
                reply, updated_history = run_agent("Summarize my emails and flag what's urgent.", st.session_state.conversation_history)
                st.session_state.conversation_history = updated_history
                st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
    with qcol2:
        if st.button("📋 Show my tasks", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Show me my current task list."})
            with st.spinner("Fetching tasks..."):
                reply, updated_history = run_agent("Show me my current task list.", st.session_state.conversation_history)
                st.session_state.conversation_history = updated_history
                st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

# ---------------------------------------------------------------------------
# RIGHT COLUMN: Live task dashboard (direct from database)
# ---------------------------------------------------------------------------
with col2:
    st.subheader("📌 Task Dashboard")

    tasks = get_all_tasks()

    if not tasks:
        st.info("No tasks yet. Ask the agent to add one!")
    else:
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        tasks_sorted = sorted(tasks, key=lambda t: priority_order.get(t[2], 3))

        for task_id, title, priority, deadline, status in tasks_sorted:
            color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(priority, "⚪")
            done = status == "completed"

            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    label = f"~~{title}~~" if done else f"**{title}**"
                    st.markdown(f"{color} {label}")
                    st.caption(f"Priority: {priority} | Deadline: {deadline}")
                with c2:
                    if not done:
                        if st.button("✓ Done", key=f"done_{task_id}"):
                            update_task_status(task_id, "completed")
                            st.rerun()
                    if st.button("🗑️", key=f"del_{task_id}"):
                        delete_task(task_id)
                        st.rerun()

    st.divider()
    if st.button("Clear all tasks", type="secondary"):
        clear_all_tasks()
        st.rerun()

st.divider()
st.caption("Built as Phase 1 of a 1-year AI Agent learning roadmap — Foundation Agent (tool-calling, memory, agent loop). Powered by Groq ⚡")