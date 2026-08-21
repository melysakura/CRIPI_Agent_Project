"""Mexico choropleth map colored by investment priority category."""

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from components.theme import (
    MUTED_MAP_COLOR,
    NOT_SELECTED_LABEL,
    PAGE_BG,
    PRIORITY_COLORS,
    PRIORITY_ORDER,
    apply_chart_theme,
)

GEOJSON_PATH = Path(__file__).resolve().parents[2] / "data" / "geo" / "mexico_states.geojson"


@st.cache_data
def _load_geojson() -> dict:
    """Load the GeoJSON file with Mexico state boundaries."""
    with GEOJSON_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def _prepare_map_colors(map_df: pd.DataFrame, focus_state: str | None) -> tuple[pd.DataFrame, dict, list]:
    """Build map color column and legend settings for overview or focus mode."""
    if focus_state:
        map_df["map_category"] = map_df.apply(
            lambda row: row["investment_priority_category"]
            if row["state"] == focus_state
            else NOT_SELECTED_LABEL,
            axis=1,
        )
        color_map = {**PRIORITY_COLORS, NOT_SELECTED_LABEL: MUTED_MAP_COLOR}
        category_order = PRIORITY_ORDER + [NOT_SELECTED_LABEL]
        return map_df, color_map, category_order

    map_df["map_category"] = map_df["investment_priority_category"]
    return map_df, PRIORITY_COLORS, PRIORITY_ORDER


def render_mexico_map(df: pd.DataFrame, focus_state: str | None = None) -> None:
    """Draw a map of Mexico. Highlight one state when focus_state is provided."""
    map_df = df.copy()
    map_df["state_code"] = map_df["state_code"].astype(str).str.zfill(2)
    map_df, color_map, category_order = _prepare_map_colors(map_df, focus_state)

    fig = px.choropleth(
        map_df,
        geojson=_load_geojson(),
        locations="state_code",
        featureidkey="properties.state_code",
        color="map_category",
        category_orders={"map_category": category_order},
        color_discrete_map=color_map,
        hover_name="state",
        hover_data={
            "cripi": ":.1f",
            "investment_priority_rank": True,
            "investment_priority_category": True,
            "state_code": False,
            "map_category": False,
        },
        labels={
            "map_category": "Priority",
            "cripi": "CRIPI",
            "investment_priority_rank": "Rank",
            "investment_priority_category": "Priority category",
        },
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        bgcolor=PAGE_BG,
        lakecolor=PAGE_BG,
        landcolor=PAGE_BG,
    )
    apply_chart_theme(fig, height=580)
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend_title_text="Investment priority",
        paper_bgcolor=PAGE_BG,
        plot_bgcolor=PAGE_BG,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
