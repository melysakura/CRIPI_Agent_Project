"""Helper functions for cluster analysis on Page 2."""

import numpy as np
import pandas as pd

from components.indicator_catalog import INDICATOR_CATALOG, indicator_columns_for_dimension
from components.formatting import format_number

DIMENSION_FEATURE_COLUMNS = [
    "hazard_dimension_index",
    "exposure_dimension_index",
    "sensitivity_dimension_index",
    "adaptive_capacity_dimension_index",
]

INDICATOR_COLUMNS = list(INDICATOR_CATALOG.keys())

CLUSTER_SUMMARIES = {
    1: "Southern high-sensitivity profile",
    2: "Northern and lower-priority states",
    3: "Central mixed vulnerability",
    4: "Gulf and southern transition states",
}


def add_pca_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """Add PC1 and PC2 columns using PCA on the four dimension indices."""
    features = df[DIMENSION_FEATURE_COLUMNS].values.astype(float)
    centered = features - features.mean(axis=0)
    _, singular_values, components = np.linalg.svd(centered, full_matrices=False)

    result = df.copy()
    result["pc1"] = centered @ components[0]
    result["pc2"] = centered @ components[1]

    total_variance = (singular_values**2).sum()
    if total_variance > 0:
        result.attrs["pc1_variance_pct"] = 100 * (singular_values[0] ** 2) / total_variance
        result.attrs["pc2_variance_pct"] = 100 * (singular_values[1] ** 2) / total_variance
    else:
        result.attrs["pc1_variance_pct"] = 0.0
        result.attrs["pc2_variance_pct"] = 0.0

    return result


def pca_axis_labels(df: pd.DataFrame) -> tuple[str, str]:
    """Return axis labels with explained variance percentages."""
    pc1_pct = df.attrs.get("pc1_variance_pct", 0.0)
    pc2_pct = df.attrs.get("pc2_variance_pct", 0.0)
    return (
        f"Principal Component 1 ({format_number(pc1_pct)}% variance)",
        f"Principal Component 2 ({format_number(pc2_pct)}% variance)",
    )


def national_indicator_means(df: pd.DataFrame) -> pd.Series:
    """Return the national mean for each of the 12 indicators."""
    return df[INDICATOR_COLUMNS].mean()


def national_dimension_means(df: pd.DataFrame) -> pd.Series:
    """Return the national mean for each dimension index."""
    return df[DIMENSION_FEATURE_COLUMNS].mean()


def cluster_member_states(df: pd.DataFrame, cluster_id: int) -> list[str]:
    """Return state names belonging to one cluster."""
    return df.loc[df["cluster"] == cluster_id, "state"].sort_values().tolist()


def cluster_indicator_means(df: pd.DataFrame, cluster_id: int) -> pd.Series:
    """Return mean indicator values for one cluster."""
    members = df[df["cluster"] == cluster_id]
    return members[INDICATOR_COLUMNS].mean()


def cluster_dimension_means(df: pd.DataFrame, cluster_id: int) -> pd.Series:
    """Return mean dimension index values for one cluster."""
    members = df[df["cluster"] == cluster_id]
    return members[DIMENSION_FEATURE_COLUMNS].mean()


def indicator_delta_table(
    df: pd.DataFrame, cluster_id: int
) -> pd.DataFrame:
    """Build a table comparing cluster means to national means."""
    cluster_means = cluster_indicator_means(df, cluster_id)
    national_means = national_indicator_means(df)

    rows = []
    for column in INDICATOR_COLUMNS:
        meta = INDICATOR_CATALOG[column]
        cluster_value = cluster_means[column]
        national_value = national_means[column]
        delta = cluster_value - national_value
        rows.append(
            {
                "Indicator": meta["label"],
                "Dimension": meta["dimension"].replace("_", " ").title(),
                "Cluster mean": cluster_value,
                "National mean": national_value,
                "Delta": delta,
                "column": column,
            }
        )

    table = pd.DataFrame(rows)
    table["Abs delta"] = table["Delta"].abs()
    return table.sort_values("Abs delta", ascending=False).drop(columns="Abs delta")


def indicator_delta_table_for_dimension(
    df: pd.DataFrame, cluster_id: int, dimension_key: str
) -> tuple[pd.DataFrame, str | None]:
    """Build a delta table for one dimension and return the top distinctive indicator."""
    cluster_means = cluster_indicator_means(df, cluster_id)
    national_means = national_indicator_means(df)

    rows = []
    for column in indicator_columns_for_dimension(dimension_key):
        meta = INDICATOR_CATALOG[column]
        cluster_value = cluster_means[column]
        national_value = national_means[column]
        delta = cluster_value - national_value
        rows.append(
            {
                "Indicator": meta["label"],
                "Cluster mean": cluster_value,
                "National mean": national_value,
                "Delta": delta,
                "column": column,
            }
        )

    table = pd.DataFrame(rows)
    if table.empty:
        return table, None

    table["Abs delta"] = table["Delta"].abs()
    table = table.sort_values("Abs delta", ascending=False).drop(columns="Abs delta").reset_index(drop=True)
    return table, table.iloc[0]["column"]


def format_profile_value(column: str, value: float) -> str:
    """Format an indicator value with its unit for tables."""
    meta = INDICATOR_CATALOG[column]
    unit = meta["unit"]
    formatted = format_number(value)
    if "years" in unit:
        return f"{formatted} yrs"
    if "%" in unit:
        return f"{formatted}%"
    return formatted


def format_delta_value(column: str, delta: float) -> str:
    """Format the difference between cluster and national means."""
    unit = INDICATOR_CATALOG[column]["unit"]
    sign = "+" if delta >= 0 else ""
    formatted = format_number(delta)
    if "%" in unit:
        return f"{sign}{formatted} pp"
    if "years" in unit:
        return f"{sign}{formatted} yrs"
    return f"{sign}{formatted}"
