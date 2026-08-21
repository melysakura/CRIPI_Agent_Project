"""Metadata for the 12 climate resilience indicators shown in the dashboard."""

from ai.data_loader import DIMENSION_COLUMNS
from components.formatting import format_number

# Label, unit, and dimension for each indicator column in the dataset.
INDICATOR_CATALOG = {
    "flood_hazard_index": {
        "label": "Flood hazard",
        "dimension": "hazard",
        "unit": "1–5 scale",
        "source": "CENAPRED 2020",
        "higher_is_worse": True,
    },
    "cyclone_hazard_index": {
        "label": "Cyclone hazard",
        "dimension": "hazard",
        "unit": "1–5 scale",
        "source": "CENAPRED 2020",
        "higher_is_worse": True,
    },
    "drought_hazard_index": {
        "label": "Drought hazard",
        "dimension": "hazard",
        "unit": "1–5 scale",
        "source": "CENAPRED 2020",
        "higher_is_worse": True,
    },
    "population_density": {
        "label": "Population density",
        "dimension": "exposure",
        "unit": "inhabitants/km²",
        "source": "INEGI 2020",
        "higher_is_worse": True,
    },
    "agricultural_land_share": {
        "label": "Agricultural land share",
        "dimension": "exposure",
        "unit": "% of state area",
        "source": "INEGI 2022",
        "higher_is_worse": True,
    },
    "multidimensional_poverty": {
        "label": "Multidimensional poverty",
        "dimension": "sensitivity",
        "unit": "% of population",
        "source": "CONEVAL",
        "higher_is_worse": True,
    },
    "marginalization_score": {
        "label": "Marginalization score",
        "dimension": "sensitivity",
        "unit": "index",
        "source": "CONAPO",
        "higher_is_worse": True,
    },
    "employment_primary_sector": {
        "label": "Employment in primary sector",
        "dimension": "sensitivity",
        "unit": "% of employment",
        "source": "INEGI ENOE 2025",
        "higher_is_worse": True,
    },
    "educational_attainment": {
        "label": "Educational attainment",
        "dimension": "adaptive_capacity",
        "unit": "years of schooling (15+)",
        "source": "INEGI 2020",
        "higher_is_worse": False,
    },
    "access_piped_water": {
        "label": "Access to piped water",
        "dimension": "adaptive_capacity",
        "unit": "% of households",
        "source": "INEGI 2020",
        "higher_is_worse": False,
    },
    "access_drainage": {
        "label": "Access to drainage",
        "dimension": "adaptive_capacity",
        "unit": "% of households",
        "source": "INEGI 2020",
        "higher_is_worse": False,
    },
    "health_service_affiliation": {
        "label": "Health service affiliation",
        "dimension": "adaptive_capacity",
        "unit": "% of population",
        "source": "INEGI 2020",
        "higher_is_worse": False,
    },
}


def indicator_columns_for_dimension(dimension_key: str) -> list[str]:
    """Return indicator columns for one dimension (without the dimension index)."""
    columns = DIMENSION_COLUMNS[dimension_key]
    return [column for column in columns if not column.endswith("_dimension_index")]


def plain_indicator_value(column: str, value: float) -> str:
    """Return only the numeric value as text, without units."""
    return format_number(value)


def format_indicator_value(column: str, value: float) -> str:
    """Return a formatted value with unit (used by the AI tools)."""
    plain_value = plain_indicator_value(column, value)
    unit = INDICATOR_CATALOG[column]["unit"]
    if "%" in unit:
        return f"{plain_value}%"
    if "years" in unit:
        return f"{plain_value} yrs"
    return plain_value
