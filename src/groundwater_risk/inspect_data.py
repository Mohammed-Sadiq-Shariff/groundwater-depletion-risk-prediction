from pathlib import Path
import pandas as pd

# Project root
ROOT = Path(__file__).resolve().parents[2]
# --------------------------------------------------
# INSPECT RAINFALL FILES
# --------------------------------------------------

rainfall_dir = ROOT / "data" / "raw" / "rainfall"

print("\n" + "=" * 80)
print("RAINFALL FILES")
print("=" * 80)

for file in sorted(rainfall_dir.glob("*.csv")):

    print(f"\nFILE: {file.name}")

    try:
        df = pd.read_csv(file, nrows=5)

        print("Columns:")
        print(list(df.columns))

        print("\nFirst rows:")
        print(df.head())

        print("\nShape sample:", df.shape)

    except Exception as e:
        print(f"ERROR: {e}")


# --------------------------------------------------
# INSPECT GROUNDWATER CSV FILES
# --------------------------------------------------

groundwater_dir = ROOT / "data" / "raw" / "groundwater"

print("\n" + "=" * 80)
print("GROUNDWATER FILES")
print("=" * 80)

for file in sorted(groundwater_dir.glob("*.csv")):

    print(f"\nFILE: {file.name}")

    try:
        df = pd.read_csv(file, nrows=5)

        print("Columns:")
        print(list(df.columns))

        print("\nFirst rows:")
        print(df.head())

        print("\nShape sample:", df.shape)

    except Exception as e:
        print(f"ERROR: {e}")