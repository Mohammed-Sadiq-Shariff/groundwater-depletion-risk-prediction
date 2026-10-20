"""
Baseline models for groundwater depth regression and depletion risk classification.

These transparent reference baselines allow fair benchmarking against
complex machine learning models under the same chronological evaluation split.
"""

from typing import Dict, Any, Optional
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin, ClassifierMixin
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    f1_score,
)


class PersistenceRegressor(BaseEstimator, RegressorMixin):
    """
    Persistence baseline for groundwater level.
    Predicts next_level = current_level (groundwater_level_m).
    """

    def __init__(self, current_col: str = "groundwater_level_m"):
        self.current_col = current_col

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None):
        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        if isinstance(X, pd.DataFrame) and self.current_col in X.columns:
            return X[self.current_col].to_numpy()
        raise ValueError(f"Column '{self.current_col}' required for persistence regression.")


class MeanTargetRegressor(BaseEstimator, RegressorMixin):
    """
    Mean dummy baseline: predicts the scalar mean of training targets.
    """

    def __init__(self):
        self.mean_value_: float = 0.0

    def fit(self, X: Any, y: pd.Series):
        self.mean_value_ = float(np.mean(y))
        return self

    def predict(self, X: Any) -> np.ndarray:
        n_samples = len(X)
        return np.full(n_samples, self.mean_value_)


class MajorityClassClassifier(BaseEstimator, ClassifierMixin):
    """
    Majority class baseline: always predicts the most frequent training class.
    """

    def __init__(self):
        self.majority_class_: Any = None

    def fit(self, X: Any, y: pd.Series):
        self.majority_class_ = pd.Series(y).mode()[0]
        return self

    def predict(self, X: Any) -> np.ndarray:
        n_samples = len(X)
        return np.full(n_samples, self.majority_class_)


def evaluate_regression_baselines(
    test_df: pd.DataFrame,
    train_mean: Optional[float] = None,
    target_col: str = "next_groundwater_level",
    pred_col: str = "predicted_next_groundwater_level",
    current_col: str = "groundwater_level_m",
) -> Dict[str, Dict[str, float]]:
    """
    Compute regression metrics for HistGradientBoosting, Persistence, and Mean baselines.
    """
    y_true = test_df[target_col].to_numpy()
    results = {}

    # 1. Trained model (if predicted column is present)
    if pred_col in test_df.columns:
        y_pred = test_df[pred_col].to_numpy()
        results["HistGradientBoosting"] = {
            "MAE": float(mean_absolute_error(y_true, y_pred)),
            "RMSE": float(np.sqrt(mean_squared_error(y_true, y_pred))),
            "R2": float(r2_score(y_true, y_pred)),
        }

    # 2. Persistence baseline
    if current_col in test_df.columns:
        y_persist = test_df[current_col].to_numpy()
        results["Persistence"] = {
            "MAE": float(mean_absolute_error(y_true, y_persist)),
            "RMSE": float(np.sqrt(mean_squared_error(y_true, y_persist))),
            "R2": float(r2_score(y_true, y_persist)),
        }

    # 3. Mean baseline
    if train_mean is not None:
        y_mean = np.full_like(y_true, fill_value=train_mean)
        results["MeanBaseline"] = {
            "MAE": float(mean_absolute_error(y_true, y_mean)),
            "RMSE": float(np.sqrt(mean_squared_error(y_true, y_mean))),
            "R2": float(r2_score(y_true, y_mean)),
        }

    return results


def evaluate_classification_baselines(
    test_df: pd.DataFrame,
    target_col: str = "depletion_risk",
    pred_col: str = "predicted_depletion_risk",
    majority_class: str = "No Depletion",
) -> Dict[str, Dict[str, float]]:
    """
    Compute classification metrics for Random Forest and Majority Class baselines.
    """
    y_true = test_df[target_col].to_numpy()
    results = {}

    if pred_col in test_df.columns:
        y_pred = test_df[pred_col].to_numpy()
        results["RandomForest"] = {
            "Accuracy": float(accuracy_score(y_true, y_pred)),
            "Macro_F1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
            "Weighted_F1": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
        }

    y_maj = np.full_like(y_true, fill_value=majority_class)
    results["MajorityClass"] = {
        "Accuracy": float(accuracy_score(y_true, y_maj)),
        "Macro_F1": float(f1_score(y_true, y_maj, average="macro", zero_division=0)),
        "Weighted_F1": float(f1_score(y_true, y_maj, average="weighted", zero_division=0)),
    }

    return results
