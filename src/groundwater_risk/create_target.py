import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "mysore_model_features.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "mysore_training_dataset.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("\n" + "=" * 60)
print("LOADING MODEL FEATURE DATA")
print("=" * 60)

df = pd.read_csv(INPUT_FILE)

print(f"\nRecords loaded: {len(df)}")
print(f"Columns: {len(df.columns)}")


# ============================================================
# CONVERT DATE
# ============================================================

print("\nConverting monitoring dates...")

df["Monitoring Date"] = pd.to_datetime(
    df["Monitoring Date"],
    errors="coerce"
)

invalid_dates = df["Monitoring Date"].isna().sum()

print(f"Invalid dates: {invalid_dates}")

df = df.dropna(subset=["Monitoring Date"]).copy()


# ============================================================
# SORT DATA
# ============================================================

print("\nSorting data by station and date...")

df = df.sort_values(
    ["Station", "Monitoring Date"]
).reset_index(drop=True)


# ============================================================
# CREATE NEXT GROUNDWATER LEVEL TARGET
# ============================================================

print("\nCreating future groundwater prediction target...")

df["next_groundwater_level"] = (
    df.groupby("Station")["groundwater_level_m"]
    .shift(-1)
)


# ============================================================
# CREATE GROUNDWATER CHANGE TARGET
# ============================================================

print("\nCreating groundwater change target...")

df["next_groundwater_change"] = (
    df["next_groundwater_level"]
    - df["groundwater_level_m"]
)


# ============================================================
# CALCULATE DAYS UNTIL NEXT OBSERVATION
# ============================================================

print("\nCalculating prediction horizon...")

df["next_monitoring_date"] = (
    df.groupby("Station")["Monitoring Date"]
    .shift(-1)
)

df["days_to_next_observation"] = (
    df["next_monitoring_date"]
    - df["Monitoring Date"]
).dt.days


# ============================================================
# REMOVE RECORDS WITHOUT FUTURE TARGET
# ============================================================

print("\nRemoving records without a future observation...")

rows_before = len(df)

df = df.dropna(
    subset=[
        "next_groundwater_level",
        "next_groundwater_change",
        "days_to_next_observation"
    ]
).copy()

rows_removed = rows_before - len(df)

print(f"Rows before target cleaning: {rows_before}")
print(f"Rows removed: {rows_removed}")
print(f"Final training records: {len(df)}")


# ============================================================
# REMOVE INVALID TIME GAPS
# ============================================================

print("\nChecking time gaps between observations...")

print("\nPrediction horizon summary (days):")

print(
    df["days_to_next_observation"]
    .describe()
)
# ============================================================
# FILTER UNREALISTIC PREDICTION HORIZONS
# ============================================================

print("\nFiltering irregular prediction horizons...")

rows_before_horizon_filter = len(df)

MIN_HORIZON_DAYS = 30
MAX_HORIZON_DAYS = 200

df = df[
    (df["days_to_next_observation"] >= MIN_HORIZON_DAYS)
    & (df["days_to_next_observation"] <= MAX_HORIZON_DAYS)
].copy()

rows_removed_horizon = rows_before_horizon_filter - len(df)

print(
    f"Prediction horizon kept: "
    f"{MIN_HORIZON_DAYS} to {MAX_HORIZON_DAYS} days"
)

print(f"Rows removed due to irregular gaps: {rows_removed_horizon}")
print(f"Records remaining: {len(df)}")

print("\nPrediction horizon after filtering:")

print(
    df["days_to_next_observation"]
    .describe()
)

# ============================================================
# CREATE DEPLETION DIRECTION
# ============================================================

# IMPORTANT:
# Groundwater level is measured as depth below ground level.
#
# Higher value = water table deeper = worse groundwater condition.
#
# Therefore:
# Positive change = depletion
# Negative change = recovery

df["depletion_direction"] = (
    df["next_groundwater_change"] > 0
).astype(int)


# ============================================================
# CREATE DEPLETION SEVERITY LABEL
# ============================================================

def classify_depletion(change):

    if change <= 0:
        return "No Depletion"

    elif change <= 1:
        return "Low"

    elif change <= 3:
        return "Moderate"

    else:
        return "High"


df["depletion_risk"] = (
    df["next_groundwater_change"]
    .apply(classify_depletion)
)


# ============================================================
# FINAL DATA CLEANING
# ============================================================

print("\nFinal data cleaning...")

df = df.replace(
    [float("inf"), float("-inf")],
    pd.NA
)


# ============================================================
# DIAGNOSTICS
# ============================================================

print("\n" + "=" * 60)
print("TARGET DATASET DIAGNOSTICS")
print("=" * 60)

print(f"\nFinal training records: {len(df)}")

print(
    f"\nDate range:\n"
    f"{df['Monitoring Date'].min()} "
    f"to "
    f"{df['Monitoring Date'].max()}"
)

print(f"\nUnique stations: {df['Station'].nunique()}")


print("\nNEXT GROUNDWATER LEVEL SUMMARY:")

print(
    df["next_groundwater_level"]
    .describe()
)


print("\nGROUNDWATER CHANGE SUMMARY:")

print(
    df["next_groundwater_change"]
    .describe()
)


print("\nPREDICTION HORIZON SUMMARY (DAYS):")

print(
    df["days_to_next_observation"]
    .describe()
)


print("\nDEPLETION DIRECTION COUNTS:")

print(
    df["depletion_direction"]
    .value_counts()
)


print("\nDEPLETION RISK DISTRIBUTION:")

print(
    df["depletion_risk"]
    .value_counts()
)


# ============================================================
# SAVE DATASET
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\n" + "=" * 60)
print("TARGET DATASET CREATED SUCCESSFULLY")
print("=" * 60)

print(f"\nOutput file:\n{OUTPUT_FILE}")

print(f"\nFinal dataset shape: {df.shape}")

print("\nSample:")

print(
    df[
        [
            "Station",
            "Monitoring Date",
            "groundwater_level_m",
            "next_groundwater_level",
            "next_groundwater_change",
            "days_to_next_observation",
            "depletion_direction",
            "depletion_risk"
        ]
    ]
    .head(10)
)


print("\n" + "=" * 60)