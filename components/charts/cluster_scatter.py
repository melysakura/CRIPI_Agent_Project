"""PCA scatter plot of states colored by cluster or investment priority."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.cluster_utils import add_pca_coordinates, pca_axis_labels
from components.theme import (
    CLUSTER_COLORS,
    DARK_BLUE,
    PRIORITY_COLORS,
    apply_chart_theme,
)


def render_cluster_scatter(df: pd.DataFrame, selected_cluster: int, color_mode: str) -> None:
    """Draw a PCA scatter plot with state labels and rich hover details."""
    plot_df = add_pca_coordinates(df)
    pc1_label, pc2_label = pca_axis_labels(plot_df)

    if color_mode == "Investment priority":
        color_column = "investment_priority_category"
        color_map = PRIORITY_COLORS
    else:
        color_column = "cluster_label"
        plot_df["cluster_label"] = plot_df["cluster"].map(lambda value: f"Cluster {value}")
        color_map = {f"Cluster {key}": value for key, value in CLUSTER_COLORS.items()}

    fig = px.scatter(
        plot_df,
        x="pc1",
        y="pc2",
        color=color_column,
        color_discrete_map=color_map,
        hover_name="state",
        custom_data=[
            "cluster",
            "cripi",
            "investment_priority_category",
            "hazard_dimension_index",
            "exposure_dimension_index",
            "sensitivity_dimension_index",
            "adaptive_capacity_dimension_index",
        ],
        labels={"pc1": pc1_label, "pc2": pc2_label, color_column: "Group"},
    )

    fig.update_traces(
        marker={"size": 14, "line": {"width": 1, "color": DARK_BLUE}, "opacity": 0.92},
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Cluster: %{customdata[0]}<br>"
            "CRIPI: %{customdata[1]:.1f}<br>"
            "Priority: %{customdata[2]}<br>"
            "Hazard: %{customdata[3]:.1f}<br>"
            "Exposure: %{customdata[4]:.1f}<br>"
            "Sensitivity: %{customdata[5]:.1f}<br>"
            "Adaptive capacity gap: %{customdata[6]:.1f}"
            "<extra></extra>"
        ),
    )

    for _, row in plot_df.iterrows():
        is_selected_cluster = row["cluster"] == selected_cluster
        fig.add_annotation(
            x=row["pc1"],
            y=row["pc2"],
            text=row["state"],
            showarrow=False,
            yshift=12,
            font={
                "size": 11 if is_selected_cluster else 9,
                "color": DARK_BLUE,
                "weight": "bold" if is_selected_cluster else "normal",
            },
        )

    if color_mode == "Cluster":
        highlight = plot_df[plot_df["cluster"] == selected_cluster]
        fig.add_trace(
            go.Scatter(
                x=highlight["pc1"],
                y=highlight["pc2"],
                mode="markers",
                marker={
                    "size": 22,
                    "color": "rgba(0,0,0,0)",
                    "line": {"width": 3, "color": DARK_BLUE},
                },
                hoverinfo="skip",
                showlegend=False,
            )
        )

    apply_chart_theme(fig, height=520)
    fig.update_layout(
        title="State positions in vulnerability space (PCA on 4 dimension indices)",
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "x": 0},
        margin={"t": 70, "b": 20, "l": 20, "r": 20},
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
