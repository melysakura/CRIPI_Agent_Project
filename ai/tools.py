"""Tools the AI agent can call to query and summarize CRIPI data."""

import json

import pandas as pd

from ai.data_loader import PRIORITY_CATEGORIES, load_cripi_data, resolve_columns
from components.cluster_utils import (
    CLUSTER_SUMMARIES,
    DIMENSION_FEATURE_COLUMNS,
    INDICATOR_COLUMNS,
    cluster_dimension_means,
    cluster_indicator_means,
    cluster_member_states,
    indicator_delta_table,
    national_dimension_means,
    national_indicator_means,
)
from components.formatting import round_value
from components.indicator_catalog import INDICATOR_CATALOG
from components.theme import DIMENSION_INDEX_LABELS

DIMENSION_ALIASES = ["hazard", "exposure", "sensitivity", "adaptive_capacity"]

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_state_data",
            "description": (
                "Retrieve raw climate resilience data for one or more Mexican states. "
                "Use for specific state lookups or when the user needs exact values."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "states": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "State names (e.g. ['Chiapas']). Partial matches supported. "
                            "Omit to return all states."
                        ),
                    },
                    "columns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "Columns to return, or dimension aliases: "
                            f"{', '.join(DIMENSION_ALIASES)}. Omit for all columns."
                        ),
                    },
                    "priority_category": {
                        "type": "string",
                        "enum": PRIORITY_CATEGORIES,
                        "description": "Optional filter by investment priority category.",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "rank_states",
            "description": (
                "Rank states by CRIPI, a dimension index, or any indicator. "
                "Use for top/bottom comparisons."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "by": {
                        "type": "string",
                        "description": "Column to rank by. Default: cripi.",
                        "default": "cripi",
                    },
                    "top_n": {
                        "type": "integer",
                        "description": "Number of states to return.",
                        "default": 5,
                    },
                    "ascending": {
                        "type": "boolean",
                        "description": "True = lowest first. For cripi use False for highest priority first.",
                        "default": False,
                    },
                    "priority_category": {
                        "type": "string",
                        "enum": PRIORITY_CATEGORIES,
                        "description": "Optional filter before ranking.",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_priority_group",
            "description": (
                "Summarize all states in one investment priority category: member states, "
                "average dimension scores vs national mean, distinctive indicators, and cluster mix. "
                "Use to explain why states in a priority group are similar or what they share."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "priority_category": {
                        "type": "string",
                        "enum": PRIORITY_CATEGORIES,
                        "description": "Priority group to summarize.",
                    },
                },
                "required": ["priority_category"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_cluster_profile",
            "description": (
                "Return cluster membership, average dimension scores, and indicator deltas vs "
                "national mean for one K-Means cluster (1-4). Use for cluster interpretation."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "cluster_id": {
                        "type": "integer",
                        "description": "Cluster number from 1 to 4.",
                        "minimum": 1,
                        "maximum": 4,
                    },
                },
                "required": ["cluster_id"],
            },
        },
    },
]


def _normalize_state_filter(states: list[str] | None) -> pd.DataFrame:
    """Filter the dataset to rows that match one or more state names."""
    df = load_cripi_data()
    if not states:
        return df

    mask = pd.Series(False, index=df.index)
    for state in states:
        mask |= df["state"].str.contains(state, case=False, na=False)
    return df[mask]


def _round_records(df: pd.DataFrame) -> list[dict]:
    """Convert a dataframe to JSON-friendly records with rounded floats."""
    records = []
    for _, row in df.iterrows():
        record = {}
        for column, value in row.items():
            if pd.isna(value):
                record[column] = None
            elif isinstance(value, (float, int)) and column != "cluster" and column != "investment_priority_rank":
                record[column] = round_value(float(value))
            else:
                record[column] = value
        records.append(record)
    return records


def _dataframe_result(title: str, df: pd.DataFrame) -> str:
    """Return tool output as JSON for the LLM to analyze."""
    if df.empty:
        return json.dumps({"title": title, "row_count": 0, "message": "No matching records found."})

    return json.dumps(
        {
            "title": title,
            "row_count": len(df),
            "columns": list(df.columns),
            "rows": _round_records(df),
        },
        ensure_ascii=False,
    )


def _dimension_summary(series: pd.Series, label_map: dict | None = None) -> dict:
    """Build a readable dict of dimension means."""
    label_map = label_map or DIMENSION_INDEX_LABELS
    return {label_map.get(column, column): round_value(series[column]) for column in series.index}


def _top_indicator_deltas(group_means: pd.Series, national_means: pd.Series, limit: int = 5) -> list[dict]:
    """Return indicators with the largest absolute gap from the national mean."""
    rows = []
    for column in INDICATOR_COLUMNS:
        delta = group_means[column] - national_means[column]
        rows.append(
            {
                "indicator": INDICATOR_CATALOG[column]["label"],
                "group_mean": round_value(group_means[column]),
                "national_mean": round_value(national_means[column]),
                "delta": round_value(delta),
                "unit": INDICATOR_CATALOG[column]["unit"],
            }
        )
    rows.sort(key=lambda row: abs(row["delta"]), reverse=True)
    return rows[:limit]


