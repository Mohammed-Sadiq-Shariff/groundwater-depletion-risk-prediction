from pathlib import Path
import pandas as pd

# Project paths
RAW_DIR = Path("data/raw/groundwater")
INTERIM_DIR = Path("data/interim/groundwater")

INTERIM_DIR.mkdir(parents=True, exist_ok=True)

# Input files
file_1991_2020 = RAW_DIR / "gwl_manual_quarterly_cgwb_ka_1991_2020.csv"
file_2021_2025 = RAW_DIR / "groundwater_karnataka_2021_2025.csv"

# Output file
output_file = INTERIM_DIR / "mysore_groundwater_1991_2025.csv"

print("Loading datasets...")

df_old = pd.read_csv(file_1991_2020)
df_new = pd.read_csv(file_2021_2025)

print(f"1991-2020 shape: {df_old.shape}")
print(f"2021-2025 shape: {df_new.shape}")

# Combine datasets
df = pd.concat(
    [df_old, df_new],
    ignore_index=True
)

print(f"\nCombined shape: {df.shape}")

# Filter Mysore district
df_mysore = df[
    df["District"]
    .astype(str)
    .str.strip()
    .str.lower()
    == "mysore"
].copy()

print(f"Mysore rows: {df_mysore.shape[0]}")

# Rename important columns to simpler names
df_mysore = df_mysore.rename(
    columns={
        "Groundwater Level Quarterly Manual (meter)": "groundwater_level_m",
        "Data Acquisition Time": "date",
        "Station": "station"
    }
)

# Convert date
df_mysore["date"] = pd.to_datetime(
    df_mysore["date"],
    dayfirst=True,
    errors="coerce"
)

# Convert groundwater level to numeric
df_mysore["groundwater_level_m"] = pd.to_numeric(
    df_mysore["groundwater_level_m"],
    errors="coerce"
)

# Sort chronologically
df_mysore = df_mysore.sort_values(
    ["station", "date"]
).reset_index(drop=True)

# Save
df_mysore.to_csv(
    output_file,
    index=False
)

print("\nDataset created successfully.")
print(f"Output: {output_file}")
print(f"Shape: {df_mysore.shape}")

print("\nColumns:")
print(df_mysore.columns.tolist())

print("\nDate range:")
print(df_mysore["date"].min())
print(df_mysore["date"].max())

print("\nSample:")
print(
    df_mysore[
        [
            "station",
            "District",
            "Tehsil",
            "Block",
            "Village",
            "Latitude",
            "Longitude",
            "date",
            "groundwater_level_m"
        ]
    ].head(10)
)