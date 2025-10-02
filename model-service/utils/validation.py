"""Data validation utilities shared across services."""

import pandas as pd
from typing import Dict, List, Optional


def validate_dataframe_schema(df: pd.DataFrame, required_columns: List[str]) -> bool:
    """Validate that DataFrame contains required columns."""
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    return True


def validate_numeric_range(value: float, min_val: Optional[float] = None,
                          max_val: Optional[float] = None) -> bool:
    """Validate that numeric value is within specified range."""
    if min_val is not None and value < min_val:
        raise ValueError(f"Value {value} below minimum {min_val}")
    if max_val is not None and value > max_val:
        raise ValueError(f"Value {value} above maximum {max_val}")
    return True


def sanitize_input_data(data: Dict) -> Dict:
    """Sanitize input data by removing null values and normalizing keys."""
    sanitized = {}
    for key, value in data.items():
        if value is not None:
            sanitized[key.lower().strip()] = value
    return sanitized
