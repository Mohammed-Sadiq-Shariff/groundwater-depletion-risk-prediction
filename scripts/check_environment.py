"""Report local environment readiness without installing or changing anything."""

from __future__ import annotations

import importlib.util
import platform
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ("pandas", "numpy", "sklearn", "geopandas", "streamlit", "pytest")
DIRECTORIES = (
    "data/raw/rainfall",
    "data/raw/groundwater",
    "data/interim",
    "data/processed",
    "data/metadata",
    "notebooks",
    "src",
    "tests",
    "models",
    "reports/figures",
    "reports/results",
    "docs",
)


def main() -> None:
    """Print environment and directory availability."""
    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {platform.platform()}")
    print(f"Workspace: {PROJECT_ROOT}")
    print("Package availability:")
    for package in PACKAGES:
        print(f"  {package}: {'available' if importlib.util.find_spec(package) else 'unavailable'}")
    print("Expected directories:")
    for relative_path in DIRECTORIES:
        print(f"  {relative_path}: {'present' if (PROJECT_ROOT / relative_path).is_dir() else 'missing'}")


if __name__ == "__main__":
    main()

