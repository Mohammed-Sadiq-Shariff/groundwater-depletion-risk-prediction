from pathlib import Path
import sys

import joblib
import numpy as np
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "mysore_model_features.csv"
)

GROUNDWATER_MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "groundwater_prediction_model.joblib"
)

GROUNDWATER_FEATURE_INFO_PATH = (
    PROJECT_ROOT
    / "models"
    / "feature_info.joblib"
)

RISK_MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "groundwater_depletion_risk_model.joblib"
)

RISK_FEATURE_INFO_PATH = (
    PROJECT_ROOT
    / "models"
    / "risk_feature_info.joblib"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def print_section(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def format_value(value):
    """
    Format values safely for console output.
    """
    if pd.isna(value):
        return "Unknown"

    return str(value)


def get_feature_columns(feature_info):
    """
    Extract feature column names from the saved feature information.

    This function supports several possible joblib dictionary formats.
    """

    if isinstance(feature_info, dict):

        possible_keys = [
            "feature_columns",
            "features",
            "input_features",
            "model_features",
        ]

        for key in possible_keys:
            if key in feature_info:
                return list(feature_info[key])

    if isinstance(feature_info, (list, tuple)):
        return list(feature_info)

    raise ValueError(
        "Could not determine feature columns from the feature "
        "information file."
    )


def get_latest_station_record(df, station_name):
    """
    Return the most recent record for a station.
    """

    station_data = df[
        df["Station"]
        .astype(str)
        .str.strip()
        .str.lower()
        ==
        station_name.strip().lower()
    ].copy()

    if station_data.empty:
        return None

    station_data = station_data.sort_values(
        "Monitoring Date"
    )

    return station_data.iloc[[-1]].copy()


# ============================================================
# LOAD MODELS
# ============================================================

print_section("LOADING TRAINED MODELS")

if not GROUNDWATER_MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Groundwater model not found:\n"
        f"{GROUNDWATER_MODEL_PATH}"
    )

if not RISK_MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Risk model not found:\n"
        f"{RISK_MODEL_PATH}"
    )

groundwater_model = joblib.load(
    GROUNDWATER_MODEL_PATH
)

groundwater_feature_info = joblib.load(
    GROUNDWATER_FEATURE_INFO_PATH
)

risk_model = joblib.load(
    RISK_MODEL_PATH
)

risk_feature_info = joblib.load(
    RISK_FEATURE_INFO_PATH
)

groundwater_features = get_feature_columns(
    groundwater_feature_info
)

risk_features = get_feature_columns(
    risk_feature_info
)

print("Groundwater prediction model loaded.")
print("Risk prediction model loaded.")

print()
print(
    "Groundwater model features:",
    len(groundwater_features)
)

print(
    "Risk model features:",
    len(risk_features)
)


# ============================================================
# LOAD FEATURE DATA
# ============================================================

print_section("LOADING LATEST STATION FEATURES")

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Feature dataset not found:\n{DATA_PATH}"
    )

df = pd.read_csv(DATA_PATH)

print(f"Records loaded: {len(df)}")

if "Monitoring Date" not in df.columns:
    raise ValueError(
        "'Monitoring Date' column not found."
    )

df["Monitoring Date"] = pd.to_datetime(
    df["Monitoring Date"],
    errors="coerce"
)

invalid_dates = df["Monitoring Date"].isna().sum()

print(f"Invalid dates: {invalid_dates}")

df = df.dropna(
    subset=["Monitoring Date"]
).copy()

df = df.sort_values(
    ["Station", "Monitoring Date"]
).reset_index(drop=True)


# ============================================================
# SHOW AVAILABLE STATIONS
# ============================================================

print_section("AVAILABLE GROUNDWATER STATIONS")

stations = sorted(
    df["Station"]
    .dropna()
    .astype(str)
    .unique()
)

print(f"Number of stations: {len(stations)}")
print()

for index, station in enumerate(stations, start=1):
    print(f"{index:>3}. {station}")


# ============================================================
# SELECT STATION
# ============================================================

print_section("SELECT A STATION")

station_name = input(
    "Enter station name exactly as shown above: "
).strip()

latest_record = get_latest_station_record(
    df,
    station_name
)

if latest_record is None:

    print()
    print(
        f"Station '{station_name}' was not found."
    )

    print()
    print(
        "Please run the script again and enter "
        "one of the listed station names."
    )

    sys.exit(1)


# ============================================================
# DISPLAY LATEST OBSERVATION
# ============================================================

print_section("LATEST GROUNDWATER OBSERVATION")

record = latest_record.iloc[0]

print(
    "Station:",
    format_value(record.get("Station"))
)

print(
    "District:",
    format_value(record.get("District"))
)

print(
    "Tehsil:",
    format_value(record.get("Tehsil"))
)

print(
    "Block:",
    format_value(record.get("Block"))
)

print(
    "Village:",
    format_value(record.get("Village"))
)

print()

print(
    "Monitoring date:",
    record["Monitoring Date"]
)

print(
    "Current groundwater level:",
    f"{record['groundwater_level_m']:.2f} m"
)


# ============================================================
# VALIDATE MODEL FEATURES
# ============================================================

print_section("VALIDATING MODEL FEATURES")

missing_groundwater_features = [
    feature
    for feature in groundwater_features
    if feature not in latest_record.columns
]

