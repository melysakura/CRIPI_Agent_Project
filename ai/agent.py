"""Send user messages to the Grok API, run tools, and return synthesized answers."""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from ai.tools import (
    TOOLS,
    get_cluster_profile,
    get_state_data,
    rank_states,
    summarize_priority_group,
)

load_dotenv()

MAX_TOOL_ROUNDS = 3

MISSING_API_KEY_MESSAGE = (
    "The CRIPI Assistant is not available because no API key is configured. "
    "Add `XAI_API_KEY` in Streamlit Cloud secrets or in a local `.env` file."
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
    """Read the xAI API key from the environment or Streamlit secrets."""
    api_key = os.environ.get("XAI_API_KEY")
    if api_key:
        return api_key

    try:
        import streamlit as st

        return st.secrets.get("XAI_API_KEY")
    except Exception:
        return None


def agent(messages: list[dict]) -> str:
    """Call the LLM, run tools if needed, and return a natural-language answer."""
    api_key = _get_api_key()
    if not api_key:
        return MISSING_API_KEY_MESSAGE

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",
    )

    api_messages = [message for message in messages if message["role"] in ("system", "user", "assistant", "tool")]

    for _ in range(MAX_TOOL_ROUNDS):
        completion = client.chat.completions.create(
            model="grok-3-mini",
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
        model="grok-3-mini",
        messages=api_messages,
    )
    return final_completion.choices[0].message.content or "I could not complete the analysis."
