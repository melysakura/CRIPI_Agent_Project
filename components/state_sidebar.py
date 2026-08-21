"""State profile with dimension scores and indicators for the selected state."""

import pandas as pd
import streamlit as st

from components.cluster_utils import national_dimension_means, national_indicator_means
from components.formatting import format_number
from components.indicator_catalog import INDICATOR_CATALOG, indicator_columns_for_dimension, plain_indicator_value
from components.theme import DIMENSIONS


def _render_profile_grid(title: str, dimension_values: pd.Series, indicator_values: pd.Series) -> None:
    """Show four dimensions in a centered 2x2 grid with indicator values."""
    html_parts = [f'<div class="state-profile-title">{title}</div>']
    html_parts.append('<div class="dimension-grid">')

    for dimension in DIMENSIONS:
        score = dimension_values[dimension["index_column"]]
        html_parts.append('<div class="dimension-cell">')
        html_parts.append(
            f'<div class="dimension-name">{dimension["emoji"]} {dimension["label"]}</div>'
            f'<div class="dimension-score">{format_number(score)}</div>'
        )

        for indicator_column in indicator_columns_for_dimension(dimension["key"]):
            meta = INDICATOR_CATALOG[indicator_column]
            value = plain_indicator_value(indicator_column, indicator_values[indicator_column])
            html_parts.append(
                '<div class="indicator-line">'
                f'{meta["label"]}: '
                f'<span class="indicator-value">{value}</span> '
                f'<span class="indicator-unit">· {meta["unit"]}</span>'
                "</div>"
            )

        html_parts.append("</div>")

    html_parts.append("</div>")
    st.markdown("".join(html_parts), unsafe_allow_html=True)


def render_state_profile(df: pd.DataFrame, selected_state: str) -> None:
    """Show four dimensions in a centered 2x2 grid with indicators for one state."""
    state_row = df.loc[df["state"] == selected_state]
    if state_row.empty:
        st.warning("Select a valid state.")
        return

    row = state_row.iloc[0]
    _render_profile_grid(row["state"], row, row)


def render_national_profile(df: pd.DataFrame) -> None:
    """Show national average dimension scores and indicators for all states."""
    _render_profile_grid(
        "National average",
        national_dimension_means(df),
        national_indicator_means(df),
    )
