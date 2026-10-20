from pathlib import Path
import pandas as pd

INPUT_FILE = Path(
    "data/interim/groundwater/mysore_groundwater_1991_2025.csv"
)

OUTPUT_DIR = Path(
    "data/processed/groundwater"
)

OUTPUT_FILE = OUTPUT_DIR / "mysore_groundwater_cleaned_1996_2024.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Loading interim groundwater dataset...")

df = pd.read_csv(INPUT_FILE)

print("Original shape:", df.shape)

# --------------------------------------------------
# 1. Convert date and groundwater level types
# --------------------------------------------------

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

df["groundwater_level_m"] = pd.to_numeric(
    df["groundwater_level_m"],
    errors="coerce"
)

# --------------------------------------------------
# 2. Standardize source placeholder values
# --------------------------------------------------

administrative_columns = [
    "Tehsil",
    "Block",
    "Village",
    "River",
    "Basin",
    "Tributary",
    "Subtributary",
    "SubSubtributary",
    "Local River"
]

for column in administrative_columns:
    if column in df.columns:
        df[column] = (
            df[column]
            .replace("-", pd.NA)
            .replace(" - ", pd.NA)
        )

# --------------------------------------------------
# 3. Remove rows without the target measurement
# --------------------------------------------------

missing_before = df["groundwater_level_m"].isna().sum()

df_clean = df.dropna(
    subset=[
        "groundwater_level_m"
    ]
).copy()

removed_rows = len(df) - len(df_clean)

# --------------------------------------------------
# 4. Add useful temporal features
# --------------------------------------------------

df_clean["year"] = df_clean["date"].dt.year
df_clean["month"] = df_clean["date"].dt.month

season_map = {
    1: "January",
    5: "Pre-monsoon",
    8: "Monsoon",
    11: "Post-monsoon"
}

df_clean["season"] = (
    df_clean["month"]
    .map(season_map)
)

# --------------------------------------------------
# 5. Sort records
# --------------------------------------------------

df_clean = df_clean.sort_values(
    [
        "station",
        "date"
    ]
).reset_index(drop=True)

# --------------------------------------------------
# 6. Save cleaned dataset
# --------------------------------------------------

df_clean.to_csv(
    OUTPUT_FILE,
    index=False
)

# --------------------------------------------------
# 7. Print summary
# --------------------------------------------------

print("\n" + "=" * 80)
print("GROUNDWATER CLEANING COMPLETE")
print("=" * 80)

print("\nOriginal rows:", len(df))
print("Missing groundwater values:", missing_before)
print("Rows removed:", removed_rows)
print("Final rows:", len(df_clean))

print("\nDate range:")
print("Earliest:", df_clean["date"].min())
print("Latest:  ", df_clean["date"].max())

print("\nRecords by season:")
print(
    df_clean["season"]
    .value_counts()
)

print("\nMissing Block values after standardisation:")
print(
    df_clean["Block"]
    .isna()
    .sum()
)

print("\nOutput file:")
print(OUTPUT_FILE)

print("\nFinal columns:")
print(df_clean.columns.tolist())

print("\n" + "=" * 80)