from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

GW_OLD_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "groundwater"
    / "gwl_manual_quarterly_cgwb_ka_1991_2020.csv"
)

GW_NEW_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "groundwater"
    / "groundwater_karnataka_2021_2025.csv"
)

RAINFALL_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "mysore_rainfall_1991_2025.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "mysore_model_dataset.csv"
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def parse_groundwater_dates(series):
    """
    Parse CGWB groundwater dates.

    Expected raw format:
    DD-MM-YYYY HH:MM
    """

    series = series.astype(str).str.strip()

    parsed = pd.to_datetime(
        series,
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )

    # Fallback for any date values that do not exactly match
    mask = parsed.isna()

    if mask.any():
        parsed.loc[mask] = pd.to_datetime(
            series.loc[mask],
            dayfirst=True,
            errors="coerce"
        )

    return parsed


# ============================================================
# LOAD AND PREPARE GROUNDWATER DATA
# ============================================================

print("\n============================================================")
print("LOADING GROUNDWATER DATA")
print("============================================================")


def load_groundwater(path):

    print(f"\nLoading: {path.name}")

    df = pd.read_csv(path, low_memory=False)

    print(f"Total records: {len(df)}")

    # Standardise column names
    df.columns = df.columns.str.strip()

    # Filter Mysore district
    district_mask = (
        df["District"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["mysore", "mysuru"])
    )

    df = df[district_mask].copy()

    print(f"Mysore/Mysuru records: {len(df)}")

    # Parse dates directly from raw source
    df["Monitoring Date"] = parse_groundwater_dates(
        df["Data Acquisition Time"]
    )

    invalid_dates = df["Monitoring Date"].isna().sum()

    print(f"Invalid dates: {invalid_dates}")

    # Convert groundwater level
    level_column = "Groundwater Level Quarterly Manual (meter)"

    df["groundwater_level_m"] = pd.to_numeric(
        df[level_column],
        errors="coerce"
    )

    invalid_levels = df["groundwater_level_m"].isna().sum()

    print(f"Missing groundwater levels: {invalid_levels}")

    # Keep required columns
    columns_to_keep = [
        "Station",
        "District",
        "Tehsil",
        "Block",
        "Village",
        "Latitude",
        "Longitude",
        "Monitoring Date",
        "groundwater_level_m"
    ]

    df = df[columns_to_keep].copy()

    return df


gw_old = load_groundwater(GW_OLD_PATH)
gw_new = load_groundwater(GW_NEW_PATH)


# ============================================================
# COMBINE GROUNDWATER DATA
# ============================================================

print("\n============================================================")
print("COMBINING GROUNDWATER DATA")
print("============================================================")

gw = pd.concat(
    [gw_old, gw_new],
    ignore_index=True
)

print(f"\nCombined groundwater records: {len(gw)}")


# Remove invalid dates and groundwater levels
gw = gw.dropna(
    subset=[
        "Monitoring Date",
        "groundwater_level_m"
    ]
).copy()


# Remove impossible groundwater levels
gw = gw[
    gw["groundwater_level_m"] > 0
].copy()


# Sort
gw = gw.sort_values(
    ["Station", "Monitoring Date"]
).reset_index(drop=True)


# ============================================================
# GROUNDWATER DIAGNOSTICS
# ============================================================

print("\n============================================================")
print("GROUNDWATER DATE DIAGNOSTICS")
print("============================================================")

print("\nFinal groundwater records:")
print(len(gw))

print("\nDate range:")
print(
    gw["Monitoring Date"].min(),
    "to",
    gw["Monitoring Date"].max()
)

print("\nRecords by month:")
print(
    gw["Monitoring Date"]
    .dt.month
    .value_counts()
    .sort_index()
)

print("\nRecords by year:")
print(
    gw["Monitoring Date"]
    .dt.year
    .value_counts()
    .sort_index()
)

print("\nUnique stations:")
print(
    gw["Station"].nunique()
)


# ============================================================
# LOAD RAINFALL DATA
# ============================================================

print("\n============================================================")
print("LOADING RAINFALL DATA")
print("============================================================")

rain = pd.read_csv(
    RAINFALL_PATH,
    low_memory=False
)

rain.columns = rain.columns.str.strip()

print(f"\nRainfall records: {len(rain)}")

print("\nRainfall columns:")
print(rain.columns.tolist())


# ============================================================
# CONVERT RAINFALL DATE
# ============================================================

rain["Monitoring Date"] = pd.to_datetime(
    rain["Monitoring Date"],
    format="%Y-%m-%d",
    errors="coerce"
)
rain["Rainfall (MM)"] = pd.to_numeric(
    rain["Rainfall (MM)"],
    errors="coerce"
)

print("\nInvalid rainfall dates:")
print(
    rain["Monitoring Date"].isna().sum()
)


# Remove invalid rows
rain = rain.dropna(
    subset=[
        "Monitoring Date",
        "Rainfall (MM)"
    ]
).copy()


# ============================================================
# AGGREGATE RAINFALL ACROSS MYSORE DISTRICT
# ============================================================

print("\n============================================================")
print("AGGREGATING RAINFALL")
print("============================================================")

daily_rain = (
    rain
    .groupby("Monitoring Date")["Rainfall (MM)"]
    .mean()
    .reset_index()
)

