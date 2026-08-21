"""Shared colors and labels used across the CRIPI dashboard charts."""

# Page background and text colors.
PAGE_BG = "#F5F0E8"
DARK_BLUE = "#1A365D"
CHART_BLUE = "#2B6CB0"
LIGHT_BLUE = "#D9EAF7"
CARD_BLUE = "#E8F4FC"
BORDER_BLUE = "#1A365D"
MUTED_MAP_COLOR = "#E2DDD6"

# Traffic-light palette from project design (low → very high priority).
PRIORITY_COLORS = {
    "Low Priority": "#A4C639",
    "Moderate Priority": "#F1C40F",
    "High Priority": "#F39C12",
    "Very High Priority": "#E74C3C",
}

PRIORITY_ORDER = [
    "Very High Priority",
    "High Priority",
    "Moderate Priority",
    "Low Priority",
]

NOT_SELECTED_LABEL = "Not selected"

# Bar chart color for top-state dimension charts.
CHART_ACCENT = CHART_BLUE

# Gap chart colors (very high vs low groups).
GAP_HIGH_COLOR = PRIORITY_COLORS["Very High Priority"]
GAP_LOW_COLOR = PRIORITY_COLORS["Low Priority"]

# Cluster colors for Page 2 scatter plots and profiles.
CLUSTER_COLORS = {
    1: "#E74C3C",
    2: "#3498DB",
    3: "#9B59B6",
    4: "#16A085",
}

NATIONAL_BENCHMARK_COLOR = "#94A3B8"
CLUSTER_MEAN_COLOR = CHART_BLUE

DIMENSIONS = [
    {
        "key": "hazard",
        "label": "Hazard",
        "emoji": "⚠️",
        "index_column": "hazard_dimension_index",
    },
    {
        "key": "exposure",
        "label": "Exposure",
        "emoji": "🏙️",
        "index_column": "exposure_dimension_index",
    },
    {
        "key": "sensitivity",
        "label": "Sensitivity",
        "emoji": "🏚️",
        "index_column": "sensitivity_dimension_index",
    },
    {
        "key": "adaptive_capacity",
        "label": "Adaptive Capacity",
        "emoji": "🛡️",
        "index_column": "adaptive_capacity_dimension_index",
    },
]

DIMENSION_INDEX_LABELS = {
    "hazard_dimension_index": "Hazard",
    "exposure_dimension_index": "Exposure",
    "sensitivity_dimension_index": "Sensitivity",
    "adaptive_capacity_dimension_index": "Adaptive Capacity Gap",
}


def apply_chart_theme(fig, height=320):
    """Apply the beige background and dark blue text style to a Plotly chart."""
    fig.update_layout(
        height=height,
        paper_bgcolor=PAGE_BG,
        plot_bgcolor=PAGE_BG,
        font={"color": DARK_BLUE},
        title_font={"color": DARK_BLUE, "size": 17},
        legend_font={"color": DARK_BLUE},
    )
    fig.update_xaxes(gridcolor="#E0D6C8", zerolinecolor="#E0D6C8")
    fig.update_yaxes(gridcolor="#E0D6C8", zerolinecolor="#E0D6C8")
    return fig