missing_risk_features = [
    feature
    for feature in risk_features
    if feature not in latest_record.columns
]

if missing_groundwater_features:

    print(
        "Missing groundwater model features:"
    )

    for feature in missing_groundwater_features:
        print(" -", feature)

    raise ValueError(
        "Feature dataset does not contain all "
        "groundwater model features."
    )


if missing_risk_features:

    print(
        "Missing risk model features:"
    )

    for feature in missing_risk_features:
        print(" -", feature)

    raise ValueError(
        "Feature dataset does not contain all "
        "risk model features."
    )


print(
    "All groundwater model features are available."
)

print(
    "All risk model features are available."
)


# ============================================================
# PREPARE MODEL INPUTS
# ============================================================

X_groundwater = latest_record[
    groundwater_features
].copy()

X_risk = latest_record[
    risk_features
].copy()


# ============================================================
# PREDICT NEXT GROUNDWATER LEVEL
# ============================================================

print_section("PREDICTING NEXT GROUNDWATER LEVEL")

predicted_groundwater_level = float(
    groundwater_model.predict(
        X_groundwater
    )[0]
)

current_groundwater_level = float(
    record["groundwater_level_m"]
)

predicted_change = (
    predicted_groundwater_level
    -
    current_groundwater_level
)

print(
    "Current groundwater level:",
    f"{current_groundwater_level:.2f} m"
)

print(
    "Predicted next groundwater level:",
    f"{predicted_groundwater_level:.2f} m"
)

print(
    "Predicted groundwater change:",
    f"{predicted_change:+.2f} m"
)


# ============================================================
# PREDICT DEPLETION RISK
# ============================================================

print_section("PREDICTING DEPLETION RISK")

predicted_risk = risk_model.predict(
    X_risk
)[0]

print(
    "Predicted depletion risk:",
    predicted_risk
)


# ============================================================
# RISK PROBABILITIES
# ============================================================

print_section("DEPLETION RISK PROBABILITIES")

if hasattr(risk_model, "predict_proba"):

    probabilities = risk_model.predict_proba(
        X_risk
    )[0]

    classes = risk_model.classes_

    probability_dict = dict(
        zip(classes, probabilities)
    )

    risk_order = [
        "No Depletion",
        "Low",
        "Moderate",
        "High",
    ]

    for risk in risk_order:

        probability = (
            probability_dict.get(risk, 0)
            * 100
        )

        print(
            f"{risk:<15}: {probability:6.2f}%"
        )

else:

    print(
        "Probability prediction is not "
        "available for this model."
    )


# ============================================================
# INTERPRET GROUNDWATER CHANGE
# ============================================================

print_section("GROUNDWATER FORECAST INTERPRETATION")

if predicted_change > 0.25:

    print(
        "Expected groundwater depth is increasing."
    )

    print(
        "This generally indicates a declining "
        "groundwater condition because the water "
        "table is becoming deeper."
    )

elif predicted_change < -0.25:

    print(
        "Expected groundwater depth is decreasing."
    )

    print(
        "This generally indicates groundwater "
        "recovery because the water table is "
        "becoming shallower."
    )

else:

    print(
        "Groundwater level is expected to remain "
        "relatively stable."
    )


# ============================================================
# SAVE PREDICTION RESULT
# ============================================================

print_section("SAVING PREDICTION RESULT")

output_dir = PROJECT_ROOT / "reports"

output_dir.mkdir(
    parents=True,
    exist_ok=True
)

result = {
    "Station": record.get("Station"),
    "District": record.get("District"),
    "Tehsil": record.get("Tehsil"),
    "Block": record.get("Block"),
    "Village": record.get("Village"),
    "Monitoring Date": record["Monitoring Date"],
    "Current Groundwater Level (m)": (
        current_groundwater_level
    ),
    "Predicted Next Groundwater Level (m)": (
        predicted_groundwater_level
    ),
    "Predicted Groundwater Change (m)": (
        predicted_change
    ),
    "Predicted Depletion Risk": predicted_risk,
}


if hasattr(risk_model, "predict_proba"):

    for risk in [
        "No Depletion",
        "Low",
        "Moderate",
        "High",
    ]:

        result[
            f"{risk} Probability"
        ] = (
            probability_dict.get(risk, 0)
            * 100
        )


result_df = pd.DataFrame([result])

output_path = (
    output_dir
    / "latest_station_prediction.csv"
)

result_df.to_csv(
    output_path,
    index=False
)

print(
    "Prediction saved to:"
)

print(output_path)


# ============================================================
# FINAL SUMMARY
# ============================================================

print_section(
    "GROUNDWATER DEPLETION RISK PREDICTION COMPLETE"
)

print(
    f"Station: {record.get('Station')}"
)

print(
    f"Monitoring date: {record['Monitoring Date']}"
)

print()

print(
    f"Current groundwater level: "
    f"{current_groundwater_level:.2f} m"
)

print(
    f"Predicted next groundwater level: "
    f"{predicted_groundwater_level:.2f} m"
)

print(
    f"Predicted groundwater change: "
    f"{predicted_change:+.2f} m"
)

print()

print(
    f"Predicted depletion risk: "
    f"{predicted_risk}"
)

print()

print("=" * 60)