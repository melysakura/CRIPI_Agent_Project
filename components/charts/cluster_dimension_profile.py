"""Grouped bar chart comparing cluster and national dimension index means."""

import pandas as pd
import plotly.express as px
import streamlit as st

from components.cluster_utils import cluster_dimension_means, national_dimension_means
from components.formatting import round_value
from components.theme import (
    CLUSTER_MEAN_COLOR,
    DIMENSION_INDEX_LABELS,
    NATIONAL_BENCHMARK_COLOR,
    apply_chart_theme,
)


def render_cluster_dimension_profile(df: pd.DataFrame, cluster_id: int) -> None:
    """Show average dimension scores for one cluster against the national mean."""
    cluster_means = cluster_dimension_means(df, cluster_id)
    national_means = national_dimension_means(df)

    rows = []
    for column, label in DIMENSION_INDEX_LABELS.items():
        rows.append(
            {
                "Dimension": label,
                "Series": f"Cluster {cluster_id} mean",
                "Average index": round_value(cluster_means[column]),
            }
        )
        rows.append(
            {
                "Dimension": label,
                "Series": "National mean",
                "Average index": round_value(national_means[column]),
            }
        )

    chart_df = pd.DataFrame(rows)
    fig = px.bar(
        chart_df,
        x="Dimension",
        y="Average index",
        color="Series",
        barmode="group",
        title=f"Dimension profile · Cluster {cluster_id}",
        labels={"Average index": "Average index (0–100)"},
        color_discrete_map={
            f"Cluster {cluster_id} mean": CLUSTER_MEAN_COLOR,
            "National mean": NATIONAL_BENCHMARK_COLOR,
        },
    )
    apply_chart_theme(fig, height=320)
    fig.update_yaxes(tickformat=".1f")
    fig.update_traces(
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"
            "Dimension: %{x}<br>"
            "Average index: %{y:.1f}<extra></extra>"
        )
    )
    fig.update_layout(showlegend=True, legend={"orientation": "h", "y": 1.15, "x": 0})
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
