"""Load and prepare the CRIPI dashboard dataset from CSV."""

from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "climate_resilience_dashboard.csv"

# Original CSV column names mapped to simple snake_case names.
COLUMN_RENAME = {
    "State Code": "state_code",
    "State": "state",
    "Climate Resilience Investment Priority Index (0–100)": "cripi",
    "Investment Priority Rank": "investment_priority_rank",
    "Investment Priority Category": "investment_priority_category",
    "Cluster": "cluster",
    "Hazard Dimension Index (0–100)": "hazard_dimension_index",
    "Exposure Dimension Index (0–100)": "exposure_dimension_index",
    "Sensitivity Dimension Index (0–100)": "sensitivity_dimension_index",
    "Adaptive Capacity Dimension Index (0–100)": "adaptive_capacity_dimension_index",
    "Flood Hazard Index (1–5 scale)": "flood_hazard_index",
    "Cyclone Hazard Index (1–5 scale)": "cyclone_hazard_index",
    "Drought Hazard Index (1–5 scale)": "drought_hazard_index",
    "Population Density (inhabitants/km²)": "population_density",
    "Agricultural Land Share (% of state area)": "agricultural_land_share",
    "Multidimensional Poverty (% of population)": "multidimensional_poverty",
    "Marginalization Score": "marginalization_score",
    "Employment in Primary Sector (% of employment)": "employment_primary_sector",
    "Educational Attainment (average years of schooling, age 15+)": "educational_attainment",
    "Access to Piped Water (% of households)": "access_piped_water",
    "Access to Drainage (% of households)": "access_drainage",
    "Health Service Affiliation (% of population)": "health_service_affiliation",
}

# Group dataset columns by IPCC-inspired dimension.
DIMENSION_COLUMNS = {
    "hazard": [
        "hazard_dimension_index",
        "flood_hazard_index",
        "cyclone_hazard_index",
        "drought_hazard_index",
    ],
    "exposure": [
        "exposure_dimension_index",
        "population_density",
        "agricultural_land_share",
    ],
    "sensitivity": [
        "sensitivity_dimension_index",
        "multidimensional_poverty",
        "marginalization_score",
        "employment_primary_sector",
    ],
    "adaptive_capacity": [
        "adaptive_capacity_dimension_index",
        "educational_attainment",
        "access_piped_water",
        "access_drainage",
        "health_service_affiliation",
    ],
}

PRIORITY_CATEGORIES = [
    "Low Priority",
    "Moderate Priority",
    "High Priority",
    "Very High Priority",
]


def _read_cripi_dataframe() -> pd.DataFrame:
    """Read the CSV file and return a cleaned dataframe."""
    df = pd.read_csv(DATA_PATH, dtype={"State Code": str})
    df = df.rename(columns=COLUMN_RENAME)
    df["state_code"] = df["state_code"].str.zfill(2)
    return df


@st.cache_data
def load_cripi_data() -> pd.DataFrame:
    """Load the dashboard dataset and cache it for faster Streamlit reruns."""
    return _read_cripi_dataframe()


def resolve_columns(columns: list[str] | None) -> list[str]:
    """Turn user-friendly column names into real dataframe column names."""
    if not columns:
        return list(load_cripi_data().columns)

    df = load_cripi_data()
    resolved = []
    for column in columns:
        key = column.strip().lower().replace(" ", "_")
        if key in DIMENSION_COLUMNS:
            resolved.extend(DIMENSION_COLUMNS[key])
            continue
        if key in df.columns:
            resolved.append(key)
            continue
        matches = [col for col in df.columns if key in col]
        if len(matches) == 1:
            resolved.append(matches[0])
        elif len(matches) > 1:
            resolved.extend(matches)
    return list(dict.fromkeys(resolved))
