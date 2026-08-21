"""Top KPI cards for the CRIPI Dashboard page."""

import streamlit as st

from components.formatting import format_number


def render_kpi_cards(df) -> None:
    """Show CRIPI range, highest state, lowest state, and total states analyzed."""
    highest = df.loc[df["investment_priority_rank"] == df["investment_priority_rank"].min()].iloc[0]
    lowest = df.loc[df["investment_priority_rank"] == df["investment_priority_rank"].max()].iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card kpi-card-split">
                <div class="kpi-card-left">
                    <div class="kpi-label">CRIPI Range</div>
                </div>
                <div class="kpi-value-right">{format_number(df['cripi'].min())} – {format_number(df['cripi'].max())}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card kpi-card-split">
                <div class="kpi-card-left">
                    <div class="kpi-label">Highest Priority</div>
                    <div class="kpi-state-large">{highest["state"]}</div>
                </div>
                <div class="kpi-value-highlight-high">{format_number(highest["cripi"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card kpi-card-split">
                <div class="kpi-card-left">
                    <div class="kpi-label">Lowest Priority</div>
                    <div class="kpi-state-large">{lowest["state"]}</div>
                </div>
                <div class="kpi-value-highlight-low">{format_number(lowest["cripi"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="kpi-card kpi-card-split">
                <div class="kpi-card-left">
                    <div class="kpi-label">States Analyzed</div>
                </div>
                <div class="kpi-value-right">{len(df)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
