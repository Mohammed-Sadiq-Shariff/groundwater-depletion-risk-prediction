"""
Generate predictions for all monitoring stations using the existing
trained groundwater prediction and depletion risk models.

The trained models require engineered historical features that are not
stored directly in mysore_model_dataset.csv. This script reconstructs
those features from each station's historical observations without
retraining or modifying the models.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd


DATA_PATH = Path("data/processed/mysore_model_dataset.csv")
PREDICTION_MODEL_PATH = Path("models/groundwater_prediction_model.joblib")
RISK_MODEL_PATH = Path("models/groundwater_depletion_risk_model.joblib")
FEATURE_INFO_PATH = Path("models/feature_info.joblib")
RISK_FEATURE_INFO_PATH = Path("models/risk_feature_info.joblib")
OUTPUT_PATH = Path("reports/all_station_predictions.csv")


def get_season(month: int) -> str:
    """
    Return the season category used by the feature engineering pipeline.

    CGWB Karnataka monitoring campaign grouping:
    - January: Winter (month 1, or months 12, 1, 2)
    - Pre_monsoon: May (month 5, or months 3, 4, 5)
    - Monsoon: August (month 8, or months 6, 7, 8, 9)
    - Post_monsoon: November (month 11, or months 10, 11)
    """
    season_mapping = {
        1: "January",
        5: "Pre_monsoon",
        8: "Monsoon",
        11: "Post_monsoon",
    }
    if month in season_mapping:
        return season_mapping[month]

    if month in (12, 1, 2):
        return "January"
    if month in (3, 4, 5):
        return "Pre_monsoon"
    if month in (6, 7, 8, 9):
        return "Monsoon"
    return "Post_monsoon"


def build_features(station_data: pd.DataFrame) -> pd.Series:
    """
    Rebuild all model features for the latest record of one station.

    Historical lag and rolling features are calculated using only the
    station's previous chronological groundwater observations, strictly
    matching create_model_features.py shift(1) conventions.
    """

    station_data = station_data.copy()

    station_data["Monitoring Date"] = pd.to_datetime(
        station_data["Monitoring Date"],
        errors="coerce",
    )

    station_data = station_data.dropna(
        subset=["Monitoring Date", "groundwater_level_m"]
    )

    station_data = station_data.sort_values("Monitoring Date").reset_index(
        drop=True
    )

    if station_data.empty:
        raise ValueError("No valid historical observations")

    latest = station_data.iloc[-1].copy()

    groundwater = pd.to_numeric(
        station_data["groundwater_level_m"],
        errors="coerce",
    )

    if groundwater.notna().sum() < 1:
        raise ValueError("No valid groundwater values")

    # Historical lag values.
    latest["gw_lag_1"] = (
        groundwater.iloc[-2]
        if len(groundwater) >= 2
        else groundwater.iloc[-1]
    )

    latest["gw_lag_2"] = (
        groundwater.iloc[-3]
        if len(groundwater) >= 3
        else latest["gw_lag_1"]
    )

    latest["gw_lag_3"] = (
        groundwater.iloc[-4]
        if len(groundwater) >= 4
        else latest["gw_lag_2"]
    )

    latest["gw_lag_4"] = (
        groundwater.iloc[-5]
        if len(groundwater) >= 5
        else latest["gw_lag_3"]
    )

    # Groundwater changes.
    latest["gw_change_1"] = (
        groundwater.iloc[-1] - latest["gw_lag_1"]
    )

    latest["gw_change_2"] = (
        latest["gw_lag_1"] - latest["gw_lag_2"]
    )

    # Rolling historical statistics on prior observations (shift(1) convention).
    prior_gw = groundwater.iloc[:-1] if len(groundwater) > 1 else groundwater
    history_for_3 = prior_gw.iloc[-3:] if len(prior_gw) >= 3 else prior_gw
    history_for_4 = prior_gw.iloc[-4:] if len(prior_gw) >= 4 else prior_gw

    latest["gw_rolling_mean_3"] = history_for_3.mean()
    latest["gw_rolling_mean_4"] = history_for_4.mean()

    latest["gw_rolling_std_3"] = (
        history_for_3.std()
        if len(history_for_3) > 1
        else 0.0
    )

    # Station-wide historical statistics (prior observations).
    latest["station_historical_mean"] = prior_gw.mean()

    latest["station_historical_std"] = (
        prior_gw.std()
        if len(prior_gw) > 1
        else 0.0
    )

    # Time-derived features.
    monitoring_date = pd.to_datetime(latest["Monitoring Date"])

    latest["year"] = monitoring_date.year
    latest["month"] = monitoring_date.month
    latest["quarter"] = monitoring_date.quarter

    latest["month_sin"] = np.sin(
        2 * np.pi * monitoring_date.month / 12
    )

    latest["month_cos"] = np.cos(
        2 * np.pi * monitoring_date.month / 12
    )

    latest["season"] = get_season(
        int(monitoring_date.month)
    )

    return latest


def main() -> None:
    print("Generating predictions for all monitoring stations...\n")

    # Load datasets.
    gw_data = pd.read_csv(DATA_PATH)

    gw_data["Monitoring Date"] = pd.to_datetime(
        gw_data["Monitoring Date"],
        errors="coerce",
    )

    print(
        f"Loaded data: {len(gw_data):,} records, "
        f"{gw_data['Station'].nunique():,} stations"
    )

    # Load existing trained models.
    pred_model = joblib.load(PREDICTION_MODEL_PATH)
    risk_model = joblib.load(RISK_MODEL_PATH)

    feature_info = joblib.load(FEATURE_INFO_PATH)
    risk_feature_info = joblib.load(RISK_FEATURE_INFO_PATH)

    pred_features = feature_info.get("features", [])
    risk_features = risk_feature_info.get("features", [])

    print(f"Prediction features: {len(pred_features)}")
    print(f"Risk features: {len(risk_features)}")

    predictions = []

    error_count = 0
    success_count = 0

    stations = (
        gw_data["Station"]
        .dropna()
        .unique()
    )

    for station in stations:
        try:
            station_data = gw_data[
                gw_data["Station"] == station
            ].copy()

            latest = build_features(station_data)

            # Verify every required feature now exists.
            missing_pred_features = [
                feature
                for feature in pred_features
                if feature not in latest.index
            ]

            missing_risk_features = [
                feature
                for feature in risk_features
                if feature not in latest.index
            ]

            if missing_pred_features:
                raise ValueError(
                    f"Missing prediction features: "
                    f"{missing_pred_features}"
                )

            if missing_risk_features:
                raise ValueError(
                    f"Missing risk features: "
                    f"{missing_risk_features}"
                )

            # Build DataFrames with exact training feature order.
            X_pred = pd.DataFrame(
                [latest[pred_features]]
            )

            X_risk = pd.DataFrame(
                [latest[risk_features]]
            )

            # Generate groundwater prediction.
            predicted_gw = float(
                pred_model.predict(X_pred)[0]
            )

            # Generate depletion risk prediction.
            risk_pred = risk_model.predict(X_risk)[0]

            # Risk probabilities.
            if hasattr(risk_model, "predict_proba"):
                probability_values = (
                    risk_model.predict_proba(X_risk)[0]
                )

                risk_probabilities = {
                    risk_class: float(probability)
                    for risk_class, probability
                    in zip(
                        risk_model.classes_,
                        probability_values,
                    )
                }
            else:
                risk_probabilities = {
                    "No Depletion": 0.0,
                    "Low": 0.0,
                    "Moderate": 0.0,
                    "High": 0.0,
                }

                risk_probabilities[str(risk_pred)] = 1.0

            current_gw = float(
                latest["groundwater_level_m"]
            )

            prediction = {
                "Station": station,
                "District": latest.get("District", ""),
                "Tehsil": latest.get("Tehsil", ""),
                "Block": latest.get("Block", ""),
                "Village": latest.get("Village", ""),
                "Latitude": latest.get("Latitude", np.nan),
                "Longitude": latest.get("Longitude", np.nan),
                "Monitoring Date": pd.to_datetime(
                    latest["Monitoring Date"]
                ).strftime("%Y-%m-%d"),
                "Current Groundwater Level (m)": current_gw,
                "Predicted Next Groundwater Level (m)": predicted_gw,
                "Predicted Groundwater Change (m)": (
                    predicted_gw - current_gw
                ),
                "Predicted Depletion Risk": str(risk_pred),
                "No Depletion Probability": (
                    risk_probabilities.get(
                        "No Depletion",
                        0.0,
                    )
                    * 100
                ),
                "Low Probability": (
                    risk_probabilities.get(
                        "Low",
                        0.0,
                    )
                    * 100
                ),
                "Moderate Probability": (
                    risk_probabilities.get(
                        "Moderate",
                        0.0,
                    )
                    * 100
                ),
                "High Probability": (
                    risk_probabilities.get(
                        "High",
                        0.0,
                    )
                    * 100
                ),
            }

            predictions.append(prediction)

            success_count += 1

            print(
                f"[{success_count}] {station}: "
                f"{current_gw:.2f} m -> "
                f"{predicted_gw:.2f} m | "
                f"{risk_pred}"
            )

        except Exception as error:
            error_count += 1

            print(
                f"ERROR | {station}: {error}"
            )

    predictions_df = pd.DataFrame(predictions)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    predictions_df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print("\n" + "=" * 60)
    print("PREDICTION GENERATION COMPLETE")
    print("=" * 60)

    print(
        f"Successful predictions: {success_count}"
    )

    print(
        f"Errors: {error_count}"
    )

    print(
        f"Output: {OUTPUT_PATH.resolve()}"
    )

    if not predictions_df.empty:
        print(
            f"Output rows: {len(predictions_df)}"
        )

        print(
            "\nRisk distribution:"
        )

        print(
            predictions_df[
                "Predicted Depletion Risk"
            ]
            .value_counts()
            .to_string()
        )
    else:
        print(
            "\nWARNING: No predictions were generated."
        )


if __name__ == "__main__":
    main()