"""State Clustering Analysis page — PCA scatter, cluster profiles, and AI assistant."""

import streamlit as st

from ai.data_loader import load_cripi_data
from components.charts.cluster_dimension_profile import render_cluster_dimension_profile
from components.charts.cluster_indicator_profile import render_cluster_indicator_profile
from components.charts.cluster_priority_crosstab import render_cluster_priority_crosstab
from components.charts.cluster_scatter import render_cluster_scatter
from components.cluster_utils import CLUSTER_SUMMARIES, cluster_member_states
from components.chat_panel import init_chat_session, render_chat_panel
from components.page_style import apply_page_style
from components.theme import CLUSTER_COLORS

AGENT_VERSION = "cripi-dashboard-v8"
CLUSTER_OPTIONS = [1, 2, 3, 4]

CHAT_SUGGESTIONS = [
    "Which states belong to Cluster 1 and what do they have in common?",
    "What makes Cluster 1 distinctive compared to the national average?",
    "What interventions would you recommend for Cluster 1?",
]

WELCOME_MESSAGE = (
    "Hi there! I can help you interpret K-Means clusters, compare vulnerability profiles, "
    "and relate clustering patterns to CRIPI investment priorities."
)

if st.session_state.get("agent_version") != AGENT_VERSION:
    st.session_state.clear()
    st.session_state["agent_version"] = AGENT_VERSION

apply_page_style()

df = load_cripi_data()

if "selected_cluster" not in st.session_state:
    st.session_state["selected_cluster"] = 1

st.markdown(
    '<h1 class="page-title">State Clustering Analysis 🧩</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="page-caption">How Mexican states group by similar climate vulnerability profiles (K-Means, k = 4)</p>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="intro-panel">
        K-Means clustering groups states by similarity across the four dimension indices.
        Clustering validates and complements CRIPI — it does not replace the investment priority ranking.
        Clusters help identify states that may need similar policy interventions even when their CRIPI rank differs.
    </div>
    """,
    unsafe_allow_html=True,
)

scatter_col, selector_col = st.columns([2.2, 1])

with selector_col:
    st.subheader("🔍 Explore clusters")
    selected_cluster = st.selectbox(
        "Select a cluster",
        CLUSTER_OPTIONS,
        index=CLUSTER_OPTIONS.index(st.session_state["selected_cluster"]),
        format_func=lambda cluster_id: f"Cluster {cluster_id} ({len(df[df['cluster'] == cluster_id])} states)",
        key="cluster_selector",
    )
    st.session_state["selected_cluster"] = selected_cluster

    members = cluster_member_states(df, selected_cluster)
    member_html = " · ".join(
        f'<span class="cluster-chip" style="border-color: {CLUSTER_COLORS[selected_cluster]};">{state}</span>'
        for state in members
    )
    st.markdown(
        f"""
        <div class="cluster-summary-card">
            <div class="cluster-summary-title">Cluster {selected_cluster}</div>
            <div class="cluster-summary-subtitle">{CLUSTER_SUMMARIES[selected_cluster]}</div>
            <div class="cluster-member-list">{member_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    color_mode = st.radio(
        "Color points by",
        ["Cluster", "Investment priority"],
        horizontal=True,
        key="scatter_color_mode",
    )

with scatter_col:
    st.subheader("📍 Cluster map")
    render_cluster_scatter(df, selected_cluster, color_mode)

st.subheader("📊 Cluster dimension profile")
render_cluster_dimension_profile(df, selected_cluster)

st.subheader("📋 Cluster indicator profile")
render_cluster_indicator_profile(df, selected_cluster)

st.subheader("🔀 Clusters vs investment priority")
st.caption("Shows that machine-learning clusters and CRIPI categories are related but not identical.")
render_cluster_priority_crosstab(df)

init_chat_session(
    page_key="clusters",
    welcome_message=WELCOME_MESSAGE,
    suggestions=CHAT_SUGGESTIONS,
)
render_chat_panel(
    "clusters",
    CHAT_SUGGESTIONS,
    input_placeholder="Ask about clusters, similarity between states, or indicator profiles",
)