def get_state_data(
    states: list[str] | None = None,
    columns: list[str] | None = None,
    priority_category: str | None = None,
) -> str:
    """Return filtered state data as JSON for the AI agent."""
    df = _normalize_state_filter(states)

    if priority_category:
        df = df[df["investment_priority_category"] == priority_category]

    selected_columns = resolve_columns(columns)
    missing = [col for col in selected_columns if col not in df.columns]
    if missing:
        return json.dumps({"error": f"Unknown columns requested: {', '.join(missing)}"})

    result = df[selected_columns]
    label = "State data"
    if states:
        label += f" for {', '.join(states)}"
    if priority_category:
        label += f" ({priority_category})"

    return _dataframe_result(label, result)


def rank_states(
    by: str = "cripi",
    top_n: int = 5,
    ascending: bool = False,
    priority_category: str | None = None,
) -> str:
    """Return a ranked list of states as JSON for the AI agent."""
    df = load_cripi_data()

    rank_column = by.strip().lower().replace(" ", "_")
    resolved = resolve_columns([rank_column])
    if not resolved:
        return json.dumps({"error": f"Unknown ranking column: {by}"})
    rank_column = resolved[0]

    if priority_category:
        df = df[df["investment_priority_category"] == priority_category]

    ranked = df.sort_values(rank_column, ascending=ascending).head(top_n)
    display_columns = [
        "state",
        "cripi",
        "investment_priority_rank",
        "investment_priority_category",
        rank_column,
    ]
    display_columns = list(dict.fromkeys(col for col in display_columns if col in ranked.columns))
    ranked = ranked[display_columns]

    direction = "lowest" if ascending else "highest"
    title = f"Top {top_n} states by {rank_column} ({direction} first)"
    if priority_category:
        title += f" — {priority_category}"

    return _dataframe_result(title, ranked.reset_index(drop=True))


def summarize_priority_group(priority_category: str) -> str:
    """Return an analytical summary of one priority category vs national benchmarks."""
    df = load_cripi_data()
    group = df[df["investment_priority_category"] == priority_category]
    if group.empty:
        return json.dumps({"error": f"No states found for {priority_category}."})

    group_dim = group[DIMENSION_FEATURE_COLUMNS].mean()
    national_dim = national_dimension_means(df)
    group_ind = group[INDICATOR_COLUMNS].mean()
    national_ind = national_indicator_means(df)

    cluster_counts = group["cluster"].value_counts().sort_index()
    cluster_mix = {f"Cluster {int(cluster)}": int(count) for cluster, count in cluster_counts.items()}

    payload = {
        "priority_category": priority_category,
        "state_count": len(group),
        "states": group.sort_values("cripi", ascending=False)["state"].tolist(),
        "average_cripi": round_value(group["cripi"].mean()),
        "national_average_cripi": round_value(df["cripi"].mean()),
        "dimension_means": _dimension_summary(group_dim),
        "national_dimension_means": _dimension_summary(national_dim),
        "dimension_gaps_vs_national": {
            DIMENSION_INDEX_LABELS[column]: round_value(group_dim[column] - national_dim[column])
            for column in DIMENSION_FEATURE_COLUMNS
        },
        "distinctive_indicators": _top_indicator_deltas(group_ind, national_ind),
        "cluster_mix": cluster_mix,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def get_cluster_profile(cluster_id: int) -> str:
    """Return cluster membership and benchmark comparisons as JSON."""
    df = load_cripi_data()
    if cluster_id not in df["cluster"].unique():
        return json.dumps({"error": f"Cluster {cluster_id} not found. Use clusters 1-4."})

    members = cluster_member_states(df, cluster_id)
    cluster_dim = cluster_dimension_means(df, cluster_id)
    national_dim = national_dimension_means(df)
    cluster_ind = cluster_indicator_means(df, cluster_id)
    national_ind = national_indicator_means(df)

    deltas = indicator_delta_table(df, cluster_id)
    top_deltas = []
    for _, row in deltas.head(5).iterrows():
        column = row["column"]
        top_deltas.append(
            {
                "indicator": row["Indicator"],
                "cluster_mean": round_value(row["Cluster mean"]),
                "national_mean": round_value(row["National mean"]),
                "delta": round_value(row["Delta"]),
                "unit": INDICATOR_CATALOG[column]["unit"],
            }
        )

    priority_mix = (
        df[df["cluster"] == cluster_id]["investment_priority_category"].value_counts().to_dict()
    )

    payload = {
        "cluster_id": cluster_id,
        "profile_label": CLUSTER_SUMMARIES.get(cluster_id, ""),
        "member_states": members,
        "state_count": len(members),
        "average_cripi": round_value(df[df["cluster"] == cluster_id]["cripi"].mean()),
        "dimension_means": _dimension_summary(cluster_dim),
        "national_dimension_means": _dimension_summary(national_dim),
        "distinctive_indicators": _top_indicator_deltas(cluster_ind, national_ind),
        "top_indicator_deltas": top_deltas,
        "priority_category_mix": priority_mix,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)
