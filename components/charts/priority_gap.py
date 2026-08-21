"""Bar chart comparing Very High vs Low priority states across dimensions."""

import pandas as pd
import plotly.express as px
import streamlit as st

from components.formatting import format_number, round_value
from components.theme import (
    DIMENSION_INDEX_LABELS,
    GAP_HIGH_COLOR,
    GAP_LOW_COLOR,
    apply_chart_theme,
)


def render_priority_gap_chart(df: pd.DataFrame) -> None:
    """Compare average dimension scores for Very High and Low priority groups."""
    very_high = df[df["investment_priority_category"] == "Very High Priority"]
    low = df[df["investment_priority_category"] == "Low Priority"]

    dimension_columns = list(DIMENSION_INDEX_LABELS.keys())
    summary = pd.DataFrame(
        {
            "dimension": [DIMENSION_INDEX_LABELS[column] for column in dimension_columns],
            "Very High Priority": [round_value(very_high[column].mean()) for column in dimension_columns],
            "Low Priority": [round_value(low[column].mean()) for column in dimension_columns],
        }
    )

    melted = summary.melt(
        id_vars="dimension",
        value_vars=["Very High Priority", "Low Priority"],
        var_name="Priority group",
        value_name="Average index",
    )

    fig = px.bar(
        melted,
        x="dimension",
        y="Average index",
        color="Priority group",
        barmode="group",
        title="Dimension index gap: Very High vs Low priority states",
        labels={"dimension": "Dimension", "Average index": "Average index (0–100)"},
        color_discrete_map={
            "Very High Priority": GAP_HIGH_COLOR,
            "Low Priority": GAP_LOW_COLOR,
        },
    )
    apply_chart_theme(fig, height=380)
    fig.update_yaxes(tickformat=".1f")
    fig.update_traces(
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"
            "Dimension: %{x}<br>"
            "Average index: %{y:.1f}<extra></extra>"
        )
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    sensitivity_gap = (
        summary.loc[summary["dimension"] == "Sensitivity", "Very High Priority"].iloc[0]
        - summary.loc[summary["dimension"] == "Sensitivity", "Low Priority"].iloc[0]
    )
    adaptive_gap = (
        summary.loc[summary["dimension"] == "Adaptive Capacity Gap", "Very High Priority"].iloc[0]
        - summary.loc[summary["dimension"] == "Adaptive Capacity Gap", "Low Priority"].iloc[0]
    )
    st.caption(
        "Very High priority states average "
        f"**{format_number(sensitivity_gap)}** points higher on Sensitivity and "
        f"**{format_number(adaptive_gap)}** points higher on Adaptive Capacity Gap than Low priority states."
    )
