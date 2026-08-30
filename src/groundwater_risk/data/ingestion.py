"""Interfaces for loading documented source datasets."""

from pathlib import Path


def load_source_data(source_path: Path) -> None:
    """Load a confirmed source dataset.

    TODO: Select readers only after the acquired data format and schema are known.
    """
    raise NotImplementedError("Data ingestion awaits confirmed source datasets.")

