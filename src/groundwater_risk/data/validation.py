"""Interfaces for validating acquired datasets."""

from typing import Any


def validate_dataset(dataset: Any) -> None:
    """Validate a dataset against its confirmed source schema.

    TODO: Define checks for confirmed columns, units, dates, coordinates, and quality flags.
    """
    raise NotImplementedError("Validation rules await data inspection.")

