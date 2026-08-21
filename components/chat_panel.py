"""Reusable AI chat panel for dashboard pages."""

import streamlit as st

from ai.agent import agent
from ai.prompts import SYSTEM_PROMPT

GREETINGS = {
    "hello",
    "hi",
    "hey",
    "hola",
    "good morning",
    "good afternoon",
    "good evening",
}


def init_chat_session(page_key: str, welcome_message: str, suggestions: list[str]) -> None:
    """Create the chat history for one page if it does not exist yet."""
    messages_key = f"messages_{page_key}"
    if messages_key not in st.session_state:
        st.session_state[messages_key] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": welcome_message},
        ]
    st.session_state["chat_suggestions"] = suggestions


def render_chat_panel(
    page_key: str,
    suggestions: list[str] | None = None,
    input_placeholder: str | None = None,
) -> None:
    """Show suggested prompts, chat history, and the chat input box."""
    messages_key = f"messages_{page_key}"
    suggestions = suggestions or st.session_state.get("chat_suggestions", [])

    st.divider()
    st.subheader("💬 Ask the CRIPI Assistant")

    if suggestions:
        chip_cols = st.columns(min(len(suggestions), 3))
        for index, suggestion in enumerate(suggestions[:3]):
            if chip_cols[index % 3].button(suggestion, key=f"suggestion_{page_key}_{index}"):
                _handle_prompt(page_key, suggestion)
                st.rerun()

    for message in st.session_state[messages_key][1:]:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.markdown(message["content"])
            else:
                st.write(message["content"])

    default_placeholder = "Ask about investment priorities, indicators, or states"
    prompt = st.chat_input(input_placeholder or default_placeholder)
    if prompt:
        _handle_prompt(page_key, prompt)
        st.rerun()


def _is_greeting(prompt: str) -> bool:
    """Return True when the user message is a simple hello-style greeting."""
    cleaned = prompt.strip().lower().rstrip("!?.")
    if cleaned in GREETINGS:
        return True
    return cleaned.startswith(("hello ", "hi ", "hey ", "hola "))


def _handle_prompt(page_key: str, prompt: str) -> None:
    """Send the user message to the agent and save the response."""
    messages_key = f"messages_{page_key}"
    st.session_state[messages_key].append({"role": "user", "content": prompt})

    if _is_greeting(prompt):
        response = "Hello! How can I help you today?"
    else:
        response = agent(st.session_state[messages_key])

    st.session_state[messages_key].append({"role": "assistant", "content": response})
