"""Interfaces for transparent baseline models."""


def build_baseline() -> None:
    """Construct a baseline only after target and split strategy are confirmed.

    TODO: Select an appropriate baseline from inspected data.
    """
    raise NotImplementedError("Baseline design awaits data inspection.")

