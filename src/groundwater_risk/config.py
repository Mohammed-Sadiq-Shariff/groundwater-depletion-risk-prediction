"""Project configuration and environment-safe paths."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _path_from_environment(variable: str, default: Path) -> Path:
    """Return an absolute path from an optional environment variable."""
    value = os.getenv(variable)
    if not value:
        return default
    candidate = Path(value).expanduser()
    return candidate if candidate.is_absolute() else PROJECT_ROOT / candidate


@dataclass(frozen=True)
class ProjectPaths:
    """Canonical project paths, expressed with pathlib for Windows compatibility."""

    root: Path = PROJECT_ROOT
    data: Path = _path_from_environment("GROUNDWATER_RISK_DATA_DIR", PROJECT_ROOT / "data")

    @property
    def raw_data(self) -> Path:
        """Return the raw-data directory."""
        return self.data / "raw"

    @property
    def interim_data(self) -> Path:
        """Return the interim-data directory."""
        return self.data / "interim"

    @property
    def processed_data(self) -> Path:
        """Return the processed-data directory."""
        return self.data / "processed"


PATHS = ProjectPaths()

