# AI-Based Groundwater Depletion Risk Prediction

## Mysuru District, Karnataka

This project will develop a reproducible machine-learning workflow to assess groundwater depletion risk in Mysuru District, Karnataka. It will bring together rainfall and groundwater-level data, derive defensible features, and produce Low, Medium, and High risk classifications for appropriate geographic units.

## Problem and objective

Groundwater availability can be affected by rainfall variability and observed groundwater-level change. The project objective is to build and evaluate a data-driven prediction system only after real, documented datasets have been acquired, validated, and inspected.

## Planned data sources

The anticipated inputs are rainfall records, groundwater-level observations, and geographic boundary or location data needed for map visualisation. Exact sources, coverage, licenses, spatial units, and field definitions are **not yet confirmed**.

## Planned workflow

1. Acquire and document real source data.
2. Validate, clean, and merge compatible observations.
3. Explore the data and engineer time, rainfall, groundwater, and spatial features.
4. Establish baseline models, compare candidates, and evaluate with an appropriate validation strategy.
5. Define risk classes from a documented, data-supported policy.
6. Produce GIS/map outputs and a user-facing prediction interface.

## Planned outputs

- A predicted groundwater-depletion risk class: Low, Medium, or High.
- Visualisations and GIS-ready map outputs, subject to available geographic data.
- Reproducible code, tests, data documentation, and a future model card.

## Current status

**Phase 1 — project setup.** No rainfall, groundwater, GIS, or other project datasets have been acquired. No model has been trained, evaluated, or claimed accurate. See [the project plan](docs/project_plan.md) for the planned phases.

## Repository layout

`data/` holds local data stages; `src/` holds application code; `notebooks/` supports documented analysis; `tests/` holds automated checks; `docs/` contains methodology and project documentation.

## Getting started later

After Phase 2 data acquisition, create an isolated Python environment and install dependencies from `requirements.txt`. Do not treat the listed packages as installed by this repository.

