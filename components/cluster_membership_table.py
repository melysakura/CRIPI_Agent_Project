"""Sortable table of cluster membership and dimension scores."""

import pandas as pd
import streamlit as st

from components.formatting import format_number
from components.theme import DIMENSION_INDEX_LABELS


def render_cluster_membership_table(df: pd.DataFrame) -> None:
    """Show all states with cluster assignment and dimension indices."""
    table = df[
        [
            "state",
            "cluster",
            "cripi",
            "investment_priority_category",
            "hazard_dimension_index",
            "exposure_dimension_index",
            "sensitivity_dimension_index",
            "adaptive_capacity_dimension_index",
        ]
    ].copy()

    table = table.rename(
        columns={
            "state": "State",
            "cluster": "Cluster",
            "cripi": "CRIPI",
            "investment_priority_category": "Priority category",
            **{column: label for column, label in DIMENSION_INDEX_LABELS.items()},
        }
    )
    table = table.sort_values(["Cluster", "CRIPI"], ascending=[True, False])
    table["CRIPI"] = table["CRIPI"].map(format_number)

    for column in DIMENSION_INDEX_LABELS.values():
        table[column] = table[column].map(format_number)

    st.dataframe(table, use_container_width=True, hide_index=True)
