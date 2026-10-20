from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from app.config import (
    ALL_PREDICTIONS_PATH,
    FEATURE_IMPORTANCE_PATH,
    GROUNDWATER_DATA_PATH,
    LATEST_PREDICTION_PATH,
    MODEL_DATASET_PATH,
    RAINFALL_DATA_PATH,
)


def _safe_float(value: Any) -> Optional[float]:
    if pd.isna(value):
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _safe_value(value: Any) -> Any:
    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.isoformat()

    return value


@lru_cache(maxsize=1)
def load_model_dataset() -> pd.DataFrame:
    if not MODEL_DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Model dataset not found: {MODEL_DATASET_PATH}"
        )

    df = pd.read_csv(MODEL_DATASET_PATH)

    if "Monitoring Date" in df.columns:
        df["Monitoring Date"] = pd.to_datetime(
            df["Monitoring Date"],
            errors="coerce",
        )

    return df


@lru_cache(maxsize=1)
def load_groundwater_dataset() -> pd.DataFrame:
    if not GROUNDWATER_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Groundwater dataset not found: {GROUNDWATER_DATA_PATH}"
        )

    df = pd.read_csv(GROUNDWATER_DATA_PATH)

    return df


@lru_cache(maxsize=1)
def load_rainfall_dataset() -> pd.DataFrame:
    if not RAINFALL_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Rainfall dataset not found: {RAINFALL_DATA_PATH}"
        )

    df = pd.read_csv(RAINFALL_DATA_PATH)

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce",
        )

    return df


@lru_cache(maxsize=1)
def load_all_predictions() -> pd.DataFrame:
    """
    Load all station predictions.

    Uses all_station_predictions.csv when it contains valid data.
    Falls back to latest_station_prediction.csv when the all-stations
    prediction file is missing, empty, or unreadable.
    """

    if ALL_PREDICTIONS_PATH.exists():
        try:
            predictions = pd.read_csv(ALL_PREDICTIONS_PATH)

            if not predictions.empty and len(predictions.columns) > 0:
                return predictions

        except pd.errors.EmptyDataError:
            pass

        except Exception:
            pass

    if LATEST_PREDICTION_PATH.exists():
        try:
            predictions = pd.read_csv(LATEST_PREDICTION_PATH)

            if not predictions.empty and len(predictions.columns) > 0:
                return predictions

        except pd.errors.EmptyDataError:
            pass

        except Exception:
            pass

    return pd.DataFrame()

@lru_cache(maxsize=1)
def load_latest_prediction() -> pd.DataFrame:
    """
    Load the latest prediction data safely.
    """

    if not LATEST_PREDICTION_PATH.exists():
        return pd.DataFrame()

    try:
        predictions = pd.read_csv(LATEST_PREDICTION_PATH)

        if predictions.empty or len(predictions.columns) == 0:
            return pd.DataFrame()

        return predictions

    except pd.errors.EmptyDataError:
        return pd.DataFrame()

    except Exception:
        return pd.DataFrame()


@lru_cache(maxsize=1)
def load_feature_importance() -> pd.DataFrame:
    if not FEATURE_IMPORTANCE_PATH.exists():
        return pd.DataFrame()

    return pd.read_csv(FEATURE_IMPORTANCE_PATH)


def get_overview() -> Dict[str, Any]:
    df = load_model_dataset()

    stations = (
        int(df["Station"].nunique())
        if "Station" in df.columns
        else 0
    )

    observations = int(len(df))

    high_risk = 0

    predictions = load_all_predictions()

    if (
        not predictions.empty
        and "Predicted Depletion Risk" in predictions.columns
    ):
        high_risk = int(
            (
                predictions[
                    "Predicted Depletion Risk"
                ]
                .astype(str)
                .str.strip()
                .str.lower()
                == "high"
            ).sum()
        )

    historical_coverage = 0.0

    if "Monitoring Date" in df.columns:
        dates = pd.to_datetime(
            df["Monitoring Date"],
            errors="coerce",
        ).dropna()

        if not dates.empty:
            historical_coverage = round(
                (
                    (dates.max() - dates.min()).days
                    / 365.25
                ),
                1,
            )

    return {
        "monitoring_stations": stations,
        "total_observations": observations,
        "historical_coverage_years": historical_coverage,
        "high_risk_stations": high_risk,
    }


def get_stations() -> List[Dict[str, Any]]:
    df = load_model_dataset()

    if "Station" not in df.columns:
        return []

    results: List[Dict[str, Any]] = []

    for station_name, group in df.groupby("Station"):
        latest = group.copy()

        if "Monitoring Date" in latest.columns:
            latest = latest.sort_values("Monitoring Date")

        row = latest.iloc[-1]

        results.append(
            {
                "station": str(station_name),
                "district": (
                    str(row["District"])
                    if "District" in row.index
                    and pd.notna(row["District"])
                    else None
                ),
                "tehsil": (
                    str(row["Tehsil"])
                    if "Tehsil" in row.index
                    and pd.notna(row["Tehsil"])
                    else None
                ),
                "block": (
                    str(row["Block"])
                    if "Block" in row.index
                    and pd.notna(row["Block"])
                    else None
                ),
                "village": (
                    str(row["Village"])
                    if "Village" in row.index
                    and pd.notna(row["Village"])
                    else None
                ),
                "latitude": (
                    _safe_float(row["Latitude"])
                    if "Latitude" in row.index
                    else None
                ),
                "longitude": (
                    _safe_float(row["Longitude"])
                    if "Longitude" in row.index
                    else None
                ),
                "records": int(len(group)),
            }
        )

    return sorted(
        results,
        key=lambda item: item["station"],
    )


