"""Shared number formatting for dashboard values."""


def format_number(value: float, decimals: int = 1) -> str:
    """Format a number with a fixed number of decimal places."""
    return f"{round(float(value), decimals):.{decimals}f}"


def round_value(value: float, decimals: int = 1) -> float:
    """Round a numeric value for charts and calculations."""
    return round(float(value), decimals)
