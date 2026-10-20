from pathlib import Path
import warnings

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.inspection import permutation_importance


# ============================================================
# CONFIGURATION
# ============================================================

warnings.filterwarnings("ignore")

RANDOM_STATE = 42

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "mysore_training_dataset.csv"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "groundwater_prediction_model.joblib"
)

FEATURE_INFO_PATH = (
    PROJECT_ROOT
    / "models"
    / "feature_info.joblib"
)

REPORTS_DIR = PROJECT_ROOT / "reports"

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ============================================================
# LOAD DATA
# ============================================================

print_section("LOADING MODEL AND DATA")


if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found:\n{DATA_PATH}"
    )


if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found:\n{MODEL_PATH}"
    )


if not FEATURE_INFO_PATH.exists():
    raise FileNotFoundError(
        f"Feature information not found:\n"
        f"{FEATURE_INFO_PATH}"
    )


df = pd.read_csv(DATA_PATH)

model = joblib.load(
    MODEL_PATH
)

feature_info = joblib.load(
    FEATURE_INFO_PATH
)


print(
    f"\nRecords loaded: {len(df)}"
)

print(
    f"Model loaded from:\n{MODEL_PATH}"
)

print(
    f"\nBest model:"
)

print(
    feature_info["best_model"]
)


# ============================================================
# CONVERT DATE
# ============================================================

print_section("PREPARING DATA")


df["Monitoring Date"] = pd.to_datetime(
    df["Monitoring Date"],
    errors="coerce",
)


invalid_dates = (
    df["Monitoring Date"]
    .isna()
    .sum()
)

print(
    f"\nInvalid dates: {invalid_dates}"
)


df = df.dropna(
    subset=["Monitoring Date"]
).copy()


# ============================================================
# LOAD FEATURES
# ============================================================

feature_columns = (
    feature_info["features"]
)

target_column = (
    feature_info["target"]
)


print(
    f"\nTarget column:"
)

print(
    target_column
)


print(
    f"\nNumber of model features:"
)

print(
    len(feature_columns)
)


# ============================================================
# RECREATE CHRONOLOGICAL TEST SPLIT
# ============================================================

print_section(
    "RECREATING CHRONOLOGICAL TEST SET"
)


df = df.sort_values(
    ["Monitoring Date", "Station"]
).reset_index(
    drop=True
)


unique_dates = np.sort(
    df["Monitoring Date"]
    .unique()
)


train_end_index = int(
    len(unique_dates) * 0.70
)

validation_end_index = int(
    len(unique_dates) * 0.85
)


train_end_date = (
    unique_dates[
        train_end_index - 1
    ]
)

validation_end_date = (
    unique_dates[
        validation_end_index - 1
    ]
)


test_mask = (
    df["Monitoring Date"]
    > validation_end_date
)


test_df = df.loc[
    test_mask
].copy()


X_test = test_df[
    feature_columns
].copy()


y_test = test_df[
    target_column
].copy()


print(
    f"\nTest records: {len(test_df)}"
)


print(
    "\nTest date range:"
)


print(
    test_df[
        "Monitoring Date"
    ].min(),
    "to",
    test_df[
        "Monitoring Date"
    ].max(),
)


# ============================================================
# MAKE PREDICTIONS
# ============================================================

print_section(
    "GENERATING TEST PREDICTIONS"
)


predictions = model.predict(
    X_test
)


# ============================================================
# CALCULATE METRICS
# ============================================================

print_section(
    "TEST PERFORMANCE"
)


mae = mean_absolute_error(
    y_test,
    predictions,
)


rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions,
    )
)


r2 = r2_score(
    y_test,
    predictions,
)


print(
    f"\nMAE:  {mae:.4f}"
)

print(
    f"RMSE: {rmse:.4f}"
)

print(
    f"R²:   {r2:.4f}"
)


# ============================================================
# CREATE PREDICTION RESULTS
# ============================================================

results = test_df[
    [
        "Station",
        "Monitoring Date",
        "groundwater_level_m",
        target_column,
    ]
].copy()


results[
    "predicted_next_groundwater_level"
] = predictions


results[
    "prediction_error"
] = (
    predictions
    -
    results[
        target_column
    ]
)


