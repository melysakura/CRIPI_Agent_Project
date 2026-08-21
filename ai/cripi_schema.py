"""Text description of the CRIPI dataset columns for the AI system prompt."""

from ai.data_loader import DIMENSION_COLUMNS, PRIORITY_CATEGORIES, _read_cripi_dataframe

_df = _read_cripi_dataframe()

CRIPI_SCHEMA = f"""
DATASET: climate_resilience_states
DESCRIPTION: State-level climate resilience investment prioritization data for Mexico's 32 federal entities.
ROWS: {_df.shape[0]} (one row per state)

IDENTIFIERS:
- state_code: Two-digit INEGI state code (e.g., "07" for Chiapas)
- state: Official state name

COMPOSITE OUTPUTS:
- cripi: Climate Resilience Investment Priority Index (0–100, higher = higher priority)
- investment_priority_rank: Rank from 1 (highest priority) to 32 (lowest priority)
- investment_priority_category: One of {", ".join(PRIORITY_CATEGORIES)}
- cluster: K-Means cluster assignment (1–4)

DIMENSION INDICES (0–100, higher = greater vulnerability except where noted):
- hazard_dimension_index
- exposure_dimension_index
- sensitivity_dimension_index
- adaptive_capacity_dimension_index

INDICATORS BY DIMENSION:

Hazard:
{chr(10).join(f"  - {col}" for col in DIMENSION_COLUMNS["hazard"])}

Exposure:
{chr(10).join(f"  - {col}" for col in DIMENSION_COLUMNS["exposure"])}

Sensitivity:
{chr(10).join(f"  - {col}" for col in DIMENSION_COLUMNS["sensitivity"])}

Adaptive Capacity:
{chr(10).join(f"  - {col}" for col in DIMENSION_COLUMNS["adaptive_capacity"])}

AVAILABLE STATES:
{", ".join(_df["state"].tolist())}
"""
