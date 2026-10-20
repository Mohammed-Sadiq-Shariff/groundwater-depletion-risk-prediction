from pathlib import Path
import pandas as pd

INPUT_FILE = Path(
    "data/interim/groundwater/mysore_groundwater_1991_2025.csv"
)

df = pd.read_csv(INPUT_FILE)

# Convert types again after reading CSV
df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

df["groundwater_level_m"] = pd.to_numeric(
    df["groundwater_level_m"],
    errors="coerce"
)

print("=" * 80)
print("MYSORE GROUNDWATER DATA INSPECTION")
print("=" * 80)

print("\n1. DATASET SHAPE")
print(df.shape)

print("\n2. DATE RANGE")
print("Earliest:", df["date"].min())
print("Latest:  ", df["date"].max())

print("\n3. UNIQUE STATIONS")
print(df["station"].nunique())

print("\n4. RECORDS PER YEAR")
print(
    df["date"]
    .dt.year
    .value_counts()
    .sort_index()
)

print("\n5. RECORDS BY MONTH")
print(
    df["date"]
    .dt.month
    .value_counts()
    .sort_index()
)

print("\n6. MISSING VALUES")
print(
    df[
        [
            "station",
            "District",
            "Latitude",
            "Longitude",
            "date",
            "groundwater_level_m"
        ]
    ]
    .isna()
    .sum()
)

print("\n7. GROUNDWATER LEVEL SUMMARY")
print(
    df["groundwater_level_m"]
    .describe()
)

print("\n8. DUPLICATE CHECK")

duplicate_count = df.duplicated(
    subset=[
        "station",
        "date",
        "Latitude",
        "Longitude"
    ]
).sum()

print("Duplicate station-date-coordinate records:", duplicate_count)

print("\n9. NEGATIVE OR ZERO WATER LEVELS")

invalid_levels = df[
    df["groundwater_level_m"] <= 0
]

print("Count:", len(invalid_levels))

if len(invalid_levels) > 0:
    print(
        invalid_levels[
            [
                "station",
                "date",
                "groundwater_level_m"
            ]
        ].head(10)
    )

print("\n10. STATIONS WITH MOST RECORDS")

print(
    df["station"]
    .value_counts()
    .head(20)
)

print("\n11. TEHSIL / BLOCK COVERAGE")

print("Unique Tehsils:", df["Tehsil"].nunique())
print("Unique Blocks:", df["Block"].nunique())

print("\nRecords by Block:")

print(
    df["Block"]
    .value_counts()
)

print("\n" + "=" * 80)
print("INSPECTION COMPLETE")
print("=" * 80)