results[
    "absolute_error"
] = np.abs(
    results[
        "prediction_error"
    ]
)


# ============================================================
# SAVE PREDICTION RESULTS
# ============================================================

predictions_path = (
    REPORTS_DIR
    / "test_prediction_results.csv"
)


results.to_csv(
    predictions_path,
    index=False,
)


print(
    "\nPrediction results saved to:"
)

print(
    predictions_path
)


# ============================================================
# ERROR DISTRIBUTION
# ============================================================

print_section(
    "PREDICTION ERROR DIAGNOSTICS"
)


print(
    "\nPrediction error summary:"
)


print(
    results[
        "prediction_error"
    ].describe()
)


print(
    "\nAbsolute error summary:"
)


print(
    results[
        "absolute_error"
    ].describe()
)


# ============================================================
# STATION LEVEL PERFORMANCE
# ============================================================

print_section(
    "STATION LEVEL PERFORMANCE"
)


station_metrics = (
    results
    .groupby("Station")
    .apply(
        lambda group: pd.Series(
            {
                "records": len(group),
                "mae": mean_absolute_error(
                    group[target_column],
                    group[
                        "predicted_next_groundwater_level"
                    ],
                ),
                "rmse": np.sqrt(
                    mean_squared_error(
                        group[target_column],
                        group[
                            "predicted_next_groundwater_level"
                        ],
                    )
                ),
            }
        ),
        include_groups=False,
    )
    .reset_index()
)


station_metrics = (
    station_metrics
    .sort_values(
        "mae",
        ascending=False,
    )
)


station_metrics_path = (
    REPORTS_DIR
    / "station_performance.csv"
)


station_metrics.to_csv(
    station_metrics_path,
    index=False,
)


print(
    "\nWorst stations by MAE:"
)


print(
    station_metrics
    .head(10)
    .to_string(
        index=False
    )
)


print(
    "\nStation performance saved to:"
)

print(
    station_metrics_path
)


# ============================================================
# PERMUTATION FEATURE IMPORTANCE
# ============================================================

print_section(
    "CALCULATING PERMUTATION FEATURE IMPORTANCE"
)


print(
    "\nThis may take a few minutes..."
)


importance_result = permutation_importance(
    model,
    X_test,
    y_test,
    scoring="neg_mean_absolute_error",
    n_repeats=10,
    random_state=RANDOM_STATE,
    n_jobs=-1,
)


importance_df = pd.DataFrame(
    {
        "feature": feature_columns,
        "importance_mean": (
            importance_result.importances_mean
        ),
        "importance_std": (
            importance_result.importances_std
        ),
    }
)


importance_df = (
    importance_df
    .sort_values(
        "importance_mean",
        ascending=False,
    )
    .reset_index(
        drop=True
    )
)


importance_path = (
    REPORTS_DIR
    / "feature_importance.csv"
)


importance_df.to_csv(
    importance_path,
    index=False,
)


print(
    "\nTop 15 most important features:"
)


print(
    importance_df
    .head(15)
    .to_string(
        index=False
    )
)


print(
    "\nFeature importance saved to:"
)

print(
    importance_path
)


# ============================================================
# PLOT 1
# ACTUAL VS PREDICTED
# ============================================================

print_section(
    "CREATING EVALUATION PLOTS"
)


plt.figure(
    figsize=(8, 8)
)


plt.scatter(
    y_test,
    predictions,
    alpha=0.5,
)


minimum = min(
    y_test.min(),
    predictions.min(),
)

maximum = max(
    y_test.max(),
    predictions.max(),
)


plt.plot(
    [minimum, maximum],
    [minimum, maximum],
)


plt.xlabel(
    "Actual Next Groundwater Level (m)"
)

plt.ylabel(
    "Predicted Next Groundwater Level (m)"
)

plt.title(
    "Actual vs Predicted Groundwater Level"
)


plt.tight_layout()


actual_vs_predicted_path = (
    REPORTS_DIR
    / "actual_vs_predicted.png"
)


plt.savefig(
    actual_vs_predicted_path,
    dpi=300,
)


plt.close()


# ============================================================
# PLOT 2
# ERROR DISTRIBUTION
# ============================================================

