"""Indicator delta tables for a selected cluster."""

import pandas as pd
import streamlit as st

from components.cluster_utils import (
    format_delta_value,
    format_profile_value,
    indicator_delta_table_for_dimension,
)
from components.theme import DIMENSIONS, LIGHT_BLUE

DELTA_LEGEND_HTML = """
<div class="delta-legend">
    The indicator deltas table answers one question:<br><br>
    <strong>For the selected cluster, which indicators are most different from the average across all of Mexico?</strong><br><br>
    Positive deltas mean the cluster is above the national average; negative deltas mean it is below.
    Highlighted rows show the most distinctive indicator within each dimension for the selected cluster.
</div>
"""


def _format_delta_display_table(delta_df: pd.DataFrame) -> pd.DataFrame:
    """Turn raw delta rows into formatted text for display."""
    return pd.DataFrame(
        {
            "Indicator": delta_df["Indicator"],
            "Cluster mean": [
                format_profile_value(row["column"], row["Cluster mean"]) for _, row in delta_df.iterrows()
            ],
            "National mean": [
                format_profile_value(row["column"], row["National mean"]) for _, row in delta_df.iterrows()
            ],
            "Delta": [format_delta_value(row["column"], row["Delta"]) for _, row in delta_df.iterrows()],
        }
    )


def _style_top_delta_row(display_df: pd.DataFrame) -> pd.DataFrame:
    """Highlight the first row, which is the most distinctive indicator in the dimension."""
    def _highlight(row: pd.Series) -> list[str]:
        if row.name == 0:
            return [f"background-color: {LIGHT_BLUE}; font-weight: 600; color: #1A365D;"] * len(row)
        return [""] * len(row)

    return display_df.style.apply(_highlight, axis=1)


def _render_dimension_delta_table(
    container,
    df: pd.DataFrame,
    cluster_id: int,
    dimension: dict,
) -> None:
    """Render one dimension's delta table with the top distinctive row highlighted."""
    delta_df, _ = indicator_delta_table_for_dimension(df, cluster_id, dimension["key"])
    if delta_df.empty:
        container.caption("No indicators available for this dimension.")
        return

    display_df = _format_delta_display_table(delta_df)
    container.markdown(f"**{dimension['emoji']} {dimension['label']}**")
    container.dataframe(
        _style_top_delta_row(display_df),
        use_container_width=True,
        hide_index=True,
    )


def render_cluster_indicator_profile(df: pd.DataFrame, cluster_id: int) -> None:
    """Show dimension-level indicator delta tables for one cluster."""
    st.markdown("**Indicator deltas**")
    st.markdown(DELTA_LEGEND_HTML, unsafe_allow_html=True)

    delta_top_left, delta_top_right = st.columns(2)
    delta_bottom_left, delta_bottom_right = st.columns(2)
    delta_panels = [delta_top_left, delta_top_right, delta_bottom_left, delta_bottom_right]

    for panel, dimension in zip(delta_panels, DIMENSIONS):
        _render_dimension_delta_table(panel, df, cluster_id, dimension)
