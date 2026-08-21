import pandas as pd
import streamlit as st

from components.formatting import format_number
from components.indicator_catalog import (
    INDICATOR_CATALOG,
    format_indicator_value,
    indicator_columns_for_dimension,
)
from components.theme import DIMENSIONS


def _benchmark_label(column: str, delta: float) -> str:
    meta = INDICATOR_CATALOG[column]
    if meta["higher_is_worse"]:
        if delta > 0:
            return f"+{format_number(delta)} vs national median (higher vulnerability)"
        if delta < 0:
            return f"{format_number(delta)} vs national median (lower vulnerability)"
    else:
        if delta > 0:
            return f"+{format_number(delta)} vs national median (stronger capacity)"
        if delta < 0:
            return f"{format_number(delta)} vs national median (weaker capacity)"
    return "At national median"


def _progress_value(column: str, value: float, benchmark: float) -> float:
    meta = INDICATOR_CATALOG[column]
    if benchmark == 0:
        return min(max(value, 0), 1)

    if meta["higher_is_worse"]:
        ratio = value / benchmark if benchmark else value
    else:
        ratio = value / benchmark if benchmark else value
    return min(max(ratio, 0), 1.5) / 1.5


def render_state_profile(df: pd.DataFrame, selected_state: str) -> None:
    state_row = df.loc[df["state"] == selected_state]
    if state_row.empty:
        st.warning("Select a valid state to view its indicator profile.")
        return

    row = state_row.iloc[0]
    st.subheader("State Indicator Profile")
    st.markdown(
        f"**{row['state']}** · CRIPI **{format_number(row['cripi'])}** · "
        f"Rank **{int(row['investment_priority_rank'])}** · "
        f"**{row['investment_priority_category']}** · Cluster **{int(row['cluster'])}**"
    )

    dimension_cols = st.columns(4)
    for column, dimension in zip(dimension_cols, DIMENSIONS):
        column.metric(dimension["label"], format_number(row[dimension["index_column"]]))

    national_medians = df.median(numeric_only=True)

    for dimension in DIMENSIONS:
        st.markdown(f"### {dimension['label']}")
        if dimension.get("note"):
            st.caption(dimension["note"])

        for indicator_column in indicator_columns_for_dimension(dimension["key"]):
            meta = INDICATOR_CATALOG[indicator_column]
            value = row[indicator_column]
            benchmark = national_medians[indicator_column]
            delta = value - benchmark

            label_col, value_col = st.columns([3, 2])
            label_col.markdown(f"**{meta['label']}**  \n_{meta['unit']} · {meta['source']}_")
            value_col.markdown(
                f"**{format_indicator_value(indicator_column, value)}**  \n"
                f"{_benchmark_label(indicator_column, delta)}"
            )
            st.progress(_progress_value(indicator_column, value, benchmark))
