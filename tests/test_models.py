"""
Essential tests for models, baselines, and evaluation metrics reproducibility.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, r2_score

from groundwater_risk.models.baselines import (
    PersistenceRegressor,
    MeanTargetRegressor,
    MajorityClassClassifier,
    evaluate_regression_baselines,
    evaluate_classification_baselines,
)
from generate_all_predictions import get_season


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_persistence_regressor():
    df = pd.DataFrame({"groundwater_level_m": [10.5, 12.0, 8.2]})
    reg = PersistenceRegressor()
    reg.fit(df)
    preds = reg.predict(df)
    np.testing.assert_array_almost_equal(preds, [10.5, 12.0, 8.2])


def test_mean_target_regressor():
    y_train = pd.Series([10.0, 20.0, 30.0])
    reg = MeanTargetRegressor()
    reg.fit(None, y_train)
    preds = reg.predict(range(4))
    np.testing.assert_array_almost_equal(preds, [20.0, 20.0, 20.0, 20.0])


def test_majority_class_classifier():
    y_train = pd.Series(["Low", "Moderate", "Low", "No Depletion"])
    clf = MajorityClassClassifier()
    clf.fit(None, y_train)
    preds = clf.predict(range(3))
    assert list(preds) == ["Low", "Low", "Low"]


def test_get_season_mapping_consistency():
    # CGWB 4-season campaigns
    assert get_season(1) == "January"
    assert get_season(5) == "Pre_monsoon"
    assert get_season(8) == "Monsoon"
    assert get_season(11) == "Post_monsoon"
    # Seasonal fallback months
    assert get_season(12) == "January"
    assert get_season(4) == "Pre_monsoon"
    assert get_season(7) == "Monsoon"
    assert get_season(10) == "Post_monsoon"


def test_verified_regression_metrics_reproducibility():
    test_pred_path = PROJECT_ROOT / "reports" / "test_prediction_results.csv"
    if not test_pred_path.exists():
        pytest.skip("Test prediction results not found")

    df = pd.read_csv(test_pred_path)
    y_true = df["next_groundwater_level"]
    y_pred = df["predicted_next_groundwater_level"]

    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
    r2 = r2_score(y_true, y_pred)

    assert abs(mae - 1.9384) < 0.01, f"Expected MAE ~ 1.94, got {mae}"
    assert abs(rmse - 2.9568) < 0.01, f"Expected RMSE ~ 2.96, got {rmse}"
    assert abs(r2 - 0.5469) < 0.01, f"Expected R2 ~ 0.55, got {r2}"


def test_verified_risk_metrics_reproducibility():
    risk_pred_path = PROJECT_ROOT / "models" / "risk_test_predictions.csv"
    if not risk_pred_path.exists():
        pytest.skip("Risk test predictions not found")

    df = pd.read_csv(risk_pred_path)
    y_true = df["depletion_risk"]
    y_pred = df["predicted_depletion_risk"]

    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
    high_f1 = f1_score(y_true == "High", y_pred == "High", zero_division=0)

    assert abs(acc - 0.5282) < 0.01, f"Expected Accuracy ~ 0.5282, got {acc}"
    assert abs(macro_f1 - 0.4570) < 0.01, f"Expected Macro F1 ~ 0.4570, got {macro_f1}"
    assert abs(high_f1 - 0.3273) < 0.02, f"Expected High-risk F1 ~ 0.33, got {high_f1}"
