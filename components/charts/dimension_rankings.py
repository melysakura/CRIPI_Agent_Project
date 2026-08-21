"""Horizontal bar charts showing the top 5 states for each dimension index."""

import pandas as pd
import plotly.express as px
import streamlit as st

from components.theme import CHART_ACCENT, DIMENSION_INDEX_LABELS, apply_chart_theme


def render_dimension_rankings(df: pd.DataFrame) -> None:
    """Create a 2x2 grid of top-5 state rankings by dimension index."""
    charts = [
        ("hazard_dimension_index", "Top 5 states by Hazard"),
        ("exposure_dimension_index", "Top 5 states by Exposure"),
        ("sensitivity_dimension_index", "Top 5 states by Sensitivity"),
        ("adaptive_capacity_dimension_index", "Top 5 states by Adaptive Capacity Gap"),
    ]

    top_left, top_right = st.columns(2)
    bottom_left, bottom_right = st.columns(2)
    columns = [top_left, top_right, bottom_left, bottom_right]

    for container, (metric, title) in zip(columns, charts):
        ranked = df.nlargest(5, metric).sort_values(metric, ascending=True)
        fig = px.bar(
            ranked,
            x=metric,
            y="state",
            orientation="h",
            text=metric,
            title=title,
            labels={
                metric: DIMENSION_INDEX_LABELS[metric],
                "state": "State",
            },
            color_discrete_sequence=[CHART_ACCENT],
        )
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        apply_chart_theme(fig, height=320)
        fig.update_layout(showlegend=False)
        container.plotly_chart(fig, use_container_width=True)
