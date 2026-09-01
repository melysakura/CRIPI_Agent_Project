"""Send user messages to the OpenAI API, run tools, and return synthesized answers."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from ai.tools import (
    TOOLS,
    get_cluster_profile,
    get_state_data,
    rank_states,
    summarize_priority_group,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=True)

MAX_TOOL_ROUNDS = 3
DEFAULT_MODEL = "gpt-4o-mini"

MISSING_API_KEY_MESSAGE = (
    "The CRIPI Assistant is not available because no API key is configured. "
    "Add `OPENAI_API_KEY` in Streamlit Cloud secrets or in a local `.env` file, then save the file."
)

LEGACY_XAI_KEY_MESSAGE = (
    "Found `XAI_API_KEY` in your environment, but this app now uses OpenAI. "
    "Rename it to `OPENAI_API_KEY` in your `.env` or Streamlit secrets and save the file."
)

TOOL_HANDLERS = {
    "get_state_data": get_state_data,
    "rank_states": rank_states,
    "summarize_priority_group": summarize_priority_group,
    "get_cluster_profile": get_cluster_profile,
}


def _run_tool(tool_name: str, arguments: dict) -> str:
    """Execute one tool and return its JSON string result."""
    handler = TOOL_HANDLERS.get(tool_name)
    if handler is None:
        return json.dumps({"error": f"Unknown tool requested: {tool_name}"})
    return handler(**arguments)


def _assistant_tool_message(response) -> dict:
    """Build an assistant message dict that includes tool calls for the API."""
    tool_calls = []
    for tool_call in response.tool_calls:
        tool_calls.append(
            {
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments,
                },
            }
        )
    return {
        "role": "assistant",
        "content": response.content,
        "tool_calls": tool_calls,
    }


def _get_api_key() -> str | None:
    """Read the OpenAI API key from the environment or Streamlit secrets."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key

    try:
        import streamlit as st

        return st.secrets.get("OPENAI_API_KEY")
    except Exception:
        return None


def _has_legacy_xai_key() -> bool:
    """Return True when an old xAI key is still configured."""
    if os.environ.get("XAI_API_KEY"):
        return True

    try:
        import streamlit as st

        return bool(st.secrets.get("XAI_API_KEY"))
    except Exception:
        return False


def _get_model() -> str:
    """Return the chat model name, defaulting to a cost-efficient OpenAI model."""
    return os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)


def agent(messages: list[dict]) -> str:
    """Call the LLM, run tools if needed, and return a natural-language answer."""
    api_key = _get_api_key()
    if not api_key:
        if _has_legacy_xai_key():
            return LEGACY_XAI_KEY_MESSAGE
        return MISSING_API_KEY_MESSAGE

    client = OpenAI(api_key=api_key)
    model = _get_model()

    api_messages = [message for message in messages if message["role"] in ("system", "user", "assistant", "tool")]

    try:
        for _ in range(MAX_TOOL_ROUNDS):
            completion = client.chat.completions.create(
                model=model,
                tools=TOOLS,
                messages=api_messages,
            )
            response = completion.choices[0].message

            if not response.tool_calls:
                return response.content or "I could not generate a response. Please try rephrasing your question."

            api_messages.append(_assistant_tool_message(response))

            for tool_call in response.tool_calls:
                tool_name = tool_call.function.name
                tool_arguments = json.loads(tool_call.function.arguments or "{}")
                tool_result = _run_tool(tool_name, tool_arguments)
                api_messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result,
                    }
                )

        final_completion = client.chat.completions.create(
            model=model,
            messages=api_messages,
        )
        return final_completion.choices[0].message.content or "I could not complete the analysis."
    except Exception as error:
        return (
            "The CRIPI Assistant could not reach OpenAI. "
            f"Check that your API key is valid and billing is enabled. ({type(error).__name__})"
        )
