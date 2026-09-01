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


def init_chat_session(page_key: str, welcome_message: str) -> None:
    """Create the chat history for one page if it does not exist yet."""
    messages_key = f"messages_{page_key}"
    if messages_key not in st.session_state:
        st.session_state[messages_key] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": welcome_message},
        ]


def _user_message_count(page_key: str) -> int:
    """Return how many user messages have been sent in this chat."""
    messages_key = f"messages_{page_key}"
    return sum(1 for message in st.session_state[messages_key] if message["role"] == "user")


def _visible_suggestions(
    page_key: str,
    initial_suggestions: list[str],
    follow_up_suggestions: list[str],
) -> list[str]:
    """Show three starters before the first question, then two follow-ups afterward."""
    if _user_message_count(page_key) == 0:
        return initial_suggestions[:3]

    if len(follow_up_suggestions) < 2:
        return follow_up_suggestions

    start = ((_user_message_count(page_key) - 1) * 2) % len(follow_up_suggestions)
    return [
        follow_up_suggestions[start],
        follow_up_suggestions[(start + 1) % len(follow_up_suggestions)],
    ]


def render_chat_panel(
    page_key: str,
    suggestions: list[str] | None = None,
    initial_suggestions: list[str] | None = None,
    follow_up_suggestions: list[str] | None = None,
    input_placeholder: str | None = None,
    standalone: bool = False,
) -> None:
    """Show suggested prompts, chat history, and the chat input box."""
    messages_key = f"messages_{page_key}"

    if initial_suggestions is None and suggestions:
        initial_suggestions = suggestions[:3]
    if follow_up_suggestions is None and suggestions:
        follow_up_suggestions = suggestions[3:]

    initial_suggestions = initial_suggestions or []
    follow_up_suggestions = follow_up_suggestions or []
    visible_suggestions = _visible_suggestions(page_key, initial_suggestions, follow_up_suggestions)
    user_message_count = _user_message_count(page_key)

    if not standalone:
        st.divider()
        st.subheader("💬 Ask the CRIPI Assistant")

    for message in st.session_state[messages_key][1:]:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.markdown(message["content"])
            else:
                st.write(message["content"])

    if visible_suggestions:
        chip_cols = st.columns(len(visible_suggestions))
        for index, suggestion in enumerate(visible_suggestions):
            if chip_cols[index].button(
                suggestion,
                key=f"suggestion_{page_key}_{user_message_count}_{index}",
            ):
                _handle_prompt(page_key, suggestion)
                st.rerun()

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
