"""Dedicated CRIPI AI assistant page for exploring the dataset via natural language."""

import streamlit as st

from components.chat_panel import init_chat_session, render_chat_panel
from components.page_style import apply_page_style

AGENT_VERSION = "cripi-dashboard-v11"

INITIAL_SUGGESTIONS = [
    "Why is Chiapas ranked first?",
    "Why are Very High Priority states similar?",
    "What investments would you recommend for Chiapas?",
]

FOLLOW_UP_SUGGESTIONS = [
    "Which states belong to Cluster 1 and what do they have in common?",
    "What makes Cluster 1 distinctive compared to the national average?",
    "What interventions would you recommend for Cluster 1?",
    "Compare Oaxaca and Nuevo León at the indicator level",
    "Which adaptive capacity indicators are weakest in Veracruz?",
    "Which high-priority states are not in the same cluster?",
]

WELCOME_MESSAGE = (
    "The CRIPI Assistant answers questions about investment priorities, state indicators, "
    "and cluster profiles using the same dataset as the dashboard and cluster pages."
)

if st.session_state.get("agent_version") != AGENT_VERSION:
    st.session_state.clear()
    st.session_state["agent_version"] = AGENT_VERSION

apply_page_style()

st.markdown(
    '<h1 class="page-title">CRIPI Assistant 💬</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="page-caption">Explore priorities, indicators, and clusters through conversation</p>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="intro-panel">
        Use this assistant while reviewing the <strong>CRIPI Dashboard</strong> and
        <strong>State Clusters</strong> pages. It retrieves real data from the index, explains patterns
        in plain language, and suggests practical next steps grounded in the indicators shown in the charts.
    </div>
    """,
    unsafe_allow_html=True,
)

init_chat_session(page_key="assistant", welcome_message=WELCOME_MESSAGE)
render_chat_panel(
    "assistant",
    initial_suggestions=INITIAL_SUGGESTIONS,
    follow_up_suggestions=FOLLOW_UP_SUGGESTIONS,
    input_placeholder="Ask about investment priorities, indicators, clusters, or specific states",
    standalone=True,
)
