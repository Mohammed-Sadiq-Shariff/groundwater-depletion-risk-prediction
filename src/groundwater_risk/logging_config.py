"""Logging setup for project scripts and future application components."""

from __future__ import annotations

import logging
import os


def configure_logging(level: str | None = None) -> None:
    """Configure a concise root logger without writing log files."""
    resolved_level = (level or os.getenv("GROUNDWATER_RISK_LOG_LEVEL", "INFO")).upper()
    logging.basicConfig(
        level=resolved_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        force=True,
    )

