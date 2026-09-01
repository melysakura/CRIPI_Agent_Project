"""Home page introducing the CRIPI framework and how to use the app."""

import streamlit as st

from components.page_style import apply_page_style

AGENT_VERSION = "cripi-dashboard-v11"

if st.session_state.get("agent_version") != AGENT_VERSION:
    st.session_state.clear()
    st.session_state["agent_version"] = AGENT_VERSION

apply_page_style()

st.markdown(
    '<h1 class="page-title">CRIPI Explained 📘</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="page-caption">Climate Resilience Investment Priority Index for Mexico</p>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="intro-panel">
        The <strong>Climate Resilience Investment Priority Index (CRIPI)</strong> is a decision-support tool
        for comparing climate vulnerability and investment needs across Mexico's 32 states.
        It adapts the IPCC climate risk framework into a transparent, data-driven index built from
        official environmental and socioeconomic indicators.
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("🎯 What can it be used for?")
st.markdown(
    """
    <div class="intro-panel">
        CRIPI helps answer strategic questions such as:
        <ul>
            <li>Which states should be prioritized for climate resilience investments?</li>
            <li>How do states differ across hazard, exposure, sensitivity and adaptive capacity?</li>
            <li>Which indicators drive higher vulnerability in specific regions?</li>
            <li>Do states with similar vulnerability profiles form meaningful groups for policy design?</li>
        </ul>
        The app supports briefing preparation, portfolio planning, and analyst-level exploration —
        not automated allocation decisions on its own.
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("👥 Who is this app for?")
st.markdown(
    """
    <div class="intro-panel">
        The dashboard is designed for <strong>international development cooperation</strong> audiences,
        including GIZ-style programme managers, climate and resilience advisors, policy analysts,
        and executive briefings. It presents technical analysis in plain language suitable for
        workshops, donor reporting, and cross-team coordination.
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("🔬 Methodology at a glance")
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="cluster-summary-card">
            <div class="cluster-summary-title">Four IPCC-inspired dimensions</div>
            <div class="cluster-summary-subtitle">
                Each state is assessed on Hazard, Exposure, Sensitivity and Adaptive Capacity using
                12 official indicators from sources such as INEGI, CONEVAL and CENAPRED.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="cluster-summary-card">
            <div class="cluster-summary-title">CRIPI index (0–100)</div>
            <div class="cluster-summary-subtitle">
                Dimension scores are combined into a single priority index. Higher values indicate
                greater need for climate resilience investment. States are ranked and classified into
                four priority categories from Low to Very High.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="cluster-summary-card">
            <div class="cluster-summary-title">K-Means clustering (k = 4)</div>
            <div class="cluster-summary-subtitle">
                An unsupervised learning step groups states with similar dimension profiles.
                Clustering complements CRIPI — it does not replace the investment priority ranking.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="cluster-summary-card">
            <div class="cluster-summary-title">AI assistant</div>
            <div class="cluster-summary-subtitle">
                A built-in assistant retrieves data via tools, analyzes patterns in natural language,
                and suggests practical recommendations grounded in the same dataset shown in the charts.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader("🧭 How to navigate the app")
st.markdown(
    """
    <div class="intro-panel">
        Use the sidebar to move between the four views:
        <ul>
            <li><strong>📊 CRIPI Dashboard</strong> — national KPIs, Mexico map, state or national indicator
            profiles, dimension rankings, and priority group comparisons.</li>
            <li><strong>🧩 State Clusters</strong> — PCA cluster map, cluster dimension profiles,
            indicator deltas, and clusters vs. investment priority analysis.</li>
            <li><strong>💬 CRIPI Assistant</strong> — ask questions about priorities, indicators, and clusters
            while you explore the data in the other pages.</li>
            <li><strong>📘 CRIPI Explained</strong> — this overview page.</li>
        </ul>
        Start with the <strong>CRIPI Dashboard</strong> for the national picture, use
        <strong>State Clusters</strong> for shared vulnerability profiles, and open
        <strong>CRIPI Assistant</strong> whenever you want a data-grounded explanation or recommendation.
    </div>
    """,
    unsafe_allow_html=True,
)