plt.figure(
    figsize=(9, 6)
)


plt.hist(
    results[
        "prediction_error"
    ],
    bins=40,
)


plt.axvline(
    0,
    linestyle="--",
)


plt.xlabel(
    "Prediction Error (m)"
)

plt.ylabel(
    "Number of Predictions"
)

plt.title(
    "Groundwater Prediction Error Distribution"
)


plt.tight_layout()


error_distribution_path = (
    REPORTS_DIR
    / "prediction_error_distribution.png"
)


plt.savefig(
    error_distribution_path,
    dpi=300,
)


plt.close()


# ============================================================
# PLOT 3
# FEATURE IMPORTANCE
# ============================================================

top_features = (
    importance_df
    .head(15)
    .sort_values(
        "importance_mean"
    )
)


plt.figure(
    figsize=(10, 7)
)


plt.barh(
    top_features["feature"],
    top_features[
        "importance_mean"
    ],
)


plt.xlabel(
    "Permutation Importance"
)

plt.ylabel(
    "Feature"
)

plt.title(
    "Top 15 Feature Importances"
)


plt.tight_layout()


feature_plot_path = (
    REPORTS_DIR
    / "feature_importance.png"
)


plt.savefig(
    feature_plot_path,
    dpi=300,
)


plt.close()


# ============================================================
# PLOT 4
# OBSERVED VS PREDICTED OVER TIME
# ============================================================

time_results = results.sort_values(
    "Monitoring Date"
)


daily_results = (
    time_results
    .groupby(
        "Monitoring Date"
    )
    .agg(
        actual=(
            target_column,
            "mean",
        ),
        predicted=(
            "predicted_next_groundwater_level",
            "mean",
        ),
    )
    .reset_index()
)


plt.figure(
    figsize=(12, 6)
)


plt.plot(
    daily_results[
        "Monitoring Date"
    ],
    daily_results[
        "actual"
    ],
    label="Actual",
)


plt.plot(
    daily_results[
        "Monitoring Date"
    ],
    daily_results[
        "predicted"
    ],
    label="Predicted",
)


plt.xlabel(
    "Monitoring Date"
)

plt.ylabel(
    "Average Groundwater Level (m)"
)

plt.title(
    "Actual vs Predicted Groundwater Levels Over Time"
)


plt.legend()


plt.tight_layout()


time_plot_path = (
    REPORTS_DIR
    / "actual_vs_predicted_over_time.png"
)


plt.savefig(
    time_plot_path,
    dpi=300,
)


plt.close()


# ============================================================
# SAVE SUMMARY
# ============================================================

summary = pd.DataFrame(
    [
        {
            "model": (
                feature_info[
                    "best_model"
                ]
            ),
            "test_records": len(test_df),
            "mae": mae,
            "rmse": rmse,
            "r2": r2,
        }
    ]
)


summary_path = (
    REPORTS_DIR
    / "model_evaluation_summary.csv"
)


summary.to_csv(
    summary_path,
    index=False,
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print_section(
    "MODEL EVALUATION COMPLETE"
)


print(
    "\nFINAL TEST METRICS"
)


print(
    f"Model: "
    f"{feature_info['best_model']}"
)

print(
    f"MAE:   {mae:.4f} m"
)

print(
    f"RMSE:  {rmse:.4f} m"
)

print(
    f"R²:    {r2:.4f}"
)


print(
    "\nGenerated reports:"
)


print(
    f"\n1. Evaluation summary:"
)

print(
    summary_path
)


print(
    f"\n2. Test predictions:"
)

print(
    predictions_path
)


print(
    f"\n3. Station performance:"
)

print(
    station_metrics_path
)


print(
    f"\n4. Feature importance:"
)

print(
    importance_path
)


print(
    f"\n5. Actual vs predicted plot:"
)

print(
    actual_vs_predicted_path
)


print(
    f"\n6. Error distribution:"
)

print(
    error_distribution_path
)


print(
    f"\n7. Feature importance plot:"
)

print(
    feature_plot_path
)


print(
    f"\n8. Time series plot:"
)

print(
    time_plot_path
)


print("\n" + "=" * 60)