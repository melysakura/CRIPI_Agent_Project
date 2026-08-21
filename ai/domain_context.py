"""Plain-language definitions of IPCC dimensions and indicators for the AI agent."""

INDICATOR_GLOSSARY = """
IPCC DIMENSIONS (adapted for investment prioritization in Mexico):

- Hazard: Climate-related events that may negatively affect people, infrastructure, and ecosystems.
- Exposure: Populations, infrastructure, and economic assets that could be affected by climate hazards.
- Sensitivity: Socioeconomic characteristics that increase susceptibility to climate impacts.
- Adaptive Capacity: Ability of communities and institutions to prepare for, respond to, and recover from climate impacts.

INDICATOR DEFINITIONS:

Hazard indicators:
- flood_hazard_index: Flood hazard exposure (1–5 scale, higher = greater hazard).
- cyclone_hazard_index: Tropical cyclone hazard exposure (1–5 scale).
- drought_hazard_index: Drought hazard exposure (1–5 scale).
- hazard_dimension_index: Composite hazard score (0–100, higher = greater hazard).

Exposure indicators:
- population_density: Population concentration potentially exposed to hazards (inhabitants/km²).
- agricultural_land_share: Share of state area used for agriculture (%).
- exposure_dimension_index: Composite exposure score (0–100, higher = greater exposure).

Sensitivity indicators:
- multidimensional_poverty: Share of population in multidimensional poverty (%).
- marginalization_score: Territorial structural disadvantage index.
- employment_primary_sector: Employment in agriculture, forestry, livestock, and fisheries (%).
- sensitivity_dimension_index: Composite sensitivity score (0–100, higher = greater sensitivity).

Adaptive Capacity indicators:
- educational_attainment: Average years of schooling for population aged 15+.
- access_piped_water: Households with access to piped water (%).
- access_drainage: Households with access to drainage (%).
- health_service_affiliation: Population affiliated with health services (%).
- adaptive_capacity_dimension_index: Composite adaptive-capacity score (0–100; higher = lower capacity).

COMPOSITE INDEX:
- cripi: Climate Resilience Investment Priority Index (0–100). Higher values indicate greater
  climate vulnerability and higher investment priority.
- investment_priority_category: Low Priority, Moderate Priority, High Priority, or Very High Priority.

IMPORTANT:
- The dataset covers Mexico's 32 federal entities (states).
- Results support strategic planning; they are not definitive funding recommendations.
"""