def get_station_details(
    station_name: str,
) -> Optional[Dict[str, Any]]:
    df = load_model_dataset()

    if "Station" not in df.columns:
        return None

    station_df = df[
        df["Station"].astype(str) == station_name
    ].copy()

    if station_df.empty:
        return None

    if "Monitoring Date" in station_df.columns:
        station_df = station_df.sort_values(
            "Monitoring Date"
        )

    latest = station_df.iloc[-1]

    result: Dict[str, Any] = {
        "station": station_name,
        "records": int(len(station_df)),
    }

    for column in [
        "District",
        "Tehsil",
        "Block",
        "Village",
        "Latitude",
        "Longitude",
    ]:
        if column in latest.index:
            key = (
                column.lower()
                .replace(" ", "_")
            )
            result[key] = _safe_value(
                latest[column]
            )

    if "Monitoring Date" in station_df.columns:
        result["date_range"] = {
            "start": _safe_value(
                station_df[
                    "Monitoring Date"
                ].min()
            ),
            "end": _safe_value(
                station_df[
                    "Monitoring Date"
                ].max()
            ),
        }

    return result


def get_station_history(
    station_name: str,
) -> List[Dict[str, Any]]:
    df = load_model_dataset()

    station_df = df[
        df["Station"].astype(str) == station_name
    ].copy()

    if station_df.empty:
        return []

    if "Monitoring Date" in station_df.columns:
        station_df = station_df.sort_values(
            "Monitoring Date"
        )

    preferred_columns = [
        "Monitoring Date",
        "groundwater_level_m",
        "rain_7d",
        "rain_30d",
        "rain_90d",
        "rain_180d",
        "rain_365d",
    ]

    available_columns = [
        column
        for column in preferred_columns
        if column in station_df.columns
    ]

    if not available_columns:
        return []

    records: List[Dict[str, Any]] = []

    for _, row in station_df[
        available_columns
    ].iterrows():
        item: Dict[str, Any] = {}

        for column in available_columns:
            key = (
                "date"
                if column == "Monitoring Date"
                else column
            )

            value = row[column]

            if column == "Monitoring Date":
                value = _safe_value(
                    pd.to_datetime(
                        value,
                        errors="coerce",
                    )
                )
            else:
                value = _safe_float(value)

            item[key] = value

        records.append(item)

    return records


def get_blocks() -> List[Dict[str, Any]]:
    df = load_model_dataset()

    if "Block" not in df.columns:
        return []

    results = []

    for block, group in df.groupby("Block"):
        results.append(
            {
                "block": str(block),
                "stations": int(
                    group["Station"].nunique()
                ),
                "observations": int(len(group)),
            }
        )

    return sorted(
        results,
        key=lambda item: item["block"],
    )


def get_predictions() -> List[Dict[str, Any]]:
    df = load_all_predictions()

    if df.empty:
        df = load_latest_prediction()

    if df.empty:
        return []

    records: List[Dict[str, Any]] = []

    for _, row in df.iterrows():
        records.append(
            {
                "station": _safe_value(
                    row.get("Station")
                ),
                "district": _safe_value(
                    row.get("District")
                ),
                "tehsil": _safe_value(
                    row.get("Tehsil")
                ),
                "block": _safe_value(
                    row.get("Block")
                ),
                "village": _safe_value(
                    row.get("Village")
                ),
                "latitude": _safe_float(
                    row.get("Latitude")
                ),
                "longitude": _safe_float(
                    row.get("Longitude")
                ),
                "monitoring_date": _safe_value(
                    row.get("Monitoring Date")
                ),
                "current_groundwater_level": _safe_float(
                    row.get(
                        "Current Groundwater Level (m)"
                    )
                ),
                "predicted_groundwater_level": _safe_float(
                    row.get(
                        "Predicted Next Groundwater Level (m)"
                    )
                ),
                "predicted_change": _safe_float(
                    row.get(
                        "Predicted Groundwater Change (m)"
                    )
                ),
                "predicted_risk": _safe_value(
                    row.get(
                        "Predicted Depletion Risk"
                    )
                ),
                "no_depletion_probability": _safe_float(
                    row.get(
                        "No Depletion Probability"
                    )
                ),
                "low_probability": _safe_float(
                    row.get(
                        "Low Probability"
                    )
                ),
                "moderate_probability": _safe_float(
                    row.get(
                        "Moderate Probability"
                    )
                ),
                "high_probability": _safe_float(
                    row.get(
                        "High Probability"
                    )
                ),
            }
        )

    return records


def get_risk_distribution() -> List[Dict[str, Any]]:
    predictions = get_predictions()

    counts: Dict[str, int] = {}

    for prediction in predictions:
        risk = (
            prediction.get("predicted_risk")
            or "Unknown"
        )

        counts[risk] = (
            counts.get(risk, 0) + 1
        )

    return [
        {
            "risk": risk,
            "count": count,
        }
        for risk, count in counts.items()
    ]


def get_features() -> List[Dict[str, Any]]:
    df = load_feature_importance()

    if df.empty:
        return []

    records = []

    for _, row in df.iterrows():
        item = {
            str(column): _safe_value(
                row[column]
            )
            for column in df.columns
        }

        records.append(item)

    return records
