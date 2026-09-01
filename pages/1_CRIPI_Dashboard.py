"""Main dashboard page: CRIPI overview, map, and charts."""

import streamlit as st

from ai.data_loader import load_cripi_data
from components.charts.dimension_rankings import render_dimension_rankings
from components.charts.mexico_map import render_mexico_map
from components.charts.priority_gap import render_priority_gap_chart
from components.kpi_cards import render_kpi_cards
from components.page_style import apply_page_style
from components.state_sidebar import render_national_profile, render_state_profile

AGENT_VERSION = "cripi-dashboard-v11"
ALL_STATES_OPTION = "All states"

if st.session_state.get("agent_version") != AGENT_VERSION:
    st.session_state.clear()
    st.session_state["agent_version"] = AGENT_VERSION

apply_page_style()

df = load_cripi_data()
state_options = df.sort_values("cripi", ascending=False)["state"].tolist()
dropdown_options = [ALL_STATES_OPTION] + state_options

if "map_selection" not in st.session_state:
    st.session_state["map_selection"] = ALL_STATES_OPTION

st.markdown(
    '<h1 class="page-title">Climate Resilience Investment Priority Framework - Mexico 🇲🇽</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="page-caption">IPCC-informed decision support for international development cooperation</p>',
    unsafe_allow_html=True,
)

render_kpi_cards(df)

st.subheader("🗺️ Geographic overview")
current_selection = st.session_state.get("map_selection", ALL_STATES_OPTION)
selection_index = (
    dropdown_options.index(current_selection) if current_selection in dropdown_options else 0
)

map_selection = st.selectbox(
    "Select a state",
    dropdown_options,
    index=selection_index,
    key="state_selector",
)
st.session_state["map_selection"] = map_selection

if map_selection == ALL_STATES_OPTION:
    render_mexico_map(df, focus_state=None)
    render_national_profile(df)
else:
    render_mexico_map(df, focus_state=map_selection)
    render_state_profile(df, map_selection)

st.subheader("📊 Top states by dimension")
render_dimension_rankings(df)

st.subheader("⚖️ Priority group comparison")
render_priority_gap_chart(df)
