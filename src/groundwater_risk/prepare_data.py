from pathlib import Path
import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_GW_DIR = PROJECT_ROOT / "data" / "raw" / "groundwater"
RAW_RAIN_DIR = PROJECT_ROOT / "data" / "raw" / "rainfall"

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 1. LOAD AND COMBINE GROUNDWATER DATA
# ============================================================

print("\nLoading groundwater files...")

groundwater_files = [
    RAW_GW_DIR / "gwl_manual_quarterly_cgwb_ka_1991_2020.csv",
    RAW_GW_DIR / "groundwater_karnataka_2021_2025.csv",
]

gw_frames = []

for file in groundwater_files:
    print(f"Loading: {file.name}")
    df = pd.read_csv(file)
    gw_frames.append(df)

groundwater = pd.concat(gw_frames, ignore_index=True)

print(f"\nTotal groundwater records: {len(groundwater):,}")


# ============================================================
# 2. CHECK DISTRICT NAMES
# ============================================================

print("\nChecking groundwater district names...")

districts = sorted(
    groundwater["District"]
    .dropna()
    .astype(str)
    .unique()
)

mysore_districts = [
    district for district in districts
    if "mys" in district.lower()
]

print("Possible Mysore/Mysuru district names:")
print(mysore_districts)


# ============================================================
# 3. FILTER MYSORE / MYSURU GROUNDWATER
# ============================================================

groundwater_mysore = groundwater[
    groundwater["District"]
    .astype(str)
    .str.contains("mys", case=False, na=False)
].copy()

print(f"\nMysore/Mysuru groundwater records: {len(groundwater_mysore):,}")

print("\nActual district names found:")
print(groundwater_mysore["District"].value_counts())


# ============================================================
# 4. CONVERT GROUNDWATER DATE
# ============================================================

groundwater_mysore["Data Acquisition Time"] = pd.to_datetime(
    groundwater_mysore["Data Acquisition Time"],
    errors="coerce"
)

print("\nGroundwater date range:")
print(
    groundwater_mysore["Data Acquisition Time"].min(),
    "to",
    groundwater_mysore["Data Acquisition Time"].max()
)


# ============================================================
# 5. SAVE MYSORE GROUNDWATER
# ============================================================

gw_output = PROCESSED_DIR / "mysore_groundwater_1991_2025.csv"

groundwater_mysore.to_csv(
    gw_output,
    index=False
)

print(f"\nSaved groundwater data:")
print(gw_output)


# ============================================================
# 6. LOAD AND COMBINE RAINFALL FILES
# ============================================================

print("\nLoading rainfall files...")

rainfall_files = sorted(RAW_RAIN_DIR.glob("*.csv"))

print(f"Rainfall files found: {len(rainfall_files)}")

rain_frames = []

for file in rainfall_files:

    if file.name == ".gitkeep":
        continue

    print(f"Loading: {file.name}")

    df = pd.read_csv(file)

    rain_frames.append(df)


rainfall = pd.concat(
    rain_frames,
    ignore_index=True
)

print(f"\nTotal rainfall records: {len(rainfall):,}")


# ============================================================
# 7. CHECK MYSORE / MYSURU DISTRICT NAMES
# ============================================================

rain_districts = sorted(
    rainfall["District"]
    .dropna()
    .astype(str)
    .unique()
)

mysore_rain_districts = [
    district for district in rain_districts
    if "mys" in district.lower()
]

print("\nPossible Mysore/Mysuru rainfall district names:")
print(mysore_rain_districts)


# ============================================================
# 8. FILTER MYSORE / MYSURU RAINFALL
# ============================================================

rainfall_mysore = rainfall[
    rainfall["District"]
    .astype(str)
    .str.contains("mys", case=False, na=False)
].copy()

print(f"\nMysore/Mysuru rainfall records: {len(rainfall_mysore):,}")

print("\nActual district names found:")
print(rainfall_mysore["District"].value_counts())


# ============================================================
# 9. CONVERT RAINFALL DATE
# ============================================================

rainfall_mysore["Monitoring Date"] = pd.to_datetime(
    rainfall_mysore["Monitoring Date"],
    dayfirst=True,
    errors="coerce"
)

rainfall_mysore["Rainfall (MM)"] = pd.to_numeric(
    rainfall_mysore["Rainfall (MM)"],
    errors="coerce"
)

print("\nRainfall date range:")
print(
    rainfall_mysore["Monitoring Date"].min(),
    "to",
    rainfall_mysore["Monitoring Date"].max()
)


# ============================================================
# 10. SAVE MYSORE RAINFALL
# ============================================================

rain_output = PROCESSED_DIR / "mysore_rainfall_1991_2025.csv"

rainfall_mysore.to_csv(
    rain_output,
    index=False
)

print(f"\nSaved rainfall data:")
print(rain_output)


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DATA PREPARATION COMPLETE")
print("=" * 60)

print(f"Groundwater records: {len(groundwater_mysore):,}")
print(f"Rainfall records:    {len(rainfall_mysore):,}")

print("\nNext step:")
print("Aggregate rainfall into quarterly features and align it")
print("with groundwater monitoring dates.")