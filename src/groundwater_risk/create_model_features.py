from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "mysore_model_dataset.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "mysore_model_features.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("\n============================================================")
print("LOADING MODEL DATASET")
print("============================================================")

df = pd.read_csv(
    INPUT_PATH,
    low_memory=False
)

print(f"\nRecords loaded: {len(df)}")

print("\nColumns:")
print(df.columns.tolist())


# ============================================================
# CONVERT DATE
# ============================================================

df["Monitoring Date"] = pd.to_datetime(
    df["Monitoring Date"],
    errors="coerce"
)


invalid_dates = df["Monitoring Date"].isna().sum()

print(f"\nInvalid dates: {invalid_dates}")


df = df.dropna(
    subset=[
        "Monitoring Date",
        "groundwater_level_m"
    ]
).copy()


# ============================================================
# SORT DATA
# ============================================================

df = df.sort_values(
    [
        "Station",
        "Monitoring Date"
    ]
).reset_index(drop=True)


# ============================================================
# CREATE GROUNDWATER LAG FEATURES
# ============================================================

print("\n============================================================")
print("CREATING GROUNDWATER LAG FEATURES")
print("============================================================")

station_group = df.groupby("Station")[
    "groundwater_level_m"
]


df["gw_lag_1"] = station_group.shift(1)

df["gw_lag_2"] = station_group.shift(2)

df["gw_lag_3"] = station_group.shift(3)

df["gw_lag_4"] = station_group.shift(4)


# ============================================================
# GROUNDWATER CHANGE FEATURES
# ============================================================

print("\nCreating groundwater change features...")


df["gw_change_1"] = (
    df["groundwater_level_m"]
    - df["gw_lag_1"]
)


df["gw_change_2"] = (
    df["groundwater_level_m"]
    - df["gw_lag_2"]
)


# ============================================================
# ROLLING GROUNDWATER FEATURES
# ============================================================

print("\nCreating rolling groundwater features...")


df["gw_rolling_mean_3"] = (
    df.groupby("Station")[
        "groundwater_level_m"
    ]
    .transform(
        lambda x: x.shift(1).rolling(
            window=3,
            min_periods=1
        ).mean()
    )
)


df["gw_rolling_mean_4"] = (
    df.groupby("Station")[
        "groundwater_level_m"
    ]
    .transform(
        lambda x: x.shift(1).rolling(
            window=4,
            min_periods=1
        ).mean()
    )
)


df["gw_rolling_std_3"] = (
    df.groupby("Station")[
        "groundwater_level_m"
    ]
    .transform(
        lambda x: x.shift(1).rolling(
            window=3,
            min_periods=2
        ).std()
    )
)


# ============================================================
# LONG-TERM STATION FEATURES
# ============================================================

print("\nCreating station historical features...")


df["station_historical_mean"] = (
    df.groupby("Station")[
        "groundwater_level_m"
    ]
    .transform(
        lambda x: x.shift(1).expanding().mean()
    )
)


df["station_historical_std"] = (
    df.groupby("Station")[
        "groundwater_level_m"
    ]
    .transform(
        lambda x: x.shift(1).expanding().std()
    )
)


# ============================================================
# TIME FEATURES
# ============================================================

print("\nCreating time features...")


df["year"] = (
    df["Monitoring Date"].dt.year
)


df["month"] = (
    df["Monitoring Date"].dt.month
)


df["quarter"] = (
    df["Monitoring Date"].dt.quarter
)


# Cyclical representation of month

df["month_sin"] = np.sin(
    2 * np.pi * df["month"] / 12
)

df["month_cos"] = np.cos(
    2 * np.pi * df["month"] / 12
)


# ============================================================
# SEASON LABEL
# ============================================================

season_mapping = {
    1: "January",
    5: "Pre_monsoon",
    8: "Monsoon",
    11: "Post_monsoon"
}


df["season"] = (
    df["month"]
    .map(season_mapping)
)


# ============================================================
# DATA QUALITY CHECK
# ============================================================

print("\n============================================================")
print("FEATURE MISSING VALUES")
print("============================================================")

feature_columns = [
    "gw_lag_1",
    "gw_lag_2",
    "gw_lag_3",
    "gw_lag_4",
    "gw_change_1",
    "gw_change_2",
    "gw_rolling_mean_3",
    "gw_rolling_mean_4",
    "gw_rolling_std_3",
    "station_historical_mean",
    "station_historical_std"
]


print(
    df[feature_columns]
    .isna()
    .sum()
)


# ============================================================
# REMOVE RECORDS WITHOUT SUFFICIENT HISTORY
# ============================================================

print("\n============================================================")
print("REMOVING RECORDS WITHOUT SUFFICIENT HISTORY")
print("============================================================")


initial_rows = len(df)


# Require at least 4 previous observations
df_model = df.dropna(
    subset=[
        "gw_lag_1",
        "gw_lag_2",
        "gw_lag_3",
        "gw_lag_4"
    ]
).copy()


final_rows = len(df_model)


print(f"\nRows before history filtering: {initial_rows}")
print(f"Rows removed: {initial_rows - final_rows}")
print(f"Final model records: {final_rows}")


# ============================================================
# SAVE
# ============================================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


df_model.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# FINAL REPORT
# ============================================================

print("\n============================================================")
print("MODEL FEATURE ENGINEERING COMPLETE")
print("============================================================")


print(f"\nFinal dataset shape: {df_model.shape}")


print("\nDate range:")

print(
    df_model["Monitoring Date"].min(),
    "to",
    df_model["Monitoring Date"].max()
)


print("\nUnique stations:")

print(
    df_model["Station"].nunique()
)


print("\nRecords by month:")

print(
    df_model["month"]
    .value_counts()
    .sort_index()
)


print("\nCreated groundwater features:")

print(
    [
        "gw_lag_1",
        "gw_lag_2",
        "gw_lag_3",
        "gw_lag_4",
        "gw_change_1",
        "gw_change_2",
        "gw_rolling_mean_3",
        "gw_rolling_mean_4",
        "gw_rolling_std_3",
        "station_historical_mean",
        "station_historical_std"
    ]
)


print("\nOutput saved to:")

print(OUTPUT_PATH)


print("\nSample:")

print(
    df_model[
        [
            "Station",
            "Monitoring Date",
            "groundwater_level_m",
            "gw_lag_1",
            "gw_lag_2",
            "gw_lag_3",
            "gw_lag_4",
            "rain_90d",
            "rain_365d"
        ]
    ].head(10)
)