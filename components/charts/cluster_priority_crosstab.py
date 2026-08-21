"""Cross-tabulation of ML clusters and CRIPI priority categories."""

import pandas as pd
import plotly.express as px
import streamlit as st

from components.theme import PRIORITY_COLORS, PRIORITY_ORDER, apply_chart_theme


def render_cluster_priority_crosstab(df: pd.DataFrame) -> None:
    """Show how investment priority categories distribute across clusters."""
    counts = (
        df.groupby(["cluster", "investment_priority_category"])
        .size()
        .reset_index(name="States")
    )
    counts["cluster_label"] = counts["cluster"].map(lambda value: f"Cluster {value}")

    fig = px.bar(
        counts,
        x="cluster_label",
        y="States",
        color="investment_priority_category",
        barmode="stack",
        title="Priority category mix within each cluster",
        labels={
            "cluster_label": "Cluster",
            "investment_priority_category": "Priority category",
        },
        category_orders={"investment_priority_category": PRIORITY_ORDER},
        color_discrete_map=PRIORITY_COLORS,
    )
    apply_chart_theme(fig, height=340)
    fig.update_traces(
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"
            "Cluster: %{x}<br>"
            "Number of states: %{y}<extra></extra>"
        )
    )
    fig.update_layout(legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "x": 0})
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