daily_rain = daily_rain.rename(
    columns={
        "Rainfall (MM)": "rainfall_mm"
    }
)

daily_rain = daily_rain.sort_values(
    "Monitoring Date"
).reset_index(drop=True)


print("\nDaily rainfall records:")
print(len(daily_rain))

print("\nRainfall date range:")
print(
    daily_rain["Monitoring Date"].min(),
    "to",
    daily_rain["Monitoring Date"].max()
)


# ============================================================
# CREATE CONTINUOUS DAILY RAINFALL SERIES
# ============================================================

print("\nCreating continuous daily rainfall series...")

full_dates = pd.date_range(
    start=daily_rain["Monitoring Date"].min(),
    end=daily_rain["Monitoring Date"].max(),
    freq="D"
)

daily_rain = (
    daily_rain
    .set_index("Monitoring Date")
    .reindex(full_dates)
)

daily_rain.index.name = "Monitoring Date"


missing_days = daily_rain["rainfall_mm"].isna().sum()

print(f"Missing rainfall dates before filling: {missing_days}")



# Preserve missing rainfall observations.
# Do not assume missing rainfall means zero rainfall.

missing_days = daily_rain["rainfall_mm"].isna().sum()

print(f"Missing rainfall dates: {missing_days}")
print(
    "Missing rainfall date range:",
    daily_rain.index[daily_rain["rainfall_mm"].isna()].min(),
    "to",
    daily_rain.index[daily_rain["rainfall_mm"].isna()].max()
)

# ============================================================
# CREATE RAINFALL FEATURES
# ============================================================

print("\n============================================================")
print("CREATING RAINFALL FEATURES")
print("============================================================")

daily_rain["rain_7d"] = (
    daily_rain["rainfall_mm"]
    .rolling(7, min_periods=1)
    .sum()
)

daily_rain["rain_30d"] = (
    daily_rain["rainfall_mm"]
    .rolling(30, min_periods=1)
    .sum()
)

daily_rain["rain_90d"] = (
    daily_rain["rainfall_mm"]
    .rolling(90, min_periods=1)
    .sum()
)

daily_rain["rain_180d"] = (
    daily_rain["rainfall_mm"]
    .rolling(180, min_periods=1)
    .sum()
)

daily_rain["rain_365d"] = (
    daily_rain["rainfall_mm"]
    .rolling(365, min_periods=1)
    .sum()
)


daily_rain = (
    daily_rain
    .reset_index()
    .rename(
        columns={
            "index": "Monitoring Date"
        }
    )
)


# ============================================================
# ALIGN RAINFALL WITH GROUNDWATER OBSERVATIONS
# ============================================================

print("\n============================================================")
print("ALIGNING RAINFALL WITH GROUNDWATER")
print("============================================================")


gw = gw.sort_values(
    "Monitoring Date"
)

daily_rain = daily_rain.sort_values(
    "Monitoring Date"
)


model_data = pd.merge_asof(
    gw,
    daily_rain[
        [
            "Monitoring Date",
            "rain_7d",
            "rain_30d",
            "rain_90d",
            "rain_180d",
            "rain_365d"
        ]
    ],
    on="Monitoring Date",
    direction="backward"
)


# ============================================================
# FINAL CLEANING
# ============================================================

print("\n============================================================")
print("FINAL DATA CLEANING")
print("============================================================")

model_data = model_data.dropna(
    subset=[
        "groundwater_level_m",
        "rain_7d",
        "rain_30d",
        "rain_90d",
        "rain_180d",
        "rain_365d"
    ]
).copy()


# Remove duplicate station-date records
model_data = model_data.drop_duplicates(
    subset=[
        "Station",
        "Monitoring Date",
        "Latitude",
        "Longitude"
    ]
)


# Sort
model_data = model_data.sort_values(
    ["Station", "Monitoring Date"]
).reset_index(drop=True)


# ============================================================
# ADD TIME FEATURES
# ============================================================

model_data["year"] = (
    model_data["Monitoring Date"].dt.year
)

model_data["month"] = (
    model_data["Monitoring Date"].dt.month
)

model_data["quarter"] = (
    model_data["Monitoring Date"].dt.quarter
)


# ============================================================
# SAVE DATASET
# ============================================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

model_data.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# FINAL REPORT
# ============================================================

print("\n============================================================")
print("FEATURE ENGINEERING COMPLETE")
print("============================================================")

print("\nFinal model records:")
print(len(model_data))

print("\nDate range:")
print(
    model_data["Monitoring Date"].min(),
    "to",
    model_data["Monitoring Date"].max()
)

print("\nUnique groundwater stations:")
print(
    model_data["Station"].nunique()
)

print("\nGroundwater records by month:")

print(
    model_data["Monitoring Date"]
    .dt.month
    .value_counts()
    .sort_index()
)

print("\nRainfall features created:")

print(
    [
        "rain_7d",
        "rain_30d",
        "rain_90d",
        "rain_180d",
        "rain_365d"
    ]
)

print("\nSaved model dataset:")
print(OUTPUT_PATH)

print("\nSample:")

print(
    model_data[
        [
            "Station",
            "Monitoring Date",
            "groundwater_level_m",
            "rain_30d",
            "rain_90d",
            "rain_180d",
            "rain_365d"
        ]
    ].head(10)
)