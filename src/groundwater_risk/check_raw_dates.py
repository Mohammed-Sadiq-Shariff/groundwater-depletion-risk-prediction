from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

FILES = [
    PROJECT_ROOT
    / "data"
    / "raw"
    / "groundwater"
    / "gwl_manual_quarterly_cgwb_ka_1991_2020.csv",

    PROJECT_ROOT
    / "data"
    / "raw"
    / "groundwater"
    / "groundwater_karnataka_2021_2025.csv",
]


for file_path in FILES:

    print("\n" + "=" * 80)
    print(file_path.name)
    print("=" * 80)

    df = pd.read_csv(file_path)

    # Keep Mysore records only
    mysore = df[
        df["District"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("mysore")
    ].copy()

    print("\nMysore records:", len(mysore))

    print("\nData Acquisition Time dtype:")
    print(mysore["Data Acquisition Time"].dtype)

    print("\nFirst 30 raw date values:")
    print(
        mysore["Data Acquisition Time"]
        .head(30)
        .to_string(index=False)
    )

    print("\nMissing raw date values:")
    print(
        mysore["Data Acquisition Time"]
        .isna()
        .sum()
    )

    # Parse explicitly as day-month-year
    parsed_dates = pd.to_datetime(
        mysore["Data Acquisition Time"],
        dayfirst=True,
        errors="coerce"
    )

    print("\nInvalid dates after dayfirst=True:")
    print(parsed_dates.isna().sum())

    print("\nParsed records by month:")
    print(
        parsed_dates
        .dt.month
        .value_counts()
        .sort_index()
    )

    print("\nParsed date range:")
    print(
        parsed_dates.min(),
        "to",
        parsed_dates.max()
    )